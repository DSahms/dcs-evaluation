#!/usr/bin/env python3
"""
LLM Engineering Evaluation Suite — Automated Scoring Engine

Evaluates an LLM's performance on a job packet assignment.
Scores inquiry quality, deliverable completeness, engineering judgment,
and documentation quality.

Usage:
    python scoring_engine.py --tier S1 --questions path/to/questions.txt \
        --deliverables path/to/deliverables/ [--output path/to/report.json]

The engine produces a detailed score report and prints a summary to stdout.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration Loader
# ---------------------------------------------------------------------------

def load_config(tier: str) -> dict:
    """Load the tier configuration JSON."""
    config_path = Path(__file__).parent / "configs" / f"{tier}.json"
    if not config_path.exists():
        print(f"ERROR: Config not found for tier {tier} at {config_path}")
        sys.exit(1)
    with open(config_path, "r") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# File Helpers
# ---------------------------------------------------------------------------

def read_file(path: Path) -> str | None:
    """Read a file and return its content, or None if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return None


def find_files_recursive(directory: Path, pattern: str = "*") -> list[Path]:
    """Find all files matching pattern in directory recursively."""
    return list(directory.rglob(pattern))


def has_code_files(directory: Path) -> bool:
    """Check if directory contains source code files."""
    code_extensions = {
        ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs",
        ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".swift", ".kt"
    }
    for f in find_files_recursive(directory):
        if f.suffix in code_extensions:
            return True
    return False


def has_test_files(directory: Path) -> bool:
    """Check if directory contains test files."""
    test_patterns = ["test_", "_test.", "spec_", ".spec.", ".test."]
    for f in find_files_recursive(directory):
        fname = f.name.lower()
        if any(p in fname for p in test_patterns):
            return True
    return False


def has_build_instructions(directory: Path, readme_content: str | None) -> bool:
    """Check if build instructions exist (in README or separate file)."""
    if readme_content:
        build_keywords = ["install", "build", "set up", "setup", "getting started",
                          "prerequisite", "npm install", "pip install", "cargo build",
                          "go build", "dotnet build", "make", "compile"]
        lower = readme_content.lower()
        if any(kw in lower for kw in build_keywords):
            return True
    build_file_names = ["BUILD.md", "INSTALL.md", "SETUP.md", "CONTRIBUTING.md"]
    for name in build_file_names:
        if (directory / name).exists():
            return True
    return False


def has_deployment_guide(directory: Path) -> bool:
    """Check if deployment guide exists."""
    deploy_names = ["DEPLOY.md", "DEPLOYMENT.md", "DEPLOY_GUIDE.md",
                    "deploy", "deployment", "DEPLOYMENT_GUIDE.md"]
    for name in deploy_names:
        if (directory / name).exists():
            return True
    # Also check if Architecture.md contains deployment section
    arch = read_file(directory / "Architecture.md")
    if arch and "deploy" in arch.lower():
        return True
    return False


def has_operations_guide(directory: Path) -> bool:
    """Check if operations guide exists."""
    ops_names = ["OPERATIONS.md", "OPS.md", "OPERATIONS_GUIDE.md",
                 "RUNBOOK.md", "operations"]
    for name in ops_names:
        if (directory / name).exists():
            return True
    return False


# ---------------------------------------------------------------------------
# SCORING: Inquiry — Omission Detection
# ---------------------------------------------------------------------------

def score_omission_detection(questions_text: str, config: dict) -> dict:
    """
    Score how many intentional omissions the model's questions identified.
    Uses keyword matching against the answer key.
    """
    questions_lower = questions_text.lower()
    results = []
    total_points = 0
    max_points = config["scoring"]["inquiry_omissions_max"]

    for omission in config["omissions"]:
        matched = False
        matched_keywords = []
        for kw in omission["keywords"]:
            if kw.lower() in questions_lower:
                matched = True
                matched_keywords.append(kw)

        status = "ASKED" if matched else "MISSED"
        points = omission["points"] if matched else 0
        total_points += points

        results.append({
            "id": omission["id"],
            "topic": omission["topic"],
            "weight": omission["weight"],
            "points_earned": points,
            "points_possible": omission["points"],
            "status": status,
            "matched_keywords": matched_keywords if matched else None
        })

    return {
        "score": total_points,
        "max": max_points,
        "details": results
    }


# ---------------------------------------------------------------------------
# SCORING: Inquiry — Question Quality
# ---------------------------------------------------------------------------

