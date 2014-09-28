# -*- mode: python -*-
a = Analysis(['GUI.py'],
             pathex=['/Users/usuario/aTXT'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=False,
          name='aTXT',
          debug=False,
          strip=None,
          upx=True,
          console=False )

extra_tree = Tree('./bin', prefix = 'bin')
extra_tree += Tree('./docx', prefix = 'docx')
extra_tree += Tree('./pdfminer', prefix = 'pdfminer')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               extra_tree,
               strip=None,
               upx=True,
               name='GUI')
