@echo off
cd /d d:\Software\bupt_icpc_rankings\bupt-ranking
echo === Checking environment ===
node --version
npm --version
echo === Running npm install ===
call npm install
echo === Exit code: %ERRORLEVEL% ===
if exist node_modules (
    echo SUCCESS: node_modules created
) else (
    echo FAILED: node_modules not found
)
echo === Done ===