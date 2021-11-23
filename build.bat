pyinstaller -F -w --clean PsychRewritesFormatter.py
powershell Compress-Archive -Update dist dist.zip
del /q PsychRewritesFormatter.spec 
rmdir /s /q __pycache__ build