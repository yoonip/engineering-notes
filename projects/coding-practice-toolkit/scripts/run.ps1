param(
    [Parameter(Mandatory=$true)][string]$Source,
    [string]$InputFile,
    [int]$TimeoutSeconds = 10,
    [switch]$BuildOnly,
    [switch]$PrepareDebugInput,
    [switch]$KeyboardInput
)
$ErrorActionPreference = 'Stop'
$workspace = Split-Path -Parent $PSScriptRoot
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$extension = [IO.Path]::GetExtension($sourcePath).ToLowerInvariant()
$sourceDir = Split-Path -Parent $sourcePath
$workspacePrefix = $workspace.TrimEnd('\') + '\'
if (-not $sourcePath.StartsWith($workspacePrefix, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Save the practice source inside the current practice workspace before running this task.'
}
$relativeSource = $sourcePath.Substring($workspacePrefix.Length)
$relativeDir = Split-Path -Parent $relativeSource
$buildRoot = Join-Path $workspace 'build'
$buildDir = if ($relativeDir) { Join-Path $buildRoot $relativeDir } else { $buildRoot }
New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
$fileName = [IO.Path]::GetFileName($sourcePath)
$inputPath = $null
if ($InputFile) {
    $inputPath = (Resolve-Path -LiteralPath $InputFile).Path
} elseif (-not $KeyboardInput) {
    $besideSource = Join-Path $sourceDir 'input.txt'
    $rootInput = Join-Path $workspace 'input.txt'
    if (Test-Path -LiteralPath $besideSource -PathType Leaf) { $inputPath = $besideSource }
    elseif (Test-Path -LiteralPath $rootInput -PathType Leaf) { $inputPath = $rootInput }
    else { throw 'Create input.txt beside the source or in the current practice workspace.' }
}
function Read-PracticeInputBytes([string]$Path) {
    [byte[]]$bytes = [IO.File]::ReadAllBytes($Path)
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191) {
        [byte[]]$cleaned = New-Object byte[] ($bytes.Length - 3)
        [Array]::Copy($bytes, 3, $cleaned, 0, $cleaned.Length)
        return ,$cleaned
    }
    return ,$bytes
}
if ($PrepareDebugInput) {
    if (-not $inputPath) { throw 'Debug file input requires input.txt.' }
    $debugInputPath = Join-Path $buildDir ($fileName + '.stdin.txt')
    [IO.File]::WriteAllBytes($debugInputPath, (Read-PracticeInputBytes $inputPath))
    Write-Host ('Input: ' + $inputPath)
}
$runtimeArgs = @()
$compilerFlags = @('-O2', '-g', '-Wall', '-Wextra')
if ($BuildOnly) { $compilerFlags = @('-O0', '-g3', '-Wall', '-Wextra', '-include', (Join-Path $PSScriptRoot 'stdin_redirect.h')) }

function Invoke-PracticeCompiler([string]$Compiler, [string]$Standard, [string]$Destination) {
    # Some MinGW linkers reject non-ASCII output paths. Only the compiler's
    # output uses a temporary ASCII filename; the final executable stays here.
    $compileRoot = if ($env:PRACTICE_BUILD_TEMP) { $env:PRACTICE_BUILD_TEMP } else { [IO.Path]::GetTempPath() }
    $compileRoot = [IO.Path]::GetFullPath($compileRoot)
    if ($compileRoot -match '[^\x00-\x7F]') {
        throw 'Set PRACTICE_BUILD_TEMP to a writable ASCII directory for the MinGW linker.'
    }
    New-Item -ItemType Directory -Path $compileRoot -Force | Out-Null
    $temporaryProgram = Join-Path $compileRoot ('practice-' + [Guid]::NewGuid().ToString('N') + '.exe')
    try {
        & $Compiler $Standard @compilerFlags $sourcePath '-o' $temporaryProgram
        if ($LASTEXITCODE -ne 0) { throw ('Compilation failed with exit code ' + $LASTEXITCODE) }
        Move-Item -LiteralPath $temporaryProgram -Destination $Destination -Force
    } finally {
        if (Test-Path -LiteralPath $temporaryProgram -PathType Leaf) {
            Remove-Item -LiteralPath $temporaryProgram -Force
        }
    }
}
switch ($extension) {
    '.c' {
        $program = Join-Path $buildDir ($fileName + '.exe')
        Invoke-PracticeCompiler 'gcc.exe' '-std=c11' $program
    }
    { $_ -in @('.cpp', '.cc', '.cxx') } {
        $program = Join-Path $buildDir ($fileName + '.exe')
        Invoke-PracticeCompiler 'g++.exe' '-std=c++17' $program
    }
    '.py' {
        $program = (Get-Command python.exe -ErrorAction Stop).Source
        $runtimeArgs = @('-X', 'utf8', $sourcePath)
    }
    default { throw 'Supported source extensions: .c, .cpp, .cc, .cxx, .py' }
}
if ($BuildOnly) { exit 0 }
if ($KeyboardInput) {
    Write-Host 'Keyboard input: if the code reads all stdin, finish with Ctrl+Z then Enter.'
    Push-Location -LiteralPath $sourceDir
    try { & $program @runtimeArgs; $programExitCode=$LASTEXITCODE }
    finally { Pop-Location }
    exit $programExitCode
}
Write-Host ('Input: ' + $inputPath)
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = $program
$processInfo.WorkingDirectory = $sourceDir
$processInfo.UseShellExecute = $false
$processInfo.CreateNoWindow = $true
$processInfo.RedirectStandardInput = $true
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.StandardOutputEncoding = New-Object System.Text.UTF8Encoding($false)
$processInfo.StandardErrorEncoding = New-Object System.Text.UTF8Encoding($false)
# Each variable argument is a file path; Windows filenames cannot contain double quotes.
$processInfo.Arguments = ($runtimeArgs | ForEach-Object { '"' + $_ + '"' }) -join ' '
$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo
[void]$process.Start()
$stdoutTask = $process.StandardOutput.ReadToEndAsync()
$stderrTask = $process.StandardError.ReadToEndAsync()
try {
    $inputBytes = Read-PracticeInputBytes $inputPath
    $writeTask = $process.StandardInput.BaseStream.WriteAsync($inputBytes, 0, $inputBytes.Length)
    if (-not $writeTask.Wait($TimeoutSeconds * 1000)) { $process.Kill(); throw 'Input write timed out.' }
    $process.StandardInput.Close()
    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        $process.Kill()
        throw ('Time limit exceeded: ' + $TimeoutSeconds + ' seconds')
    }
    $process.WaitForExit()
    [Console]::Out.Write($stdoutTask.Result)
    [Console]::Error.Write($stderrTask.Result)
    exit $process.ExitCode
} finally { $process.Dispose() }
