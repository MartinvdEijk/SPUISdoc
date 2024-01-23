# Packages
import PyInstaller.__main__
import os
import glob

# Input
VERSION = 'V03'

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
files = glob.glob('/YOUR/PATH/*')
for f in files:
    os.remove(f)
os.remove('SPUIS'+VERSION+'.spec')