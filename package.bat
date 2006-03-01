REM python 2.3.5 with py2exe 0.6.4
python.exe setup_win.py py2exe --bundle 1 --dll-excludes w9xpopen.exe

sleep 1

rm -rf build

sleep 1

mv dist omaha

sleep 1

python.exe setup_con.py py2exe --bundle 1 --dll-excludes w9xpopen.exe

sleep 1

rm -rf build

sleep 1

mv dist\calc.exe omaha

sleep 1

rm -rf dist

sleep 1
