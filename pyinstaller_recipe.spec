# -*- mode: python ; coding: utf-8 -*-
# pip install pyinstaller

# Icon generator in a python console
#from PIL import Image
# Open the source image (recommended size: 1024x1024 or higher)
#img = Image.open("./images/explosion.png")
# Save as .ico with multiple resolutions for best quality
#img.save("icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

block_cipher = None

# Importing shared libraries
#import sysconfig
#import os
#python_lib = os.path.join(sysconfig.get_config_var('LIBDIR'), sysconfig.get_config_var('INSTSONAME'))

def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path

a = Analysis(
    ['main.py'],
    pathex=[],
    #binaries=[(python_lib, '.')],
    binaries=[],
    datas=[('utils', 'utils'), ('images', 'images'), ('haarcascade_xml_files', 'haarcascade_xml_files')],
    #hiddenimports=['sklearn.ensemble._forest'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])
a.datas += mediapipe_tree
a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI4Kids-Laser-Eyes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="icon.ico"
)


