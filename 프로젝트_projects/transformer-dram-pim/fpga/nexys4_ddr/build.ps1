<#
Nexys 4 DDR용 실제 합성·배치·배선·bitstream 자동화.
Vivado 2024.1이 한글 원본 경로에서 TclStackFree로 중단되고 동일 파일이
영문 경로에서는 진행한 관찰에 따라, 원본은 유지하고 임시 영문 폴더에서 빌드한다.
보드에 쓰는 작업은 하지 않는다. JTAG programming은 program_device.tcl로 별도 실행한다.
#>
param(
    [string]$Vivado = 'C:/Xilinx/Vivado/2024.1/bin/vivado.bat',
    [string]$StageRoot = [System.IO.Path]::GetTempPath(),
    [ValidateRange(1,32)][int]$Context = 8,
    [ValidateSet('registers','distributed')][string]$CacheStorage = 'registers',
    # 0은설정에맞는값을자동선택한다. 32-token distributed는2.5MHz, 나머지는기존5MHz다.
    # 명시값은실제MMCM generic으로전달되며요약JSON의숫자만바꾸는옵션이아니다.
    [ValidateSet(0,2500000,5000000)][int]$CoreClockHz = 0,
    # 0은실제core clock에맞춰2.5MHz→57600,5MHz→115200을선택한다.
    # 두자동설정은UART정수divider43으로동작한다. PC host도동일baud를사용한다.
    [ValidateSet(0,57600,115200)][int]$HostBaud = 0
)
$ErrorActionPreference = 'Stop'
# 명시인수가0일때만자동값을계산한다. 사용자가선택한설정은stage와collector에똑같이전달한다.
# 실제회로파라미터·타이밍제약의자동clock도출·통신bit길이·결과메타데이터가같아야한다.
$taskCoreClockHz = if ($CoreClockHz -ne 0) { $CoreClockHz } elseif ($Context -eq 32 -and $CacheStorage -eq 'distributed') { 2500000 } else { 5000000 }
$taskHostBaud = if ($HostBaud -ne 0) { $HostBaud } elseif ($taskCoreClockHz -eq 2500000) { 57600 } else { 115200 }
$taskRepo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../..')).Path
$taskOutputName = if ($Context -eq 8) { 'board' } else { "board_context$Context" }
if ($CacheStorage -eq 'distributed') { $taskOutputName += '_distributed' }
$taskOut = Join-Path $taskRepo ('build/nexys4_ddr/' + $taskOutputName)
$taskStage = Join-Path $StageRoot ('nexys_gpt_' + [guid]::NewGuid().ToString('N'))
if ($taskStage -match '[^\x00-\x7F]') {
    throw '임시 빌드 경로는 영문이어야 합니다. -StageRoot 옵션으로 쓰기 가능한 영문 경로를 지정하세요.'
}
if (-not (Test-Path -LiteralPath $Vivado -PathType Leaf)) {
    throw "Vivado 실행 파일이 없습니다: $Vivado"
}
# 합성/배선 checkpoint와 tool 중간 파일을 저장할 여유가 필요하다.
# 저장 공간 부족을 회로 실패로 오해하지 않도록 장시간 실행 전에 확인한다.
$taskDrive = [System.IO.Path]::GetPathRoot([System.IO.Path]::GetFullPath($taskStage))
$taskFreeBytes = (New-Object System.IO.DriveInfo($taskDrive)).AvailableFreeSpace
if ($taskFreeBytes -lt 10GB) {
    throw '빌드용 드라이브에 10GB 이상의 여유를 확보하거나 -StageRoot로 다른 영문 경로를 지정하세요.'
}
$taskWeightFiles = @(Get-ChildItem -LiteralPath (Join-Path $taskRepo 'build/vivado_weights') -Filter '*.mem')
if ($taskWeightFiles.Count -ne 36) {
    throw '먼저 python tools/export_vivado_weights.py --output build/vivado_weights 를 실행하세요. 36개 .mem 파일이 필요합니다.'
}
New-Item -ItemType Directory -Force -Path (Join-Path $taskStage 'rtl'),
    (Join-Path $taskStage 'fpga/nexys4_ddr'),
    (Join-Path $taskStage 'build/nexys4_ddr/board/weights'), $taskOut | Out-Null
$taskSources = @('dram_pim_pu_synth.sv','dram_pim_vmm_bank.sv',
    'transformer_gpt_kvcache_seq.sv','gpt_kvcache_rom_board_top.sv',
    'nexys4_ddr_uart.sv','nexys4_ddr_gpt_uart_bridge.sv','nexys4_ddr_gpt_top.sv')
