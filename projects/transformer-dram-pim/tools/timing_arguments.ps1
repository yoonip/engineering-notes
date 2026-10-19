<#
SDF 재실행 인수를 만드는 순수 helper다. Python/Vivado를 실행하거나 결과를 쓰지 않는다.
Transport0는 짧은 pulse를 전달하는 0 정책이고, Inertial100은 별도 필터 실험이다.
timing check·specify·SDF 배선 지연은 두 정책 모두 유지한다.
#>
function Get-TaskTimingArguments {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [ValidateSet(8,32)] [int]$Context,
        [Parameter(Mandatory=$true)]
        [ValidateSet('slow','fast')] [string]$Corner,
        [ValidateSet('Transport0','Inertial100')] [string]$TimingPulsePolicy='Transport0',
        [Parameter(Mandatory=$true)] [string]$Stage
    )
    $taskDelay=if ($Corner -eq 'slow') {'max'} else {'min'}
    $taskBoard=if ($Context -eq 8) {'board'} else {'board_context32_distributed'}
    $taskBaud=if ($Context -eq 8) {115200} else {57600}
    $taskPulseLimit=if ($TimingPulsePolicy -eq 'Transport0') {'0'} else {'100'}
    $taskOutput=if ($TimingPulsePolicy -eq 'Transport0') {
        'build/nexys4_ddr/timing_netlist'+$Context+'_'+$Corner+'_'+$taskDelay
    } else {
        'build/nexys4_ddr/timing_netlist'+$Context+'_inertial100_'+$Corner+'_'+$taskDelay
    }
    # 각 path/interconnect reject/error와 O2를 명시하여 기존 kernel과 혼동하지 않는다.
    [string[]]@('fpga/nexys4_ddr/verify_timing_netlist.py','--checkpoint',
        ('build/nexys4_ddr/'+$taskBoard+'/routed.dcp'),'--stage',$Stage,
        '--host-baud',[string]$taskBaud,'--corner',$Corner,'--delay-mode',$taskDelay,
        '--lexical-safe-instance-names','--pulse-reject-limit',$taskPulseLimit,
        '--pulse-error-limit',$taskPulseLimit,'--interconnect-pulse-reject-limit',$taskPulseLimit,
        '--interconnect-pulse-error-limit',$taskPulseLimit,'--optimization','2',
        '--timeout','21600','--output-dir',$taskOutput)
}

function Get-TaskTimingStepName {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)] [ValidateSet(8,32)] [int]$Context,
        [Parameter(Mandatory=$true)] [ValidateSet('slow','fast')] [string]$Corner,
        [ValidateSet('Transport0','Inertial100')] [string]$TimingPulsePolicy='Transport0'
    )
    $taskDelay=if ($Corner -eq 'slow') {'max'} else {'min'}
    if ($TimingPulsePolicy -eq 'Transport0') {
        'timing'+$Context+'_'+$Corner+'_'+$taskDelay
    } else {
        'timing'+$Context+'_inertial100_'+$Corner+'_'+$taskDelay
    }
}
