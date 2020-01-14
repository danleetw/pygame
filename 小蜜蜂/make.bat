@echo off
REM --noconsole
call pyinstaller  -F --noupx --noconsole Game20200112.py   
rem call pyinstaller -F Game20200112.py  -p -add-data datafile.ext *.png
 

