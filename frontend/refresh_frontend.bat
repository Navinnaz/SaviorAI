@echo off
echo ========================================
echo SaviorAI Frontend Cache Clear & Restart
echo ========================================
echo.

echo [1/4] Stopping any running dev servers...
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo [2/4] Clearing Vite cache...
if exist "node_modules\.vite" (
    rmdir /s /q "node_modules\.vite"
    echo     - Vite cache cleared
) else (
    echo     - No Vite cache found
)

if exist "dist" (
    rmdir /s /q "dist"
    echo     - Dist folder cleared
) else (
    echo     - No dist folder found
)

echo [3/4] Clearing browser cache...
echo     Please do ONE of these in your browser:
echo     - Press Ctrl + Shift + R (hard refresh)
echo     - Press Ctrl + Shift + Delete (clear cache)
echo     - Open Incognito: Ctrl + Shift + N
echo.

echo [4/4] Starting fresh dev server...
echo.
echo ========================================
echo Frontend will start in 3 seconds...
echo Open: http://localhost:5173
echo Remember to HARD REFRESH: Ctrl+Shift+R
echo ========================================
timeout /t 3 >nul
echo.

npm run dev
