@echo off
echo ========================================
echo OperaLote 4.3 - Sistema de Analise de Infracoes
echo ========================================
echo.

REM Adiciona assets ao PYTHONPATH
set PYTHONPATH=%CD%\assets;%PYTHONPATH%

REM Navega para o diretorio src
cd src

REM Executa a aplicacao
python main.py

REM Pausa para ver erros
pause
