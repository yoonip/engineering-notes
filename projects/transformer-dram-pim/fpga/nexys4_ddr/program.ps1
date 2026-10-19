<#
실제 Nexys 4 DDR를 연결한 사용자가 실행하는 JTAG 구성 입구다.
기본: powershell -ExecutionPolicy Bypass -File fpga/nexys4_ddr/program.ps1
32-token: 위 명령 뒤에 -Context 32 -CacheStorage distributed 를 붙인다.
원본 성공 report와 bit 해시를 확인하고 영문 임시 폴더로 복사한 뒤 Vivado를 실행한다.
실제 연결된100T가 정확히 한 대인지 Tcl이 확인한다. SPI flash를 쓰지는 않는다.
이 스크립트는 작성만 했으며 이 프로젝트에서 실물 programming을 수행하지 않았다.
#>
param(
    [ValidateRange(1,32)][int]$Context=8,
    [ValidateSet('registers','distributed')][string]$CacheStorage='registers',
    [string]$Vivado='C:/Xilinx/Vivado/2024.1/bin/vivado.bat'
)
$ErrorActionPreference='Stop'
$taskRepo=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$taskFolder=if ($Context -eq 8) {'board'} else {"board_context$Context"}
if ($CacheStorage -eq 'distributed') { $taskFolder += '_distributed' }
$taskBoard=Join-Path $taskRepo ('build/nexys4_ddr/'+$taskFolder)
$taskResult=Get-Content -LiteralPath (Join-Path $taskBoard 'result.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$taskLocation=Get-Content -LiteralPath (Join-Path $taskBoard 'build_location.json') -Raw -Encoding UTF8 | ConvertFrom-Json
if ($taskLocation.vivado_exit_code -ne 0) { throw '최근 빌드가 실패했습니다. 성공한 새 구현 결과를 먼저 확인하세요.' }
if ($taskResult.device -ne 'xc7a100tcsg324-1' -or $taskResult.max_context -ne $Context) {
    throw '요약의 장치/context가 선택한 파일과 다릅니다.'
}
if ($taskResult.timing.WNS_ns -lt 0 -or $taskResult.timing.WHS_ns -lt 0 -or $taskResult.drc.error_count -ne 0) {
    throw 'timing/DRC 조건을 통과한 bitstream이 필요합니다.'
}
$taskBit=Join-Path $taskBoard 'nexys4_ddr_gpt.bit'
if ((Get-FileHash -LiteralPath $taskBit -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskResult.bitstream.sha256) {
    throw 'bitstream SHA256이 성공 보고서와 다릅니다.'
}
$taskStage=Join-Path ([System.IO.Path]::GetTempPath()) ('nexys_program_'+[guid]::NewGuid().ToString('N'))
if ($taskStage -match '[^\x00-\x7F]') { throw 'TEMP가 한글 경로입니다. 영문 TEMP 환경에서 실행하세요.' }
New-Item -ItemType Directory -Path $taskStage -Force | Out-Null
Copy-Item -LiteralPath $taskBit -Destination (Join-Path $taskStage 'nexys4_ddr_gpt.bit')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'program_device.tcl') -Destination $taskStage
$taskPreviousBit=$env:NEXYS_BITFILE
try {
    $env:NEXYS_BITFILE=(Join-Path $taskStage 'nexys4_ddr_gpt.bit').Replace('\','/')
    $taskVivadoArgs=@('-mode','batch','-source',(Join-Path $taskStage 'program_device.tcl'),
        '-log',(Join-Path $taskStage 'program.log'),'-journal',(Join-Path $taskStage 'program.jou'))
    & $Vivado @taskVivadoArgs
    if ($LASTEXITCODE -ne 0) { throw "JTAG 구성 실패: $taskStage/program.log" }
} finally {
    $env:NEXYS_BITFILE=$taskPreviousBit
}
Write-Output 'JTAG 구성 명령이 완료됐습니다. host.py --port 실제COM번호 로65개 점수 대조를 수행하세요.'
Write-Output "구성 로그: $taskStage/program.log"
