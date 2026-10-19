$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$script = Join-Path $root "train_numpy.py"
if (-not (Test-Path -LiteralPath $script)) {
    $script = Join-Path $root "work\train_numpy.py"
}
if (-not (Test-Path -LiteralPath $script)) { throw "train_numpy.py was not found beside train.ps1 or under work\." }

$python = Get-Command python -ErrorAction SilentlyContinue
$launcher = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -c "import numpy"
    if ($LASTEXITCODE -ne 0) {
        throw "NumPy is required only for retraining. Install it with: python -m pip install numpy"
    }
    & $python.Source $script
} elseif ($launcher) {
    & $launcher.Source -3 -c "import numpy"
    if ($LASTEXITCODE -ne 0) {
        throw "NumPy is required only for retraining. Install it with: py -3 -m pip install numpy"
    }
    & $launcher.Source -3 $script
} else {
    throw "Python 3 was not found. Install Python 3 to retrain; pre-trained RTL inference does not need Python."
}
if ($LASTEXITCODE -ne 0) { throw "Training or SystemVerilog weight export failed." }

Write-Host "Updated rtl\tiny_gpt.sv and weights\trained_weights_q8.json"
