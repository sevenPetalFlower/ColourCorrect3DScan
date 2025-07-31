@echo off
setlocal enabledelayedexpansion

REM Set paths
set DCRAW_PATH=C:\Users\Laysa\Documents\svitlana\usefull_installs\DCRaw_V9.28.exe
set IMAGE_FOLDER=C:\Users\Laysa\Documents\svitlana\white_object_final\nef

REM Go to image folder
cd /d "%IMAGE_FOLDER%"

REM Loop through all .dng files
for %%f in (*.NEF) do (
    echo Processing: %%f
    "%DCRAW_PATH%"  -v -r 2.7183125 1 1.3616409 1 -o 1 -T "%%f"
)

echo Done!
pause
