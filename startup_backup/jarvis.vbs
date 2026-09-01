' JARVIS Autostart - Silent Background
' Start via BAT yang set env vars dengan benar
Dim WshShell
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """C:\Users\arija\jarvis-dashboard\start-jarvis.bat""", 0, False
Set WshShell = Nothing
