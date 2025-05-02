# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app2.py'],
    pathex=[],
    binaries=[],
    datas=[('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.core.dll', 'azure\\cognitiveservices\\speech'), ('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.audio.sys.dll', 'azure\\cognitiveservices\\speech'), ('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.codec.dll', 'azure\\cognitiveservices\\speech'), ('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.kws.dll', 'azure\\cognitiveservices\\speech'), ('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.kws.ort.dll', 'azure\\cognitiveservices\\speech'), ('venv\\Lib\\site-packages\\azure\\cognitiveservices\\speech\\Microsoft.CognitiveServices.Speech.extension.lu.dll', 'azure\\cognitiveservices\\speech')],
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
    name='app2',
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
