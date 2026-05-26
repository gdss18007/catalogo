@echo off
:: Navega para a pasta onde o script esta
cd /d "%~dp0"

echo [1/4] Baixando atualizacoes do GitHub (Garantindo sincronia)...
git pull origin master --rebase

echo.
echo [2/4] Verificando e adicionando alteracoes locais...
git add -A

echo.
echo [3/4] Criando o ponto de salvamento (commit)...
git commit -m "Atualizacao automatica da loja: %date% %time%"

echo.
echo [4/4] Enviando tudo de volta para o GitHub...
git push origin master

echo.
echo ==========================================
echo Catalogo atualizado com sucesso no GitHub!
echo ==========================================
pause