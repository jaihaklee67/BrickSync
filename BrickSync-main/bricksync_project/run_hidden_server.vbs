Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\PC\Desktop\Anti\bricksync_project"
WshShell.Run "cmd /c ""chcp 65001 && py bridge_server\server.py""", 0, False