def score_question_quality(questions_text: str, config: dict, packet_text: str | None = None) -> dict:
    """
    Score the quality of the model's clarification questions.
    """
    max_points = config["scoring"]["inquiry_quality_max"]
    details = {}
    total = 0

    # Q1: Batch submission — assume YES (we receive questions as one block)
    # In practice, if the evaluator passes multiple question rounds, this would change.
    q1_score = 3
    details["batch_submission"] = {"points": q1_score, "max": 3, "note": "Assumed single submission"}
    total += q1_score

    # Q2: Clear formatting — check for numbered list or clear separators
    lines = [l.strip() for l in questions_text.strip().split("\n") if l.strip()]
    has_numbers = bool(re.search(r'^\s*\d+[\.\)]\s', questions_text, re.MULTILINE))
    has_separators = any(line.startswith(("-", "*", "•", "#", "**")) for line in lines)
    q2_score = 3 if (has_numbers or has_separators) else 0
    details["clear_formatting"] = {
        "points": q2_score, "max": 3,
        "note": "Numbered" if has_numbers else ("Bulleted" if has_separators else "No clear formatting")
    }
    total += q2_score

    # Q3: Packet re-questions — check if questions ask things already in the packet
    requestion_penalty = 0
    requestions_found = []
    if packet_text:
        for rq in config["packet_requestion_patterns"]:
            if re.search(rq["pattern"], questions_text, re.IGNORECASE):
                requestion_penalty += config["requestion_penalty"]
                requestions_found.append(rq["section"])
    q3_score = requestion_penalty  # This is negative or zero
    details["packet_requestions"] = {
        "points": q3_score, "max": 0,
        "penalty_per": config["requestion_penalty"],
        "found": requestions_found
    }
    total += q3_score

    # Q4: Reading comprehension — do questions reference specific packet details?
    # Check for specific numbers, names, or terms from the packet
    comprehension_score = 0
    if packet_text:
        # Extract specific terms from packet (numbers, proper nouns)
        specific_terms = re.findall(r'\b\d{2,}\b|[A-Z][a-z]+(?:\s[A-Z][a-z]+)+', packet_text)
        questions_lower = questions_text.lower()
        referenced = sum(1 for term in specific_terms if term.lower() in questions_lower)
        if referenced >= 2:
            comprehension_score = 5
        elif referenced >= 1:
            comprehension_score = 3
    details["reading_comprehension"] = {
        "points": comprehension_score, "max": 5,
        "note": f"Referenced specific packet details"
    }
    total += comprehension_score

    # Q5: Complexity awareness — are questions appropriate for tier?
    # This is a simplified heuristic. Full version uses LLM-as-judge.
    tier = config["tier"]
    q5_max = {"S1": 3, "S2": 5, "S3": 8}[tier]

    # Check for tier-appropriate question patterns
    junior_patterns = ["what if", "how long", "how does", "what happens", "what kind"]
    mid_patterns = ["concurrent", "conflict", "sync", "real-time", "role", "permission",
                    "granular", "batch", "event", "workflow"]
    senior_patterns = ["migrate", "migration", "compliance", "HIPAA", "RPO", "RTO",
                       "failover", "disaster", "rollout", "phase", "tenant",
                       "BAA", "FHIR", "HL7", "ICD-10", "revenue cycle", "reconcil"]

    questions_lower = questions_text.lower()

    if tier == "S1":
        # Should ask basic business questions, not enterprise architecture
        has_basic = any(p in questions_lower for p in junior_patterns)
        has_enterprise = any(p in questions_lower for p in senior_patterns)
        if has_basic and not has_enterprise:
            q5_score = 3
        elif has_basic:
            q5_score = 1
        else:
            q5_score = 0
    elif tier == "S2":
        has_mid = any(p in questions_lower for p in mid_patterns)
        q5_score = 5 if has_mid else 2
    else:  # S3
        has_senior = any(p in questions_lower for p in senior_patterns)
        q5_score = 8 if has_senior else 3

    details["complexity_awareness"] = {
        "points": q5_score, "max": q5_max,
        "tier": tier
    }
    total += q5_score

    # Q6: Prioritization — did they ask about critical omissions?
    q6_max = {"S1": 3, "S2": 5, "S3": 9}[tier]
    critical_omissions = [o for o in config["omissions"] if o["weight"] == "CRITICAL"]
    if critical_omissions:
        critical_asked = 0
        for o in critical_omissions:
            for kw in o["keywords"]:
                if kw.lower() in questions_lower:
                    critical_asked += 1
                    break
        ratio = critical_asked / len(critical_omissions)
        q6_score = round(ratio * q6_max)
    else:
        q6_score = q6_max  # No critical omissions = full points
    details["prioritization"] = {
        "points": q6_score, "max": q6_max,
        "critical_asked": critical_asked if critical_omissions else "N/A",
        "critical_total": len(critical_omissions)
    }
    total += q6_score

    # No-questions penalty
    if not questions_text.strip():
        total += config["no_questions_penalty"]
        details["no_questions_penalty"] = {"points": config["no_questions_penalty"]}

    # Cap at max
    total = min(total, max_points)

    return {
        "score": max(total, 0),  # Don't go negative for total
        "max": max_points,
        "raw_total": total,
        "details": details
    }


# ---------------------------------------------------------------------------
# SCORING: Deliverable Completeness
# ---------------------------------------------------------------------------

