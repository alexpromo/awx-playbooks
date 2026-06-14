$interval = 1
$cpuCount = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors

$p1 = Get-Process | Select-Object Id, CPU
Start-Sleep -Seconds $interval
$p2 = Get-Process | Select-Object Id, CPU, ProcessName, WorkingSet

$result = @()

foreach ($proc2 in $p2) {
    $proc1 = $p1 | Where-Object { $_.Id -eq $proc2.Id }

    if ($proc1) {
        $cpu_delta = $proc2.CPU - $proc1.CPU

        if ($cpu_delta -gt 0) {
            $cpu_percent = ($cpu_delta / $interval) * 100 / $cpuCount

            $result += [PSCustomObject]@{
                name   = $proc2.ProcessName + ".exe"
                cpu    = [Math]::Round($cpu_percent,2)
                memory = $proc2.WorkingSet
            }
        }
    }
}

$result | Sort-Object cpu -Descending | Select-Object -First 5 | ConvertTo-Json -Depth 3
