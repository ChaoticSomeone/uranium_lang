clear
cd C:\Users\deniz\OneDrive\Dokumente\Coding\Uranium_Lang
py main.py
./out/main.exe
echo ""
[string]$exitMsg = "Uranium Lang: Process finished with exit code {0}" -f $LastExitCode
Write-Host $exitMsg -ForegroundColor Red