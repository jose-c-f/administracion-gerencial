@echo off
REM convert_all.cmd - Convert every .txt file in this folder to .mp3 using txt2mp3.py
REM For each file, an existing .mp3 with the same name is deleted first.
REM
REM Usage:
REM   convert_all.cmd                    -> uses the Tomas (Argentina) voice
REM   convert_all.cmd es-MX-JorgeNeural  -> uses the voice given as argument
REM   convert_all.cmd 2                  -> uses menu number 2 from txt2mp3.py

setlocal enabledelayedexpansion
cd /d "%~dp0"

set "VOICE=%~1"
if "%VOICE%"=="" set "VOICE=es-AR-TomasNeural"

set /a OK=0
set /a FAILED=0

for %%F in (*.txt) do (
    set "OUTPUT=%%~nF.mp3"
    if exist "!OUTPUT!" (
        echo Deleting old !OUTPUT!
        del /q "!OUTPUT!"
    )
    echo Converting %%F to !OUTPUT! with voice %VOICE% ...
    python txt2mp3.py "%%F" -v "%VOICE%" -o "!OUTPUT!"
    if errorlevel 1 (
        echo   FAILED: %%F
        set /a FAILED+=1
    ) else (
        set /a OK+=1
    )
    echo.
)

echo Finished: !OK! converted, !FAILED! failed.
pause
endlocal
