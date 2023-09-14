@echo off

echo Choose a file to run:
echo 1. Run dailyemail.py
echo 2. Run random_utils.py
echo 3. Run rokuinterface.py
echo Q. Quit
echo Type 1, 2, 3, or Q and press Enter:

set /p choice=
if "%choice%"=="1" (
    echo You chose Option 1.
    echo. 
    python "dailyemail.py"
) else if "%choice%"=="2" (
    echo You chose Option 2.
    echo. 
    python "random_utils.py"
) else if "%choice%"=="3" (
    echo You chose Option 3.
    echo. 
    python "rokuinterface.py"
) else if /i "%choice%"=="Q" (
    echo Quitting...
) else (
    echo Invalid choice. Please enter a valid option.
)

pause