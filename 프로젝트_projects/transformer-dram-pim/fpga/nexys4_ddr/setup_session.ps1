<#
현재 PowerShell 창에서만 Python과 Icarus를 찾도록 PATH를 준비한다.
관리자 권한, Windows 시스템 PATH 변경, 학습 재실행은 필요하지 않다.
다른 PC에서는 실제 설치 위치를 -PythonPath / -IcarusBin으로 지정한다.
#>
param(
    [string]$PythonPath = (Get-Command python -ErrorAction Stop).Source,
    [string]$IcarusBin = 'C:/iverilog/bin'
)
$ErrorActionPreference='Stop'
if (-not (Test-Path -LiteralPath $PythonPath -PathType Leaf)) {
    throw 'Python 실행파일이 없습니다. 설치된 python.exe의 절대 경로를 -PythonPath로 지정하세요.'
}
if (-not (Test-Path -LiteralPath (Join-Path $IcarusBin 'iverilog.exe') -PathType Leaf)) {
    throw 'Icarus가 없습니다. 설치된 iverilog.exe/vvp.exe 폴더를 -IcarusBin으로 지정하세요.'
}
$taskPythonDir=Split-Path -Parent $PythonPath
$env:PYTHONIOENCODING='utf-8'
# Windows PowerShell 5.1도 Python의 UTF-8 한글 출력을 같은 문자로 읽도록 맞춘다.
[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$OutputEncoding=[Console]::OutputEncoding
$env:PATH=$taskPythonDir+';'+$IcarusBin+';'+$env:PATH
$taskVendor=Join-Path $PSScriptRoot '../../tools/vendor'
if (Test-Path -LiteralPath $taskVendor -PathType Container) {
    $taskVendor=(Resolve-Path -LiteralPath $taskVendor).Path
    if ($env:PYTHONPATH) { $env:PYTHONPATH=$taskVendor+';'+$env:PYTHONPATH }
    else { $env:PYTHONPATH=$taskVendor }
}
Write-Output ('현재 창 Python: '+(Get-Command python).Source)
Write-Output ('현재 창 Icarus: '+(Get-Command iverilog).Source)
Write-Output '설정은 이 창에서만 유지되며 Windows 시스템 환경변수는 바꾸지 않습니다.'