foreach ($taskSource in $taskSources) {
    Copy-Item -LiteralPath (Join-Path $taskRepo ('rtl/' + $taskSource)) -Destination (Join-Path $taskStage 'rtl')
}
foreach ($taskControl in @('build_bitstream.tcl','nexys4_ddr_gpt.xdc')) {
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot $taskControl) -Destination (Join-Path $taskStage 'fpga/nexys4_ddr')
}
foreach ($taskWeight in $taskWeightFiles) {
    Copy-Item -LiteralPath $taskWeight.FullName -Destination (Join-Path $taskStage 'build/nexys4_ddr/board/weights')
}
$taskOldRepoEnv = $env:TRANSFORMER_REPO
$taskOldContextEnv = $env:NEXYS_MAX_CONTEXT
$taskOldCacheEnv = $env:NEXYS_FLAT_CACHE
$taskOldClockEnv = $env:NEXYS_CORE_CLOCK_HZ
$taskOldBaudEnv = $env:NEXYS_HOST_BAUD
try {
    $env:TRANSFORMER_REPO = $taskStage.Replace('\','/')
    $env:NEXYS_MAX_CONTEXT = [string]$Context
    $env:NEXYS_FLAT_CACHE = if ($CacheStorage -eq 'distributed') { '1' } else { '0' }
    # Vivado Tcl은이두값을top의CORE_CLOCK_HZ/HOST_BAUD generic으로넘긴다.
    # 환경변수는이번자식프로세스의설정이며finally에서원래세션값으로복원한다.
    $env:NEXYS_CORE_CLOCK_HZ = [string]$taskCoreClockHz
    $env:NEXYS_HOST_BAUD = [string]$taskHostBaud
    Write-Output "실제 빌드 설정: context=$Context, cache=$CacheStorage, clock=$taskCoreClockHz Hz, host baud=$taskHostBaud"
    & $Vivado -mode batch -source (Join-Path $taskStage 'fpga/nexys4_ddr/build_bitstream.tcl') `
        -log (Join-Path $taskStage 'vivado.log') -journal (Join-Path $taskStage 'vivado.jou')
    $taskExitCode = $LASTEXITCODE
} finally {
    $env:TRANSFORMER_REPO = $taskOldRepoEnv
    $env:NEXYS_MAX_CONTEXT = $taskOldContextEnv
    $env:NEXYS_FLAT_CACHE = $taskOldCacheEnv
    $env:NEXYS_CORE_CLOCK_HZ = $taskOldClockEnv
    $env:NEXYS_HOST_BAUD = $taskOldBaudEnv
    # 실패해도 진단 로그와 이미 완료된 보고서는 보존한다. 삭제나 이동은 하지 않는다.
    foreach ($taskLog in @('vivado.log','vivado.jou')) {
        $taskLogPath = Join-Path $taskStage $taskLog
        if (Test-Path -LiteralPath $taskLogPath) {
            Copy-Item -LiteralPath $taskLogPath -Destination (Join-Path $taskOut $taskLog) -Force
        }
    }
    $taskBuiltDir = Join-Path $taskStage 'build/nexys4_ddr/board'
    foreach ($taskArtifact in Get-ChildItem -LiteralPath $taskBuiltDir -File) {
        Copy-Item -LiteralPath $taskArtifact.FullName -Destination $taskOut -Force
    }
    # 실제 합성한 소스와 고정 가중치를 함께 보존한다. 나중에 원본이 수정돼도
    # bitstream을 만든 당시의 입력을 확인할 수 있으며 다른 PC의 재현에도 사용한다.
    foreach ($taskArchive in @('weights','project')) {
        $taskArchivePath = Join-Path $taskBuiltDir $taskArchive
        if (Test-Path -LiteralPath $taskArchivePath) {
            Copy-Item -LiteralPath $taskArchivePath -Destination $taskOut -Recurse -Force
        }
    }
    $taskSourceSnapshot = Join-Path $taskOut 'source_snapshot'
    New-Item -ItemType Directory -Path $taskSourceSnapshot -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $taskStage 'rtl') -Destination $taskSourceSnapshot -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $taskStage 'fpga') -Destination $taskSourceSnapshot -Recurse -Force
    @{ source_root=$taskRepo; ascii_stage=$taskStage; device='xc7a100tcsg324-1';
       max_context=$Context; cache_storage=$CacheStorage;
       clock_hz=$taskCoreClockHz; clock_period_ns=(1000000000.0/$taskCoreClockHz);
       host_baud=$taskHostBaud;
       physical_programming_performed=$false; vivado_exit_code=$taskExitCode } |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskOut 'build_location.json') -Encoding UTF8
}
if ($taskExitCode -ne 0) {
    throw "Vivado 빌드 실패(exit=$taskExitCode). 진단: $taskOut/vivado.log. 임시 프로젝트: $taskStage"
}
# 원본 report/.bit를 다시 읽어 새 성공 요약을 자동 갱신한다. 현재 machine의
# bundled Python은 fallback이며, 일반 Python이 PATH에 있으면 그 설치를 사용한다.
$taskPythonCommand=Get-Command python -ErrorAction SilentlyContinue
$taskPythonExe=if ($taskPythonCommand) { $taskPythonCommand.Source } else {
    Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
}
if (Test-Path -LiteralPath $taskPythonExe -PathType Leaf) {
    & $taskPythonExe (Join-Path $taskRepo 'tools/collect_nexys_result.py') --directory $taskOut `
        --context $Context --cache-storage $CacheStorage --stage $taskStage `
        --clock-hz $taskCoreClockHz --host-baud $taskHostBaud
    if ($LASTEXITCODE -ne 0) { throw '원본 bit/report를 읽는 결과 요약 검증에 실패했습니다.' }
} else {
    Write-Warning 'Python을 찾지 못해 result.json 자동 생성은 하지 못했습니다. 원본 .rpt와 .bit는 보존돼 있습니다.'
}
Write-Output "빌드 완료: $taskOut/nexys4_ddr_gpt.bit"
Write-Output "Vivado .xpr 프로젝트와 빌드 원본은 $taskStage 에 보존되어 있습니다. 실제 보드 programming은 별도입니다."
