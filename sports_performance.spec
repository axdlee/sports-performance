# -*- mode: python ; coding: utf-8 -*-
"""
体育成绩评估系统 - 统一打包配置文件
支持 macOS 和 Windows 平台
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 收集所有数据文件（只包含必需的配置文件）
datas = [
    ('config', 'config'),
]

# 如果 data 目录存在则添加（用户数据应存储在系统目录，不打包进应用）
if os.path.exists('data'):
    datas.append(('data', 'data'))

# 收集所有隐藏导入
hiddenimports = [
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.backends.backend_agg',
    'matplotlib.backends._backend_tk',
    'matplotlib.figure',
    'matplotlib.pyplot',
    'PIL',
    'PIL._tkinter_finder',
    'tkinter',
    'tkinter.ttk',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'tkinter.font',
    'json',
    'datetime',
    'uuid',
    'numpy',
]

# 分析阶段
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ 阶段
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 判断平台
is_macos = sys.platform == 'darwin'
is_windows = sys.platform == 'win32'

# EXE 阶段
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='体育成绩评估系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用 UPX 压缩，避免 DLL 加载问题和杀毒软件误报
    console=False,  # 无控制台窗口
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.icns' if is_macos else 'assets/icon.ico',  # 平台特定图标
    version_file=None,  # 可以添加版本信息文件来降低误报率
)

# COLLECT 阶段
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # 禁用 UPX 压缩，避免 DLL 加载问题
    upx_exclude=[],
    name='体育成绩评估系统',
)

# macOS App Bundle
if is_macos:
    app = BUNDLE(
        coll,
        name='体育成绩评估系统.app',
        icon='assets/icon.icns' if os.path.exists('assets/icon.icns') else None,
        bundle_identifier='com.sports.performance.assessment',
        info_plist={
            'CFBundleName': '体育成绩评估系统',
            'CFBundleDisplayName': '体育成绩评估系统',
            'CFBundleGetInfoString': "Physical Education Performance Assessment System",
            'CFBundleIdentifier': "com.sports.performance.assessment",
            'CFBundleVersion': "1.0.0",
            'CFBundleShortVersionString': "1.0.0",
            'NSHumanReadableCopyright': "Copyright © 2025",
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
