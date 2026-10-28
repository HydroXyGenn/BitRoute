# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['converter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app_icon.png', '.'),
        ('app_icon.ico', '.'),
    ],
    hiddenimports=[
        'engine',
        'engine.ipv4_math',
        'engine.vlsm_solver',
        'engine.drills_solver',
        'engine.tips_bank',
        'ui',
        'ui.main_window',
        'ui.themes',
        'ui.widgets',
        'ui.tab_binary',
        'ui.tab_subnet',
        'ui.tab_vlsm',
        'ui.tab_drills',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.png'],
)
