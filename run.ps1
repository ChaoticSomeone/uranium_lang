Clear-Host
Write-Host "Running the Uranium Compiler..." -ForegroundColor Green
py uranc.py
if ($LastExitCode -eq 0) {
    Write-Host "`nRunning the final executeable..." -ForegroundColor Green
    ./_out/main.exe
    Write-Host ""
    [string]$exitMsg = "Uranium Lang: Process finished with exit code {0}" -f $LastExitCode
    Write-Host $exitMsg -ForegroundColor Red
} else {
    Write-Host "Uranium Lang: Compilation process failed! See above for errors" -ForegroundColor Red
}

