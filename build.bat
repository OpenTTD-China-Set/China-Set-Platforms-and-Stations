@echo off
:start
py nml_patcher.py -f "cnsplatmenu.pnml" -o "cnsplat.nml" -b 1 -v 1
nmlc cnsplat.nml -o cnsplatform.grf

:: move to newgrf directory
copy cnsplatform.grf D:\Data\Documents\OpenTTD\newgrf
pause
goto start
exit