def score_deliverables(deliverables_dir: Path, config: dict) -> dict:
    """Score deliverable file presence and functional requirements coverage."""
    results = {}
    readme_content = read_file(deliverables_dir / "README.md")
    arch_content = read_file(deliverables_dir / "Architecture.md")
    all_content = ""

    # Gather all text content for keyword searches
    for f in find_files_recursive(deliverables_dir):
        if f.suffix in {".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx",
                        ".java", ".go", ".rs", ".rb", ".php", ".cs", ".json",
                        ".yaml", ".yml", ".toml", ".cfg", ".ini"}:
            content = read_file(f)
            if content:
                all_content += "\n" + content

    all_content_lower = all_content.lower()

    # --- Required Files ---
    file_results = []
    file_score = 0
    file_max = config["scoring"]["deliverables_files_max"]

    for req in config["required_files"]:
        name = req["name"]
        points = req["points"]
        found = False

        if req.get("check") == "has_code_files":
            found = has_code_files(deliverables_dir)
        elif req.get("check") == "has_test_files":
            found = has_test_files(deliverables_dir)
        elif req.get("check") == "has_build_instructions":
            found = has_build_instructions(deliverables_dir, readme_content)
        elif req.get("check") == "has_deployment_guide":
            found = has_deployment_guide(deliverables_dir)
        elif req.get("check") == "has_operations_guide":
            found = has_operations_guide(deliverables_dir)
        else:
            # Direct filename check
            found = (deliverables_dir / name).exists()

        if found:
            file_score += points

        file_results.append({
            "name": name,
            "points": points if found else 0,
            "max": points,
            "status": "PRESENT" if found else "MISSING"
        })

    results["files"] = {"score": file_score, "max": file_max, "details": file_results}

    # --- Functional Requirements ---
    req_results = []
    req_score = 0
    req_max = config["scoring"]["deliverables_requirements_max"]

    for req in config["functional_requirements"]:
        name = req["name"]
        points = req["points"]
        keywords = req["keywords"]

        # Check if any keyword appears in the combined content
        addressed = any(kw.lower() in all_content_lower for kw in keywords)

        if addressed:
            req_score += points

        req_results.append({
            "name": name,
            "points": points if addressed else 0,
            "max": points,
            "status": "ADDRESSED" if addressed else "MISSING"
        })

    results["requirements"] = {"score": req_score, "max": req_max, "details": req_results}

    total_score = file_score + req_score
    total_max = file_max + req_max

    return {"score": total_score, "max": total_max, "details": results}


# ---------------------------------------------------------------------------
# SCORING: Engineering Judgment — ASSUMPTIONS.md
# ---------------------------------------------------------------------------

def score_assumptions(deliverables_dir: Path, config: dict) -> dict:
    """Score ASSUMPTIONS.md quality — structure, reasoning, relevance."""
    max_points = config["scoring"]["engineering_assumptions_max"]
    assumptions_path = deliverables_dir / "ASSUMPTIONS.md"
    content = read_file(assumptions_path)

    if not content:
        return {"score": 0, "max": max_points, "details": {"note": "ASSUMPTIONS.md not found"}}

    # Parse assumptions — look for structured entries with the 4 required fields
    # Supports various formats: markdown headers, bullet points, numbered lists
    content_lower = content.lower()

    # Try to identify assumption blocks
    # Look for patterns that indicate structured assumptions
    blocks = re.split(r'\n(?=#{1,3}\s|\d+[\.\)]\s|\-\s+\*\*|\*\*\d+)', content)

    # Simpler approach: check for the 4 required labels anywhere in the file
    has_unknown_label = bool(re.search(
        r'\bunknown\b', content_lower
    ))
    has_decision_label = bool(re.search(
        r'\bdecision\b', content_lower
    ))
    has_reasoning_label = bool(re.search(
        r'\breason(?:ing)?\b', content_lower
    ))
    has_risk_label = bool(re.search(
        r'\brisk\b', content_lower
    ))

    # Count assumption entries (heuristic: count occurrences of "Unknown" or numbered items)
    assumption_count = max(
        len(re.findall(r'(?:^|\n)\s*(?:#{1,3}\s|\d+[\.\)]\s)\s*.*?(?:assumption|unknown)', content_lower)),
        len(re.findall(r'\*\*unknown\*\*', content_lower)),
        len(re.findall(r'\bunknown\b', content_lower)),
        1  # minimum 1 if file exists
    )
    assumption_count = min(assumption_count, 10)  # Cap at 10 scored

    # Score per-assumption structure
    per_assumption = 0
    if has_unknown_label:
        per_assumption += 2
    if has_decision_label:
        per_assumption += 3
    if has_reasoning_label:
        per_assumption += 3
    if has_risk_label:
        per_assumption += 2

    structure_score = per_assumption * min(assumption_count, 5)  # Scale by count (up to 5)
    structure_max = 10 * 5  # Theoretical max
    normalized_structure = round((structure_score / structure_max) * (max_points - 5))  # Leave 5pts for bonuses

    # Bonus: Relevance — check if assumptions relate to omissions
    relevance_bonus = 0
    omission_topics = [o["topic"].lower() for o in config["omissions"]]
    relevant_count = sum(1 for topic in omission_topics if any(word in content_lower for word in topic.split()))
    if relevant_count >= 3:
        relevance_bonus = 3
    elif relevant_count >= 1:
        relevance_bonus = 1

    # Bonus: Edge case assumption
    edge_case_bonus = 0
    edge_case_terms = ["edge case", "failure", "timeout", "network", "offline",
                       "concurrent", "race condition", "error", "exception", "fallback"]
    if any(term in content_lower for term in edge_case_terms):
        edge_case_bonus = 2

    total = normalized_structure + relevance_bonus + edge_case_bonus
    total = min(total, max_points)

    return {
        "score": total,
        "max": max_points,
        "details": {
            "assumption_count_detected": assumption_count,
            "has_unknown": has_unknown_label,
            "has_decision": has_decision_label,
            "has_reasoning": has_reasoning_label,
            "has_risk": has_risk_label,
            "relevance_bonus": relevance_bonus,
            "edge_case_bonus": edge_case_bonus
        }
    }


