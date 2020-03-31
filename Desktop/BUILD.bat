rmdir /s /q __pycache__
pyinstaller -F RigMonitor.pyw
rem rmdir /s /q dist
rem rmdir /s /q build
rmdir /s /q __pycache__
del RigMonitor.spec