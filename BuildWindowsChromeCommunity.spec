a = Analysis(
	['StandaloneWindowsChrome.py'],
	datas=[
		('Web-Historian-Community/', 'Web-Historian/'),
		('Web-Extension-Shim/WebExtensionShim.js', 'Web-Historian/'),
		('FullDiskAccess.html', 'Web-Historian/'),
		('FullDiskAccess.gif', 'Web-Historian/'),
		('LoadJson.js', 'Web-Historian/')
	]
)
pyz = PYZ(
	a.pure,
	a.zipped_data
)
exe = EXE(
	pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	name='WebHistorian',
	console=False,
	icon='icon-128.ico'
)