# ---------------------------------------------------------------------------
# SCORING: Engineering Judgment — Architecture.md
# ---------------------------------------------------------------------------

def score_architecture(deliverables_dir: Path, config: dict) -> dict:
    """Score Architecture.md quality — reasoning, NFRs, appropriateness, tradeoffs."""
    max_points = config["scoring"]["engineering_architecture_max"]
    arch_path = deliverables_dir / "Architecture.md"
    content = read_file(arch_path)

    if not content:
        return {"score": 0, "max": max_points, "details": {"note": "Architecture.md not found"}}

    content_lower = content.lower()
    word_count = len(content.split())
    details = {}
    total = 0

    # A1: Architecture documented (not just code comments)
    a1_max = 3
    a1_score = a1_max if word_count > 200 else 0
    details["documented"] = {"points": a1_score, "max": a1_max, "word_count": word_count}
    total += a1_score

    # A2: Technology choices stated
    a2_max = 3
    tech_terms = ["framework", "language", "database", "db ", "stack", "react", "vue",
                  "angular", "django", "flask", "express", "node", "postgres", "mysql",
                  "sqlite", "mongodb", "python", "javascript", "typescript", "java", "go",
                  "rust", "next.js", "rails", "spring", "laravel", ".net"]
    a2_score = a2_max if any(t in content_lower for t in tech_terms) else 0
    details["tech_choices_stated"] = {"points": a2_score, "max": a2_max}
    total += a2_score

    # A3: Technology choices include REASONING (why, not just what)
    tier = config["tier"]
    a3_max = {"S1": 5, "S2": 7, "S3": 10}[tier]
    reasoning_patterns = [
        r"because", r"reason", r"chose.*because", r"selected.*for",
        r"why.*chose", r"rationale", r"justif", r"trade-off", r"tradeoff",
        r"advantage", r"benefit", r"suit", r"appropriate for", r"given the"
    ]
    has_reasoning = any(re.search(p, content_lower) for p in reasoning_patterns)
    # Check for reasoning that references requirements
    references_reqs = any(term in content_lower for term in
                          ["requirement", "user", "scale", "security", "reliab",
                           "perform", "budget", "simple", "small business",
                           "150 user", "8000", "hospital", "HIPAA"])
    if has_reasoning and references_reqs:
        a3_score = a3_max
    elif has_reasoning:
        a3_score = round(a3_max * 0.6)
    else:
        a3_score = 0
    details["tech_choices_reasoned"] = {"points": a3_score, "max": a3_max,
                                        "has_reasoning": has_reasoning,
                                        "references_requirements": references_reqs}
    total += a3_score

    # A4: Architecture addresses non-functional requirements
    a4_max = {"S1": 3, "S2": 5, "S3": 8}[tier]
    nfr_terms = {
        "S1": ["easy to use", "responsive", "mobile", "reliab", "desktop", "browser"],
        "S2": ["reliab", "scalab", "cloud", "perform", "downtime", "delay"],
        "S3": ["24x7", "24/7", "availab", "reliab", "scalab", "8000", "concurrent"]
    }
    nfr_found = sum(1 for term in nfr_terms[tier] if term in content_lower)
    nfr_total = len(nfr_terms[tier])
    a4_score = round((nfr_found / nfr_total) * a4_max) if nfr_total > 0 else 0
    details["nfrs_addressed"] = {"points": a4_score, "max": a4_max,
                                  "found": nfr_found, "total": nfr_total}
    total += a4_score

    # A5: Architecture appropriateness (over/under-engineering check)
    # IMPORTANT: Must detect negation context — if the doc REJECTS a pattern,
    # that's a POSITIVE signal (they considered and rejected it), not over-engineering.
    a5_max = {"S1": 4, "S2": 6, "S3": 10}[tier]
    over_signals = config["over_engineering_signals"]
    under_signals = config["under_engineering_signals"]

    # Negation patterns that indicate the author REJECTED the approach
    negation_patterns = [
        r"(don'?t|do not|didn'?t|does not|won'?t|would not|should not|is not|aren'?t)\s+need",
        r"(don'?t|do not|didn'?t|does not|won'?t|would not|should not|is not|aren'?t)\s+(use|require|want|need|recommend)",
        r"(avoid|rejected|inappropriate|overkill|over-engineer|unnecessary|too complex)",
        r"not (appropriate|needed|necessary|required|suitable|warranted)",
        r"would be (overkill|inappropriate|unnecessary|too much)",
        r"no (need for|reason to|requirement for|need of)",
        r"(monolith|simple) (is|would be) (better|appropriate|sufficient|enough|the right)",
        r"chose (a |the )?(monolith|simple)",
    ]
    negation_regex = re.compile('|'.join(negation_patterns), re.IGNORECASE)

    def is_negated(signal: str, text: str) -> bool:
        """Check if a signal word appears in a negation context."""
        pattern = re.compile(re.escape(signal), re.IGNORECASE)
        for match in pattern.finditer(text):
            # Get surrounding context (100 chars before and after)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context = text[start:end]
            if negation_regex.search(context):
                return True
        return False

    over_found = [s for s in over_signals
                  if s.lower() in content_lower and not is_negated(s, content)]
    under_found = [s for s in under_signals
                   if s.lower() in content_lower and not is_negated(s, content)]

    if over_found:
        a5_score = 0
        a5_status = "OVER-ENGINEERED"
        a5_signals = over_found
    elif under_found:
        a5_score = 0
        a5_status = "UNDER-ENGINEERED"
        a5_signals = under_found
    else:
        a5_score = a5_max
        a5_status = "APPROPRIATE"
        a5_signals = []
    details["appropriateness"] = {"points": a5_score, "max": a5_max,
                                   "status": a5_status, "signals": a5_signals}
    total += a5_score

    # A6: Tradeoffs and limitations acknowledged
    a6_max = {"S1": 2, "S2": 4, "S3": 7}[tier]
    tradeoff_terms = ["trade-off", "tradeoff", "limitation", "drawback", "downside",
                      "compromise", "sacrifice", "risk", "won't scale", "doesn't support",
                      "not suitable", "future improvement", "v2", "phase 2", "later",
                      "constraint", "caveat"]
    has_tradeoffs = any(term in content_lower for term in tradeoff_terms)
    a6_score = a6_max if has_tradeoffs else 0
    details["tradeoffs"] = {"points": a6_score, "max": a6_max, "acknowledged": has_tradeoffs}
    total += a6_score

    total = min(total, max_points)

    return {"score": total, "max": max_points, "details": details}


