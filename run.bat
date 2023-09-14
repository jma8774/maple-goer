@echo off

echo Choose a file to run:
echo 1. Run dailyemail.py -- Jeemong's Marksman bot
echo 2. Run rokuinterface.py -- Justin's Wind Archer bot
echo 3. Run ricky.py -- Ricky's Evan bot
echo 4. Run random_utils.py -- Random utilities (Craft WAP, Extracting, Open Herb, and Enhancing)
echo 5. Run autoroll.py -- Auto cubing
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
    python "rokuinterface.py"
) else if "%choice%"=="3" (
    echo You chose Option 3.
    echo. 
    python "ricky.py"
) else if "%choice%"=="4" (
    echo You chose Option 4.
    echo. 
    python "random_utils.py"
) else if "%choice%"=="5" (
    echo You chose Option 5.
    echo. 
    python "autoroll.py"
) else if /i "%choice%"=="Q" (
    echo Quitting...
) else (
    echo Invalid choice. Please enter a valid option.
)

pause