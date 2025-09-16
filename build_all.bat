@echo off
cls
echo ====================================================
echo    Build Completo do OperaLote 4.0
echo ====================================================
echo.

REM Gera o executável
echo [1/2] Gerando o executável...
call build_exe.bat

if %errorlevel% neq 0 (
    echo.
    echo Erro ao gerar o executável!
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Gerando o instalador...
call build_installer.bat

if %errorlevel% neq 0 (
    echo.
    echo Erro ao gerar o instalador!
    pause
    exit /b %errorlevel%
)

echo.
echo ====================================================
echo    Build concluído com sucesso!
echo ====================================================
echo Executável: dist\OperaLote4.0.exe
echo Instalador: output\install\operalote4.exe
echo ====================================================
pause