# ---------------------------------------------------------------------------
# SCORING: Engineering Judgment — Security
# ---------------------------------------------------------------------------

def score_security(deliverables_dir: Path, config: dict) -> dict:
    """Score security requirements coverage."""
    max_points = config["scoring"]["engineering_security_max"]
    arch_content = read_file(deliverables_dir / "Architecture.md")
    all_content = ""

    for f in find_files_recursive(deliverables_dir):
        if f.suffix in {".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".java",
                        ".go", ".rs", ".rb", ".php", ".cs", ".yaml", ".yml"}:
            c = read_file(f)
            if c:
                all_content += "\n" + c

    all_lower = all_content.lower()
    sec_results = []
    sec_score = 0

    for req in config["security_requirements"]:
        name = req["name"]
        points = req["points"]
        keywords = req["keywords"]
        addressed = any(kw.lower() in all_lower for kw in keywords)
        if addressed:
            sec_score += points
        sec_results.append({
            "name": name,
            "points": points if addressed else 0,
            "max": points,
            "status": "ADDRESSED" if addressed else "MISSING"
        })

    return {"score": sec_score, "max": max_points, "details": sec_results}


# ---------------------------------------------------------------------------
# SCORING: Documentation — README Quality
# ---------------------------------------------------------------------------

# Known technical terms that should be explained for non-technical users
TECH_TERMS = [
    "node", "npm", "npx", "yarn", "pnpm", "pip", "pipenv", "poetry",
    "virtualenv", "venv", "conda", "anaconda", "docker", "container",
    "git", "github", "repository", "clone", "fork", "branch", "commit",
    "api", "rest", "graphql", "http", "https", "ssl", "tls",
    "database", "sql", "nosql", "postgres", "mysql", "sqlite", "mongodb",
    "redis", "orm", "migration", "seed", "schema",
    "framework", "react", "vue", "angular", "django", "flask", "express",
    "typescript", "javascript", "python", "java", "go", "rust",
    "env", "environment variable", "dotenv", "config",
    "localhost", "port", "server", "deploy", "build", "compile",
    "dependency", "package", "install", "require",
    "cli", "command line", "terminal", "shell", "bash", "zsh",
    "ci/cd", "github actions", "jenkins", "kubernetes", "k8s",
    "oauth", "jwt", "token", "session", "cookie", "cors",
    "css", "html", "tailwind", "sass", "scss", "webpack", "vite",
    "protobuf", "grpc", "websocket", "microservice",
    "ubuntu", "debian", "linux", "macos", "windows",
    "homebrew", "apt", "yum", "choco", "scoop",
    "cd", "ls", "mkdir", "touch", "chmod", "export", "source",
    "run", "start", "dev", "production", "development",
    "lint", "format", "test", "coverage", "debug",
    "middleware", "route", "controller", "model", "view",
    "component", "hook", "state", "prop", "render",
    "async", "await", "promise", "callback",
    "tcp", "udp", "dns", "ssl", "certificate",
    "json", "xml", "yaml", "csv",
    "log", "logging", "debug", "trace",
    "cache", "queue", "worker", "cron", "scheduler",
    "pdf", "export", "import", "upload", "download",
    "responsive", "mobile", "desktop", "browser",
    "ssl", "tls", "certificate", "https",
    "encryption", "hash", "salt", "bcrypt",
    "rbac", "role", "permission", "auth", "sso", "ldap",
    "hipaa", "phi", "baa", "compliance", "audit"
]


