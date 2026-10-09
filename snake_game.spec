# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['snake_game.py'],
    pathex=[],
    binaries=[],
    datas=[('PressStart2P.ttf', '.'), ('eat_sound.wav', '.'), ('game_over.wav', '.'), ('snake_head.png', '.'), ('snake_body.png', '.'), ('food.png', '.'), ('bonus_food.png', '.'), ('trophy.png', '.'), ('fruit_icon.png', '.'), ('snake_menu.png', '.'), ('background_level_1.png', '.'), ('background_level_2.png', '.'), ('background_level_3.png', '.'), ('background_level_4.png', '.'), ('background_level_5.png', '.'), ('background_level_6.png', '.'), ('background_level_7.png', '.'), ('background_level_8.png', '.'), ('background_level_9.png', '.'), ('background_level_10.png', '.')],
    hiddenimports=[],
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
    name='snake_game',
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
)
