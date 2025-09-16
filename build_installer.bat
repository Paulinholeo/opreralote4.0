@echo off
echo Compilando o instalador do OperaLote 4.0...
echo.

REM Verifica se o executável principal existe
if not exist "dist\OperaLote4.0.exe" (
    echo Erro: O executável principal "dist\OperaLote4.0.exe" não foi encontrado.
    echo Por favor, gere o executável primeiro usando PyInstaller:
    echo python -m PyInstaller operalote4.spec
    echo.
    pause
    exit /b 1
)

REM Compila o instalador usando o Inno Setup Compiler
echo Compilando o instalador...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "install\operalote4.iss"

if %errorlevel% neq 0 (
    echo.
    echo Erro ao compilar o instalador!
    pause
    exit /b %errorlevel%
)

echo.
echo Instalador compilado com sucesso!
echo O instalador está localizado em: output\install\operalote4.exe
echo.
pause