def check_readme_section(readme: str, section_keywords: list[str]) -> dict:
    """Check if a README section exists and is accessible."""
    readme_lower = readme.lower()
    lines = readme.split("\n")

    # Find the section
    section_start = -1
    section_end = len(lines)

    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        # Check for markdown headings or bold text that matches section keywords
        for kw in section_keywords:
            if (line_lower.startswith("#") and kw in line_lower) or \
               (line_lower.startswith(f"**{kw}") or f" {kw} " in f" {line_lower} "):
                section_start = i
                break
        if section_start >= 0:
            break

    if section_start < 0:
        return {"present": False, "accessible": False, "section_text": ""}

    # Find end of section (next heading or end of file)
    for i in range(section_start + 1, len(lines)):
        if lines[i].strip().startswith("#"):
            section_end = i
            break

    section_text = "\n".join(lines[section_start:section_end])

    # Check accessibility: do technical terms have explanations?
    terms_in_section = [t for t in TECH_TERMS if t.lower() in section_text.lower()]
    explained_terms = 0

    for term in terms_in_section:
        # Look for explanation patterns near the term
        term_regex = re.compile(re.escape(term), re.IGNORECASE)
        for match in term_regex.finditer(section_text):
            start = max(0, match.start() - 10)
            end = min(len(section_text), match.end() + 80)
            context = section_text[start:end]
            explanation_patterns = [
                r'—\s', r' - ', r':\s', r'\(\s', r'is a ', r'is an ',
                r'is used', r'allows', r'lets you', r'enables',
                r'manages', r'handles', r'provides', r'runs',
                r'packages', r'tools? that', r'software that',
                r'environment', r'system for', r'manager for'
            ]
            if any(re.search(p, context, re.IGNORECASE) for p in explanation_patterns):
                explained_terms += 1
                break

    if terms_in_section:
        accessibility_ratio = explained_terms / len(terms_in_section)
        accessible = accessibility_ratio >= 0.5
    else:
        # No technical terms — check if section has meaningful content
        accessible = len(section_text.strip()) > 50

    return {
        "present": True,
        "accessible": accessible,
        "terms_found": len(terms_in_section),
        "terms_explained": explained_terms,
        "section_length": len(section_text.strip())
    }


def score_documentation(deliverables_dir: Path, config: dict) -> dict:
    """Score README documentation quality — 8 required sections."""
    max_points = config["scoring"]["documentation_max"]
    readme_content = read_file(deliverables_dir / "README.md")

    if not readme_content:
        return {"score": 0, "max": max_points, "details": {"note": "README.md not found"}}

    tier = config["tier"]

    # Define sections and their point values per tier
    sections = [
        {
            "id": "D1",
            "name": "Prerequisites",
            "tier_points": {"S1": 3, "S2": 3, "S3": 3},
            "keywords": ["prerequisite", "prerequisites", "requirements", "before you begin",
                         "what you need", "dependencies", "pre-install", "install first"]
        },
        {
            "id": "D2",
            "name": "What Each Prerequisite IS",
            "tier_points": {"S1": 3, "S2": 3, "S3": 3},
            "keywords": ["prerequisite", "requirement", "dependency", "you'll need",
                         "you will need"]
            # This is checked as a sub-check of D1 accessibility
        },
        {
            "id": "D3",
            "name": "Step-by-step Installation",
            "tier_points": {"S1": 5, "S2": 5, "S3": 3},
            "keywords": ["install", "installation", "set up", "setup", "getting started",
                         "how to install", "installing"]
        },
        {
            "id": "D4",
            "name": "Configuration",
            "tier_points": {"S1": 4, "S2": 5, "S3": 4},
            "keywords": ["config", "configuration", "environment", "env", "setting",
                         "settings", ".env"]
        },
        {
            "id": "D5",
            "name": "Database Setup",
            "tier_points": {"S1": 4, "S2": 4, "S3": 3},
            "keywords": ["database", "db setup", "migration", "migrate", "seed",
                         "schema", "create database", "postgres", "mysql", "sqlite"]
        },
        {
            "id": "D6",
            "name": "Running the App",
            "tier_points": {"S1": 4, "S2": 5, "S3": 5},
            "keywords": ["run", "running", "start", "starting", "launch", "execute",
                         "how to run", "start the app", "npm start", "python ", "go run",
                         "cargo run", "dotnet run"]
        },
        {
            "id": "D7",
            "name": "Troubleshooting",
            "tier_points": {"S1": 4, "S2": 5, "S3": 5},
            "keywords": ["troubleshoot", "troubleshooting", "trouble", "problem", "issue",
                         "common issue", "faq", "help", "error", "fix", "known issue"]
        },
        {
            "id": "D8",
            "name": "Project Structure",
            "tier_points": {"S1": 3, "S2": 5, "S3": 4},
            "keywords": ["project structure", "folder", "directory", "file structure",
                         "codebase", "repository structure", "project layout"]
        }
    ]

    section_results = []
    total_score = 0
    anti_pattern_deductions = 0

    for sec in sections:
        pts = sec["tier_points"][tier]
        result = check_readme_section(readme_content, sec["keywords"])

        if not result["present"]:
            sec_score = 0
            status = "MISSING"
        elif not result["accessible"]:
            sec_score = round(pts * 0.4)
            status = "PRESENT (not accessible)"
        else:
            sec_score = pts
            status = "PRESENT+ACCESSIBLE"

        # D2 is special — it's an accessibility sub-check of D1
        if sec["id"] == "D2":
            # Check if D1's section explains what prerequisites ARE
            d1_result = check_readme_section(readme_content, sections[0]["keywords"])
            if d1_result["present"] and d1_result.get("terms_explained", 0) > 0:
                sec_score = pts
                status = "PRESENT+ACCESSIBLE"
            elif d1_result["present"]:
                sec_score = round(pts * 0.4)
                status = "PRESENT (terms not explained)"
            else:
                sec_score = 0
                status = "MISSING"

        total_score += sec_score

        section_results.append({
            "id": sec["id"],
            "name": sec["name"],
            "points": sec_score,
            "max": pts,
            "status": status
        })

    # Check anti-patterns
    readme_lower = readme_content.lower()
    anti_patterns = [
        (r"just run (npm install|pip install|go mod|cargo build)", 3,
         "Assumes reader knows what the command does"),
        (r"see (the )?(doc|documentation|readme) for", 2,
         "Circular reference to documentation"),
    ]
    for pattern, deduction, reason in anti_patterns:
        if re.search(pattern, readme_lower):
            anti_pattern_deductions += deduction

    # Check for unexplained jargon
    jargon_terms = ["orm", "ci/cd", "kubernetes", "k8s", "graphql",
                    "oauth", "jwt", "cors", "rbac", "sso", "ldap",
                    "hipaa", "phi", "baa"]
    unexplained_jargon = 0
    for term in jargon_terms:
        if term in readme_lower:
            # Check if explained nearby
            idx = readme_lower.index(term)
            context = readme_lower[max(0, idx - 10):min(len(readme_lower), idx + 100)]
            explanation = any(p in context for p in
                             [" is ", " — ", " - ", ":", "stands for", "meaning", "which is"])
            if not explanation:
                unexplained_jargon += 1

    jargon_deduction = min(unexplained_jargon, 5)
    anti_pattern_deductions += jargon_deduction

    final_score = max(0, total_score - anti_pattern_deductions)
    final_score = min(final_score, max_points)

    return {
        "score": final_score,
        "max": max_points,
        "sections": section_results,
        "anti_pattern_deductions": anti_pattern_deductions,
        "unexplained_jargon_count": unexplained_jargon
    }


