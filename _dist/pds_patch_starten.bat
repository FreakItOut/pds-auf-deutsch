@echo off
rem PANZER DRAGOON SAGA - Deutsche Fassung: GUI starten
rem (nur privater Gebrauch; Details: ANLEITUNG.txt)
setlocal
where pythonw >nul 2>nul
if not errorlevel 1 (
  start "PDS GUI" pythonw "%~dp0pds_deutsch_patcher_gui.py"
  exit /b
)
where pyw >nul 2>nul
if not errorlevel 1 (
  start "PDS GUI" pyw "%~dp0pds_deutsch_patcher_gui.py"
  exit /b
)
where python >nul 2>nul
if not errorlevel 1 (
  start "PDS GUI" python "%~dp0pds_deutsch_patcher_gui.py"
  echo Hinweis: pythonw/pyw fehlt; es startet mit Fenster der Konsole.
  exit /b
)
echo Python wurde nicht gefunden. Bitte Python installieren.
echo Download: https://www.python.org/downloads/
pause
