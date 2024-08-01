# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['full_app_code.py'],  # Replace with your main script file name
    pathex=['.'],  # Path to search for imports
    binaries=[],
    datas=[
        ('path_to_qtawesome_fonts', 'qtawesome/fonts'),  # Add any additional data files or directories needed
    ],
    hiddenimports=[
        'pymysql', 'qtawesome'  # Add hidden imports if needed
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DatabaseApp',  # Name of your executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False  # Change to True if you want a console window to be shown
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DatabaseApp'  # Name of the final folder containing all files
)
