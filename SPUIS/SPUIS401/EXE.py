# Packages
import PyInstaller.__main__
import os
import glob
import shutil

# Input
VERSION = 'V01'

# Check
if os.path.exists(os.getcwd()+'\\dist\\'+'SPUIS'+VERSION+'.exe'):
    print('Version already exists. Please remove folder or use different version.')
    exit()

# Generate exe
PyInstaller.__main__.run([
    'SPUIS401.py',
    '--onefile',
    '--contents-directory', VERSION,
    '-n', 'SPUIS'+VERSION
])
test = os.listdir(dir_name)
for item in test:
    if item.endswith(".spec") or item.endswith(".exe"):
        os.remove(os.path.join(dir_name, item))
shutil.copyfile('./dist/SPUIS'+VERSION+'.exe', 'SPUIS401.exe')