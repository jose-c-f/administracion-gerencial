@echo off
REM regenerate_summary.cmd - Rebuild summary.pdf and/or summary.mp3 from summary.html
REM
REM Usage:
REM   regenerate_summary.cmd          -> regenerates both the PDF and the MP3
REM   regenerate_summary.cmd pdf      -> only summary.pdf   (a few seconds)
REM   regenerate_summary.cmd mp3      -> only summary.mp3   (about 15 minutes, needs internet)
REM   regenerate_summary.cmd mp3 es-MX-JorgeNeural   -> MP3 with another voice (see convert.py --list-voices)
REM
REM Requirements: Python 3 with edge-tts (python -m pip install --user edge-tts),
REM Google Chrome or Microsoft Edge for the PDF, convert.py and summary_text.py in this folder.

setlocal
cd /d "%~dp0"

set "WHAT=%~1"
if "%WHAT%"=="" set "WHAT=all"
set "VOICE=%~2"
if "%VOICE%"=="" set "VOICE=es-AR-TomasNeural"

if not exist "summary.html" (
    echo summary.html not found in %CD%
    exit /b 1
)

set "VALID="
if /i "%WHAT%"=="all" set "VALID=1"
if /i "%WHAT%"=="pdf" set "VALID=1"
if /i "%WHAT%"=="mp3" set "VALID=1"
if not defined VALID (
    echo Unknown option "%WHAT%". Use: pdf, mp3 or nothing for both.
    exit /b 1
)

set /a FAILED=0

if /i "%WHAT%"=="all" call :pdf
if /i "%WHAT%"=="pdf" call :pdf
if /i "%WHAT%"=="all" call :mp3
if /i "%WHAT%"=="mp3" call :mp3

echo.
if %FAILED% gtr 0 (
    echo Finished with %FAILED% errors.
    exit /b 1
)
echo Finished OK.
exit /b 0


:pdf
echo === summary.pdf ===
set "BROWSER="
for %%B in (
    "%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    "%LocalAppData%\Google\Chrome\Application\chrome.exe"
    "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
    "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
) do if not defined BROWSER if exist %%B set "BROWSER=%%~B"
if not defined BROWSER (
    echo   Chrome or Edge not found; cannot render the PDF.
    set /a FAILED+=1
    goto :eof
)
echo   Using %BROWSER%
if exist "summary.pdf" del /q "summary.pdf"
"%BROWSER%" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=15000 --print-to-pdf="%CD%\summary.pdf" "file:///%CD:\=/%/summary.html" 2>nul
if exist "summary.pdf" (
    for %%F in ("summary.pdf") do echo   summary.pdf written (%%~zF bytes^)
) else (
    echo   FAILED: summary.pdf was not created.
    set /a FAILED+=1
)
goto :eof


:mp3
echo === summary.mp3 ===
python summary_text.py summary.html -o summary-audio.txt
if errorlevel 1 (
    echo   FAILED: could not extract the text from summary.html
    set /a FAILED+=1
    goto :eof
)
if exist "summary.mp3" del /q "summary.mp3"
python convert.py summary-audio.txt -v "%VOICE%" -o summary.mp3
if errorlevel 1 (
    echo   FAILED: text-to-speech did not finish.
    set /a FAILED+=1
) else (
    for %%F in ("summary.mp3") do echo   summary.mp3 written (%%~zF bytes^)
)
del /q "summary-audio.txt" 2>nul
goto :eof
