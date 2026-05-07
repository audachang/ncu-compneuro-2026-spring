function Stop-Streamlit {
    param([int]$Port = 8501)
    $pids = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique |
        Where-Object { $_ -ne 0 }
    if (-not $pids) {
        Write-Host "No process listening on port $Port"
        return
    }
    foreach ($processId in $pids) {
        taskkill /PID $processId /T /F | Out-Null
        Write-Host "Killed PID $processId (and child processes) on port $Port"
    }
}
