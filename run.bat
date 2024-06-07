@echo off

echo Type a number to choose a file to run:
echo 1. Run rokuinterface.py -- Justin's Wind Archer bot
echo 2. Run rokuinterface.py -- Justin's Wind Archer bot in dev mode
echo 3. Run steven.py -- Steven's Mechanic bot
echo 4. Run steven.py -- Steven's Mechanic bot in dev mode
echo 5. Run random_utils.py -- Random utilities (Craft WAP, Extracting, Open Herb, and Enhancing)
echo 6. Run autoroll.py -- Auto cubing
echo Q. Quit
echo Type a number like 1 and press Enter to choose an option.

set /p choice=
if "%choice%"=="1" (
    python "rokuinterface.py"
) else if "%choice%"=="2" (
    python "rokuinterface.py" "dev"
) else if "%choice%"=="3" (
    python "steven.py"
) else if "%choice%"=="4" (
    python "steven.py" "dev"
) else if "%choice%"=="5" (
    python "random_utils.py"
) else if "%choice%"=="6" (
    python "autoroll.py"
) else if /i "%choice%"=="Q" (
    echo Quitting...
) else (
    echo Invalid choice. Please enter a valid option.
)

pause