# ---------------------------------------------------------------------------
# Report Generation
# ---------------------------------------------------------------------------

def generate_report(tier_config: dict, inquiry_omissions: dict,
                    inquiry_quality: dict, deliverables: dict,
                    assumptions: dict, architecture: dict,
                    security: dict, documentation: dict) -> dict:
    """Generate the full evaluation report."""
    scoring = tier_config["scoring"]
    max_total = tier_config["max_total_score"]

    # Calculate totals per category
    inquiry_total = inquiry_omissions["score"] + inquiry_quality["score"]
    inquiry_max = scoring["inquiry_omissions_max"] + scoring["inquiry_quality_max"]

    deliverables_total = deliverables["score"]
    deliverables_max = scoring["deliverables_files_max"] + scoring["deliverables_requirements_max"]

    engineering_total = (assumptions["score"] + architecture["score"] + security["score"])
    engineering_max = scoring["engineering_assumptions_max"] + scoring["engineering_architecture_max"] + scoring["engineering_security_max"]

    documentation_total = documentation["score"]
    documentation_max = scoring["documentation_max"]

    final_score = inquiry_total + deliverables_total + engineering_total + documentation_total
    percentage = round((final_score / max_total) * 100, 1) if max_total > 0 else 0

    # Grade
    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return {
        "tier": tier_config["tier"],
        "tier_name": tier_config["name"],
        "timestamp": datetime.now().isoformat(),
        "scores": {
            "inquiry_omissions": inquiry_omissions,
            "inquiry_quality": inquiry_quality,
            "inquiry_total": {"score": inquiry_total, "max": inquiry_max},
            "deliverables": deliverables,
            "deliverables_total": {"score": deliverables_total, "max": deliverables_max},
            "assumptions": assumptions,
            "architecture": architecture,
            "security": security,
            "engineering_total": {"score": engineering_total, "max": engineering_max},
            "documentation": documentation,
            "documentation_total": {"score": documentation_total, "max": documentation_max}
        },
        "final": {
            "score": final_score,
            "max": max_total,
            "percentage": percentage,
            "grade": grade
        }
    }


