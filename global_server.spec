# -*- mode: python ; coding: utf-8 -*-
import PyInstaller

datas = [('C:\\Users\\hseth\\Anaconda3\\envs\\myenv2\\xgboost\\*', 'xgboost/'), ('C:\\Users\\hseth\\Anaconda3\\envs\\myenv2\\Lib\\site-packages\\xgboost\\VERSION', 'xgboost/')]
datas.extend(PyInstaller.utils.hooks.collect_data_files('spacy.lang', include_py_files = True))
datas.extend(PyInstaller.utils.hooks.collect_data_files('en_core_web_sm'))
datas.extend(PyInstaller.utils.hooks.collect_data_files('thinc'))

block_cipher = None


a = Analysis(['global_server.py'],
             pathex=['C:\\Users\\hseth\\Desktop\\manage server'],
             binaries=[],
             datas=datas,
             hiddenimports=['spacy.kb',
    'spacy.lexeme',
    'spacy.matcher._schemas',
    'spacy.morphology',
    'spacy.parts_of_speech',
    'spacy.syntax._beam_utils',
    'spacy.syntax._parser_model',
    'spacy.syntax.arc_eager',
    'spacy.syntax.ner',
    'spacy.syntax.nn_parser',
    'spacy.syntax.stateclass',
    'spacy.syntax.transition_system',
    'spacy.tokens._retokenize',
    'spacy.tokens.morphanalysis',
    'spacy.tokens.underscore',

    'blis',
    'blis.py','sqlalchemy','mysql','pymysql',

    'cymem',
    'cymem.cymem',

    'murmurhash',

    'preshed.maps',

    'srsly.msgpack.util',

    'thinc.extra.search',
    'thinc.linalg',
    'thinc.neural._aligned_alloc',
    'thinc.neural._custom_kernels'
],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='server')
