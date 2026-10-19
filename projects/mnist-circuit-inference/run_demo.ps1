param(
    [string]$PythonExe = 'python',
    [string]$NgspiceExe = '',
    [switch]$Regenerate,
    [switch]$Retrain
)
$ErrorActionPreference = 'Stop'
if ($Retrain) {
    & $PythonExe (Join-Path $PSScriptRoot 'prepare_demo.py')
    if ($LASTEXITCODE -ne 0) { throw 'Training failed' }
    $Regenerate = $true
}
if ($Regenerate) {
    & $PythonExe (Join-Path $PSScriptRoot 'export_circuit.py')
    if ($LASTEXITCODE -ne 0) { throw 'Circuit export failed' }
}
if ($NgspiceExe) {
    & $PythonExe (Join-Path $PSScriptRoot 'verify_run.py') --run-spice --ngspice $NgspiceExe
} else {
    & $PythonExe (Join-Path $PSScriptRoot 'verify_run.py') --run-spice
}
if ($LASTEXITCODE -ne 0) { throw 'SPICE verification failed' }
Write-Output 'Completed: verified_execution.json'
