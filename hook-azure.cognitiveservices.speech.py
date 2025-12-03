from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

# Bundle the native DLLs and any submodules the SDK loads dynamically.
binaries = collect_dynamic_libs("azure.cognitiveservices.speech")
hiddenimports = collect_submodules("azure.cognitiveservices.speech")
