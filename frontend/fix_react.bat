@echo off
echo ===============================================
echo Fixing React Hook Error - Multiple React Copies
echo ===============================================
echo.

echo Step 1: Stopping any running processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo Step 2: Removing node_modules...
if exist node_modules rmdir /s /q node_modules
echo    Done

echo Step 3: Removing package-lock.json...
if exist package-lock.json del /f package-lock.json
echo    Done

echo Step 4: Clearing npm cache...
call npm cache clean --force
echo    Done

echo Step 5: Clearing Vite cache...
if exist .vite rmdir /s /q .vite
if exist dist rmdir /s /q dist
echo    Done

echo Step 6: Installing dependencies (this may take a minute)...
call npm install
echo    Done

echo.
echo ===============================================
echo Fix complete! Now run: npm run dev
echo ===============================================
pause
