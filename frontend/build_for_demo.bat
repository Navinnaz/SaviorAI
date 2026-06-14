@echo off
echo ========================================
echo SaviorAI Production Build for Demo
echo ========================================
echo.

echo [1/3] Clearing old build...
if exist "dist" (
    rmdir /s /q "dist"
    echo     - Old build cleared
)
if exist "node_modules\.vite" (
    rmdir /s /q "node_modules\.vite"
    echo     - Vite cache cleared
)

echo [2/3] Building production version...
call npm run build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    pause
    exit /b 1
)

echo [3/3] Starting production preview...
echo.
echo ========================================
echo SUCCESS! Production build complete.
echo.
echo Starting preview server...
echo Open: http://localhost:4173
echo.
echo This is your DEMO-READY version!
echo Open in INCOGNITO mode: Ctrl+Shift+N
echo ========================================
echo.

call npm run preview
