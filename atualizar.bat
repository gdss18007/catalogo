@echo off
:: Navega para a pasta onde o script esta (deve ser a pasta do repositorio)
cd /d "%~dp0"

echo [1/3] Verificando e adicionando alteracoes (novas, deletadas, renomeadas)...
git add -A

echo.
echo [2/3] Criando o ponto de salvamento (commit)...
:: O commit leva a data e a hora atual como mensagem automatica
git commit -m "Atualizacao automatica do catalogo: %date% %time%"

echo.
echo [3/3] Enviando para o GitHub...
git push origin master

echo.
echo ==========================================
echo Catalogo atualizado com sucesso no GitHub!
echo ==========================================
pause