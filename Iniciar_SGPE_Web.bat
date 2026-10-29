@echo off
chcp 65001 >nul
echo ============================================================================
echo   SGPE PGE-MA 2027-2030 - Sistema de Gestao do Planejamento Estrategico
echo   Executando 100%% em User-Space (Sem necessidade de privilegios de Admin)
echo ============================================================================
echo.
cd /d "%~dp0"
start "" "http://127.0.0.1:8765"
python -m uvicorn sgpe_app.backend:app --host 127.0.0.1 --port 8765
pause
