@echo off
:start
cls
echo quick debag your example
echo ----------------
echo 0. exit
echo 1. basic model with ATC take-turns algorithm
echo 2. basic model with Tabu Search algorithm
echo 3. basic model with virtual list algorithm
echo 4. contiunous model with ATCS take-turns algorithm
echo 5. contiunous model with Tabu Search algorithm
echo 6. contiunous model with virtual list algorithm
echo 7. generate data
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
set /p data="your data: "
python basicatc.py ./data/"%data%"
echo work down!
pause
goto start

:2
cls
set /p data="your data: "
python basictabu.py ./data/"%data%"
echo work down!
pause
goto start

:3
cls
set /p data="your data: "
python basicvirtual.py ./data/"%data%"
echo work down!
pause
goto start

:4
cls
set /p data="your data: "
python continueatcs.py ./data/"%data%"
echo work down!
pause
goto start

:5
cls
set /p data="your data: "
python continuetabu.py ./data/"%data%"
echo work down!
pause
goto start

:6
cls
set /p data="your data: "
python continuevirtual.py ./data/"%data%"
echo work down!
pause
goto start

:other
cls
set /p data="your data: "
python experiment_data.py ./data/"%data%"
echo work down!
pause
goto start

:exit
exit