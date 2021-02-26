@echo on
pyinstaller --noconfirm --onedir --windowed --icon "koala.ico" --name "ScreamGUI" --uac-admin --add-data "koala.ico;."  "main.py"