Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & Replace(WScript.ScriptFullName, "open_app_hidden.vbs", "run_app.bat") & chr(34), 0
Set WshShell = Nothing
