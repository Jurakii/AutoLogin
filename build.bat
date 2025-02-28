@echo off
pyinstaller --onefile --windowed --icon="icon.ico" --add-data "dist\chromedriver.exe;dist\chromedriver.exe" Autolog.pyw
pause