def print_report(report: dict):
    """Print a human-readable summary of the evaluation report."""
    s = report["scores"]
    f = report["final"]

    print("=" * 60)
    print(f"  EVALUATION RESULTS — {report['tier']} ({report['tier_name']})")
    print(f"  Date: {report['timestamp'][:10]}")
    print("=" * 60)

    # Inquiry
    print("\n--- INQUIRY ---")
    print(f"  Omission Detection: {s['inquiry_omissions']['score']}/{s['inquiry_omissions']['max']}")
    for d in s["inquiry_omissions"]["details"]:
        status_icon = "+" if d["status"] == "ASKED" else "x"
        print(f"    [{status_icon}] {d['topic']} ({d['weight']}): "
              f"{d['points_earned']}/{d['points_possible']} — {d['status']}")
    print(f"  Question Quality: {s['inquiry_quality']['score']}/{s['inquiry_quality']['max']}")
    for key, val in s["inquiry_quality"]["details"].items():
        pts = val.get("points", 0)
        mx = val.get("max", 0)
        note = val.get("note", "")
        print(f"    {key}: {pts}/{mx} {note}")
    print(f"  INQUIRY TOTAL: {s['inquiry_total']['score']}/{s['inquiry_total']['max']}")

    # Deliverables
    print("\n--- DELIVERABLES ---")
    for file_d in s["deliverables"]["details"]["files"]["details"]:
        icon = "+" if file_d["status"] == "PRESENT" else "x"
        print(f"    [{icon}] {file_d['name']}: {file_d['points']}/{file_d['max']}")
    for req_d in s["deliverables"]["details"]["requirements"]["details"]:
        icon = "+" if req_d["status"] == "ADDRESSED" else "x"
        print(f"    [{icon}] {req_d['name']}: {req_d['points']}/{req_d['max']}")
    print(f"  DELIVERABLES TOTAL: {s['deliverables_total']['score']}/{s['deliverables_total']['max']}")

    # Engineering Judgment
    print("\n--- ENGINEERING JUDGMENT ---")
    a = s["assumptions"]
    print(f"  Assumptions Quality: {a['score']}/{a['max']}")
    if "details" in a and "note" not in a.get("details", {}):
        d = a["details"]
        print(f"    Assumptions detected: {d.get('assumption_count_detected', '?')}")
        print(f"    Structure: Unknown={d.get('has_unknown')}, Decision={d.get('has_decision')}, "
              f"Reasoning={d.get('has_reasoning')}, Risk={d.get('has_risk')}")
        print(f"    Relevance bonus: +{d.get('relevance_bonus', 0)}")
        print(f"    Edge case bonus: +{d.get('edge_case_bonus', 0)}")

    arch = s["architecture"]
    print(f"  Architecture Quality: {arch['score']}/{arch['max']}")
    if "details" in arch:
        d = arch["details"]
        for key in ["documented", "tech_choices_stated", "tech_choices_reasoned",
                     "nfrs_addressed", "appropriateness", "tradeoffs"]:
            if key in d:
                item = d[key]
                extra = ""
                if key == "appropriateness":
                    extra = f" — {item.get('status', '')}"
                    if item.get("signals"):
                        extra += f" (signals: {', '.join(item['signals'][:3])})"
                print(f"    {key}: {item.get('points', 0)}/{item.get('max', 0)}{extra}")

    sec = s["security"]
    print(f"  Security: {sec['score']}/{sec['max']}")
    if isinstance(sec.get("details"), list):
        for item in sec["details"]:
            icon = "+" if item["status"] == "ADDRESSED" else "x"
            print(f"    [{icon}] {item['name']}: {item['points']}/{item['max']}")

    print(f"  ENGINEERING TOTAL: {s['engineering_total']['score']}/{s['engineering_total']['max']}")

    # Documentation
    print("\n--- DOCUMENTATION ---")
    for sec_item in s["documentation"].get("sections", []):
        print(f"    {sec_item['name']}: {sec_item['points']}/{sec_item['max']} — {sec_item['status']}")
    if s["documentation"].get("anti_pattern_deductions", 0) > 0:
        print(f"    Anti-pattern deductions: -{s['documentation']['anti_pattern_deductions']}")
    print(f"  DOCUMENTATION TOTAL: {s['documentation_total']['score']}/{s['documentation_total']['max']}")

    # Final
    print("\n" + "=" * 60)
    print(f"  FINAL SCORE: {f['score']}/{f['max']} ({f['percentage']}%)")
    print(f"  GRADE: {f['grade']}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LLM Engineering Evaluation Suite — Scoring Engine"
    )
    parser.add_argument(
        "--tier", required=True, choices=["S1", "S2", "S3"],
        help="Evaluation tier (S1=Junior, S2=Mid, S3=Enterprise)"
    )
    parser.add_argument(
        "--questions", required=True,
        help="Path to file containing the model's clarification questions (text)"
    )
    parser.add_argument(
        "--deliverables", required=True,
        help="Path to directory containing the model's deliverables"
    )
    parser.add_argument(
        "--packet", default=None,
        help="Path to the job packet (for re-question detection)"
    )
    parser.add_argument(
        "--output", default=None,
        help="Path to save JSON report (optional)"
    )

    args = parser.parse_args()

    # Load config
    config = load_config(args.tier)
    print(f"Loaded config for {config['tier']} — {config['name']}")
    print(f"Max possible score: {config['max_total_score']}")

    # Load inputs
    questions_text = read_file(Path(args.questions))
    if questions_text is None:
        print(f"ERROR: Questions file not found: {args.questions}")
        sys.exit(1)

    deliverables_dir = Path(args.deliverables)
    if not deliverables_dir.is_dir():
        print(f"ERROR: Deliverables directory not found: {args.deliverables}")
        sys.exit(1)

    packet_text = None
    if args.packet:
        packet_text = read_file(Path(args.packet))

    print(f"Questions file: {args.questions} ({len(questions_text)} chars)")
    print(f"Deliverables dir: {args.deliverables}")

    # Run all scorers
    print("\nScoring...")

    inquiry_omissions = score_omission_detection(questions_text, config)
    inquiry_quality = score_question_quality(questions_text, config, packet_text)
    deliverables = score_deliverables(deliverables_dir, config)
    assumptions = score_assumptions(deliverables_dir, config)
    architecture = score_architecture(deliverables_dir, config)
    security = score_security(deliverables_dir, config)
    documentation = score_documentation(deliverables_dir, config)

    # Generate report
    report = generate_report(
        config, inquiry_omissions, inquiry_quality, deliverables,
        assumptions, architecture, security, documentation
    )

    # Print report
    print_report(report)

    # Save JSON report
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nJSON report saved to: {output_path}")

    # Also save a default location
    default_output = Path(__file__).parent / f"results_{config['tier']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    default_output.parent.mkdir(parents=True, exist_ok=True)
    with open(default_output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"JSON report also saved to: {default_output}")


if __name__ == "__main__":
    main()