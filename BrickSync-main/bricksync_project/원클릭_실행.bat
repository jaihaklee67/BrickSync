@echo off
:: [자동 권한 상승 시스템] 현재 실행 권한이 관리자 권한인지 검사
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :AdminConfirmed
) else (
    echo.
    echo =======================================================
    echo   [알림] 브릭싱크-포트나이트 연동을 위해 권한 승인이 필요합니다.
    echo   화면에 나타나는 권한 요청 팝업에서 [예]를 눌러주세요.
    echo =======================================================
    echo.
    goto :RequestAdmin
)

:RequestAdmin
    :: 임시 스크립트를 생성하여 관리자(runas) 모드로 본 배치파일 재실행
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0""", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:AdminConfirmed
cd /d "%~dp0"
chcp 65001 >nul
title 레고 스파이크 컨트롤러 서버
color 0B
echo =======================================================
echo.
echo     [ 원클릭 레고 스파이크 컨트롤러 자동 실행 ]
echo.
echo =======================================================
echo.
echo 1. 좀비 프로세스 정리 및 포트 확보 중...
echo [필수 패키지 자동 설치 확인 중...]
py -m pip install -q aiohttp pydirectinput
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
timeout /T 1 /NOBREAK >nul

echo 2. 백그라운드 브릿지 서버를 가동합니다 (server.py)...
echo    (※주의※ 게임하는 동안 이 까만 창을 절대 끄지 마시고, 최소화 시켜두시면 됩니다!)
echo.
:: 백그라운드 서버 실행 (별도 윈도우 미생성 대신 최소화 창으로 실행)
set PYTHONIOENCODING=utf-8
start "BrickSync_Server" cmd /k "py -u bridge_server\server.py"

:: 서버가 뜰 때까지 2초 대기
timeout /T 2 /NOBREAK >nul

echo.
echo 3. 인터넷 페이지(브릭싱크 워크스페이스)를 엽니다...
start "" "http://localhost:8000/app.html"

echo.
echo 모든 준비가 완료되었습니다! 
echo 인터넷 창에서 [1. 허브 연결]을 클릭하고 바로 흔들어보세요!
echo.
echo.
:: 창이 닫히면 파이썬 프로세스도 종료되므로 창 유지
pause
