param(
    [Parameter(Mandatory = $true)]
    [string]$Model,

    [Parameter(Mandatory = $false)]
    [ValidateSet("S1", "S2", "S3")]
    [string]$Tier = "S1",

    [Parameter(Mandatory = $false)]
    [string]$Deliverables = ""
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$engine = Join-Path $root "scoring_engine\scoring_engine.py"
$questions = Join-Path $root "runs\${Model}_${Tier}_questions.txt"
$packet = Join-Path $root "${Tier}_Job_Packet.md"
$output = Join-Path $root "runs\${Model}_${Tier}_inquiry_score.json"

if (-not (Test-Path $questions)) {
    Write-Error "Questions file not found: $questions"
    Write-Host "Save model questions to: runs\${Model}_${Tier}_questions.txt"
    exit 1
}

if ([string]::IsNullOrWhiteSpace($Deliverables)) {
    $Deliverables = Join-Path $root "runs\_empty"
    New-Item -ItemType Directory -Force -Path $Deliverables | Out-Null
}

if (-not (Test-Path $packet)) {
    Write-Error "Packet not found: $packet"
    exit 1
}

Write-Host "Scoring $Model on $Tier..."
Write-Host "  Questions:    $questions"
Write-Host "  Deliverables: $Deliverables"
Write-Host "  Output:       $output"

python $engine `
    --tier $Tier `
    --questions $questions `
    --deliverables $Deliverables `
    --packet $packet `
    --output $output

if ($LASTEXITCODE -eq 0) {
    Write-Host "Done. Open: $output"
}
