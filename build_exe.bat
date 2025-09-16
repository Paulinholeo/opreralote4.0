@echo off
echo Gerando o executável do OperaLote 4.0...
echo.

REM Verifica se o PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo PyInstaller não encontrado. Instalando...
    pip install pyinstaller
    echo.
)

REM Gera o executável usando o arquivo spec
echo Gerando executável...
python -m PyInstaller operalote4.spec

if %errorlevel% neq 0 (
    echo.
    echo Erro ao gerar o executável!
    pause
    exit /b %errorlevel%
)

echo.
echo Executável gerado com sucesso!
echo O executável está localizado em: dist\OperaLote4.0.exe
echo.
pause