@echo off
:start
cls
echo quick debag your example
echo ----------------
echo 0. exit
echo 1. problem 1
echo 2. problem 2
echo 3. problem 3
echo 4. problem 4
echo 5. problem 5
echo 6. problem 6
echo 7. other data
echo 8. submit
echo ----------------
set /p num="your choice: "
if "%num%"=="1" goto 1
if "%num%"=="2" goto 2
if "%num%"=="3" goto 3
if "%num%"=="4" goto 4
if "%num%"=="5" goto 5
if "%num%"=="6" goto 6
if "%num%"=="7" goto other
if "%num%"=="8" goto submit
if "%num%"=="0" goto exit
echo wrong choice！
pause
goto start

:1
cls
python debag.py ./data/gc_50_3
echo work down!
pause
goto start

:2
cls
python debag.py ./data/gc_70_7
echo work down!
pause
goto start

:3
cls
python debag.py ./data/gc_100_5
echo work down!
pause
goto start

:4
cls
python debag.py ./data/gc_250_9
echo work down!
pause
goto start

:5
cls
python debag.py ./data/gc_500_1
echo work down!
pause
goto start

:6
cls
python debag.py ./data/gc_1000_5
echo work down!
pause
goto start

:other
cls
set /p data="your data: "
set /p result="your result: "
python debag.py ./data/"%data%" ./result/"%result%"
echo work down!
pause
goto start

echo work down!
pause
goto start

:submit
cls
python submit.py
echo work down!
pause
goto start

:exit
exit