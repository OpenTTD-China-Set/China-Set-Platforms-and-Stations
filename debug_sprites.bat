@echo off
:start
py generate_code_and_sprite.py
py nml_patcher.py -f "cnsps.pnml" -o "cnsps.nml" -b 1 -v 1
nmlc cnsps.nml -o cnsplatform.grf

:: move to newgrf directory
copy cnsplatform.grf D:\Data\Documents\OpenTTD\newgrf
echo.
echo ========================================================
echo.
pause
:: debug purpose, goto start to run again
goto start