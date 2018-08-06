### How to run under Windows XP, Windows 7 or later ###

- Open Node.js command prompt:
```
C:\tensorflow-mnist> "C:\Program Files\nodejs\npm.cmd" install
```

- Open Anaconda3 or Miniconda3 prompt:
```
C:\tensorflow-mnist> pip install -r requirements.txt
C:\tensorflow-mnist> set FLASK_APP=main.py
C:\tensorflow-mnist> flask run
```

- Open `http://127.0.0.1:5000` in any web browser.


### Note ###

- Node.js command prompt:
```
%windir%\System32\cmd.exe /K "C:\Program Files\nodejs\nodevars.bat"
```

- Anaconda3 prompt:
```
%windir%\System32\cmd.exe "/K" "C:\Anaconda3\Scripts\activate.bat" "C:\Anaconda3"
```

- Miniconda3 prompt:
```
%windir%\System32\cmd.exe "/K" "C:\Miniconda3\Scripts\activate.bat" "C:\Miniconda3"
```

- Windows command prompt:
```
%windir%\System32\cmd.exe
```
