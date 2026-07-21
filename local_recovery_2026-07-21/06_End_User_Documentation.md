# Stage 4C — End-User Documentation Judge (Mandatory)

**This is not optional.** GitHub README culture assumes the reader is a developer peer. This benchmark assumes the reader is **a willing non-developer beta tester** — smart, willing, but has never sideloaded an APK and will abort if the screen says "unknown source."

---

## Why this gate exists

Beautiful repos fail in the real world because:

- Install steps assume terminal, git, and IDE literacy  
- "Just run `./install.sh`" is meaningless to most humans  
- Permission prompts (unknown source, firewall, mic access) look malicious without explanation  
- Devs hand off to devs; **customers and hobby beta testers get nothing**

**Mandatory deliverable:** `USER_GUIDE.md` or `docs/user-guide/` — separate from developer README.

---

## Packet requirement (`04_end_user_doc_requirements.md`)

Stage 0 must define for this app:

| Section | Required content |
|---------|------------------|
| **Who this is for** | "You don't need to be technical" |
| **What you need** | Device, OS version, internet yes/no |
| **Install steps** | Numbered, one action per step, no jargon |
| **Scary screens** | Plain language for permission / unknown source / SmartScreen |
| **First run** | What they should see in the first 60 seconds |
| **Daily use** | Core tasks in order |
| **Troubleshooting** | "If X happens, do Y" |
| **Getting help** | Who to contact, what info to send |
| **Uninstall** | How to remove cleanly |

---

## Formatting standards (concise but readable)

The guide must be **scannable** — not a wall of prose.

Required:

- Clear **headings** (H1 → H2 → H3)  
- **Numbered steps** for procedures  
- **Bold** for button names, menu items, and warnings  
- Short paragraphs (2–4 lines max)  
- Warning callouts for permissions and security prompts  

Optional but encouraged:

- Table of contents for guides over ~2 pages  
- Screenshots or placeholders (`[screenshot: install prompt]`)  
- "Time required: ~5 minutes" at top  

**Not acceptable:**

- README-only with clone/build commands  
- "Ask the developer" as install step  
- Assuming APK sideload, Homebrew, or `npm install` without explaining  

---

## Judge prompt

    You are evaluating END-USER DOCUMENTATION only.

    You are NOT a developer. You have never used a terminal for this app.
    You will follow USER_GUIDE.md exactly as written, mentally or against the submission.

    Inputs:
    1. End-user doc requirements from benchmark packet
    2. Submitted USER_GUIDE (or docs/user-guide/)
    3. Submitted project (to verify steps are plausible)

    Score:

    {
      "end_user_documentation": {
        "score": 0,
        "max": 15,
        "exists_separate_from_dev_readme": true,
        "install_without_author": { "pass": false, "notes": "" },
        "first_run_clear": { "pass": false, "notes": "" },
        "scary_prompts_explained": { "pass": false, "notes": "" },
        "troubleshooting": { "pass": false, "notes": "" },
        "scannable_format": { "pass": false, "notes": "" },
        "deductions": []
      }
    }

---

## Mobile sideload example (real world)

Beta tester receives a link → permission flow → **"unknown source"** → without you there, she stops.

A passing user guide includes a section like:

> **If your phone asks about an unknown source**  
> This is normal for beta apps not from the app store. You are not doing anything malicious.  
> 1. Tap …  
> 2. Enable …  
> 3. Go back and tap the install link again  

If the submission omits this class of explanation for its platform, **deduct heavily**.

---

## Hard fail

- No user guide separate from dev README → **max 3/15** regardless of README quality  
- Install steps require unexplained developer tools with no alternative → **cap 5/15**
