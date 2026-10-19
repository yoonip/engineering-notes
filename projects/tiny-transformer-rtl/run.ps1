param(
    [string]$Iverilog = "",
    [string]$Prompt = "",
    [string]$City = "서울",
    [string]$TargetDate = "",
    [ValidateRange(1,100)][int]$RainProbabilityThreshold = 50
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

# Windows PowerShell 5 can default to older TLS versions. Require TLS 1.2 when
# this setting is available; never disable certificate verification.
if ($PSVersionTable.PSEdition -eq "Desktop") {
    try {
        [Net.ServicePointManager]::SecurityProtocol =
            [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
    } catch {
        # Newer .NET builds may manage TLS independently of ServicePointManager.
    }
}

# Find the open-source simulator. Icarus is used for simulation, not training.
$candidatePaths = @()
if ($Iverilog) { $candidatePaths += $Iverilog }
$candidatePaths += @(
    (Join-Path $root "tools\iverilog\bin\iverilog.exe"),
    (Join-Path $root "work\tools\iverilog\bin\iverilog.exe"),
    "C:\iverilog\bin\iverilog.exe"
)
$compiler = $null
foreach ($candidate in $candidatePaths) {
    if (Test-Path -LiteralPath $candidate) {
        $compiler = (Resolve-Path -LiteralPath $candidate).Path
        break
    }
}
if (-not $compiler) {
    $command = Get-Command iverilog -ErrorAction SilentlyContinue
    if ($command) { $compiler = $command.Source }
}
if (-not $compiler) {
    throw "Icarus Verilog was not found. Install it, add it to PATH, or pass -Iverilog <path-to-iverilog.exe>."
}
$vvp = Join-Path (Split-Path -Parent $compiler) "vvp.exe"
if (-not (Test-Path -LiteralPath $vvp)) { throw "Could not find vvp.exe beside the compiler: $compiler" }

$buildDir = Join-Path $root "work\build"
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
$simulator = Join-Path $buildDir "tiny_gpt.vvp"
$testbench = Join-Path $root "tb\tb_tiny_gpt.sv"
$runtimeArgs = @()

if ($Prompt) {
    # Tiny host-side tokenizer: supported Korean weather words and common
    # English equivalents map to one of two semantic query IDs. This is a
    # transparent rule table, not an unrestricted Korean language model.
    $rainTerms = @(
        "비", "강수", "우산", "장마", "rain", "rainfall", "rain chance",
        "rain probability", "precipitation", "precipitation probability", "umbrella"
    )
    $clearTerms = @("맑", "쾌청", "sunny", "clear", "sunshine")
    $weatherTerms = @("날씨", "weather", "기상")
    $queryId = 0
    foreach ($term in $rainTerms) { if ($Prompt.IndexOf($term, [StringComparison]::OrdinalIgnoreCase) -ge 0) { $queryId = 2; break } }
    if ($queryId -eq 0) {
        foreach ($term in $clearTerms) { if ($Prompt.IndexOf($term, [StringComparison]::OrdinalIgnoreCase) -ge 0) { $queryId = 3; break } }
    }
    $isGenericWeatherQuestion = $false
    foreach ($term in $weatherTerms) {
        if ($Prompt.IndexOf($term, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
            $isGenericWeatherQuestion = $true
            break
        }
    }
    if (($queryId -eq 0) -and $isGenericWeatherQuestion) { $queryId = 2 }
    if ($queryId -eq 0) {
        throw "No supported weather keyword found. Try words such as 비/강수/우산 or 맑/쾌청."
    }

    # Relative-date convenience: a prompt containing 내일 selects tomorrow;
    # otherwise today is used unless -TargetDate is supplied explicitly.
    if ($TargetDate) {
        $date = [DateTime]::ParseExact($TargetDate, "yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)
    } elseif ($Prompt.Contains("내일")) {
        $date = (Get-Date).Date.AddDays(1)
    } else {
        $date = (Get-Date).Date
    }
    $dateKey = $date.ToString("yyyy-MM-dd", [Globalization.CultureInfo]::InvariantCulture)

    # Open-Meteo geocoding resolves the city to coordinates. The forecast API
    # returns that city's daily maximum precipitation probability. These two
    # host-side API calls provide facts; the Transformer itself remains RTL.
    $encodedCity = [Uri]::EscapeDataString($City)
    $geoUrl = "https://geocoding-api.open-meteo.com/v1/search?name=$encodedCity&count=1&language=ko&format=json&countryCode=KR"
    try {
        $geo = Invoke-RestMethod -Uri $geoUrl -TimeoutSec 20
        if (-not $geo.results -or $geo.results.Count -eq 0) { throw "City was not found in South Korea: $City" }
        $location = $geo.results[0]
        $lat = ([double]$location.latitude).ToString([Globalization.CultureInfo]::InvariantCulture)
        $lon = ([double]$location.longitude).ToString([Globalization.CultureInfo]::InvariantCulture)
        $timezone = [Uri]::EscapeDataString([string]$location.timezone)
        $forecastUrl = "https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lon&daily=precipitation_probability_max&timezone=$timezone&forecast_days=7"
        $forecast = Invoke-RestMethod -Uri $forecastUrl -TimeoutSec 20
    } catch {
        throw "Weather lookup failed. Check the Internet connection, city, and date. Provider error: $($_.Exception.Message)"
    }

    $dateIndex = [Array]::IndexOf([string[]]$forecast.daily.time, $dateKey)
    if ($dateIndex -lt 0) { throw "The selected date $dateKey is outside the returned seven-day forecast." }
    $probabilityValue = $forecast.daily.precipitation_probability_max[$dateIndex]
    if ($null -eq $probabilityValue) { throw "The forecast provider did not return precipitation probability for $dateKey." }
    $probability = [int][Math]::Round([double]$probabilityValue, 0)
    if ($probability -ge $RainProbabilityThreshold) { $forecastId = 4; $level = "HIGH" }
    else { $forecastId = 5; $level = "LOW" }

    $testbench = Join-Path $root "tb\tb_query.sv"
    $runtimeArgs = @("+QUERY_ID=$queryId", "+FORECAST_ID=$forecastId")
    Write-Host "입력 문장: $Prompt"
    Write-Host "분류 ID: $queryId; 지역: $($location.name), $($location.country); 날짜: $dateKey"
    Write-Host "Open-Meteo 일 최대 강수확률: $probability% (판정 기준 $RainProbabilityThreshold%, category $level)"
} else {
    Write-Host "Running four deterministic, offline forecast-bin tests."
}

& $compiler -g2012 -s tb_tiny_gpt -o $simulator `
    (Join-Path $root "rtl\tiny_gpt.sv") `
    $testbench
if ($LASTEXITCODE -ne 0) { throw "Icarus compilation failed with exit code $LASTEXITCODE" }

& $vvp $simulator @runtimeArgs
if ($LASTEXITCODE -ne 0) { throw "Simulation failed with exit code $LASTEXITCODE" }
