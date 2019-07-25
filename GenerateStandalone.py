import os, sys, tempfile, sqlite3, json, os, shutil, webbrowser

temporaryDirectoryBase = tempfile.mkdtemp(prefix="WebHistorian_")
temporaryDirectory = os.path.join(temporaryDirectoryBase, "Files")
homePage = os.path.join(temporaryDirectory, "index.html")
fullDiskAccessPage = os.path.join(temporaryDirectory, "FullDiskAccess.html")
fullDiskAccessSettings = "x-apple.systempreferences:com.apple.preference.security?Privacy"
historyItemsOutputFile = os.path.join(temporaryDirectory, "HistoryItems.js")
visitItemsOutputFile = os.path.join(temporaryDirectory, "VisitItems.js")
manifestInputFile = os.path.join(temporaryDirectory, "manifest.json")
manifestOutputFile = os.path.join(temporaryDirectory, "Manifest.js")
categoriesInputFile = os.path.join(temporaryDirectory, "core", "js", "app", "categories.json")
categoriesOutputFile = os.path.join(temporaryDirectory, "Categories.js")
def messagesInputFile(temporaryDirectory, defaultLocale):
	return os.path.join(temporaryDirectory, "_locales", defaultLocale, "messages.json")
messagesOutputFile = os.path.join(temporaryDirectory, "Messages.js")
databaseInputFileCopy = os.path.join(temporaryDirectory, "History.db")
logOutputFile = os.path.join(temporaryDirectory, "Log.json")
logList = []
resourceSubDirectory = "Web-Historian"
if hasattr(sys, '_MEIPASS'):
	resourceInputDirectory = os.path.join(sys._MEIPASS, resourceSubDirectory)
else:
	resourceInputDirectory = os.path.join(os.path.abspath("."), resourceSubDirectory)
injectedHtml = "\
	<script type=\"application/javascript\" src=\"Manifest.js\"></script> \
	<script type=\"application/javascript\" src=\"Messages.js\"></script> \
	<script type=\"application/javascript\" src=\"HistoryItems.js\"></script> \
	<script type=\"application/javascript\" src=\"VisitItems.js\"></script> \
	<script type=\"application/javascript\" src=\"WebExtensionShim.js\"></script> \
	<script type=\"application/javascript\" src=\"Categories.js\"></script> \
	<script type=\"application/javascript\" src=\"LoadJson.js\"></script>"

def generateStandalone(databaseInputFile, sqlHistoryItems, sqlVisitItems, copyDatabaseInputFile):

	continueBoolean = True

	try:
		shutil.copytree(resourceInputDirectory, temporaryDirectory) # Also creates the temp directory.
		logList.append({"Action" : "Copy Web Historian files to temporary directory", "Success" : True})
	except Exception as exception:
		logList.append({"Action" : "Copy Web Historian files to temporary directory", "Success" : False, "Error" : str(exception)})
		continueBoolean = False

	if continueBoolean:
		if os.path.isfile(homePage):
			logList.append({"Action" : "Locate home page", "Success" : True})
		else:
			logList.append({"Action" : "Locate home page", "Success" : False})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(homePage, "r") as file:
				mainHtml = file.read()
			logList.append({"Action" : "Read home page", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Read home page", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		if "<head>" in mainHtml:
			newHtml = mainHtml.replace("<head>", "<head>" + injectedHtml, 1)
			logList.append({"Action" : "Replace HEAD in HTML code", "Success" : True})
		else:
			logList.append({"Action" : "Replace HEAD in HTML code", "Success" : False})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(homePage, "w") as file:
				file.write(newHtml)
			logList.append({"Action" : "Inject HTML code into home page", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Inject HTML code into home page", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		if os.path.isfile(manifestInputFile):
			logList.append({"Action" : "Locate extension manifest", "Success" : True})
		else:
			logList.append({"Action" : "Locate extension manifest", "Success" : False})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(manifestInputFile, "r") as file:
				manifestJson = json.load(file)
			manifestJs = "var manifestJson = " + json.dumps(manifestJson)
			with open(manifestOutputFile, "w") as file:
				file.write(manifestJs)
			logList.append({"Action" : "Wrote manifest data", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Wrote manifest data", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		if "default_locale" in manifestJson:
			defaultLocale = manifestJson.get("default_locale")
			logList.append({"Action" : "Manifest contains default locale", "Success" : True})
		else:
			logList.append({"Action" : "Manifest contains default locale", "Success" : False})
			continueBoolean = False

	if continueBoolean:
		if os.path.isfile(messagesInputFile(temporaryDirectory, defaultLocale)):
			logList.append({"Action" : "Locate default locale messages", "Success" : True})
		else:
			logList.append({"Action" : "Locate default locale messages", "Success" : False})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(messagesInputFile(temporaryDirectory, defaultLocale), "r") as file:
				messagesJson = json.load(file)
			messagesJs = "var messagesJson = " + json.dumps(messagesJson)
			with open(messagesOutputFile, "w") as file:
				file.write(messagesJs)
			logList.append({"Action" : "Wrote default locale messages data", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Wrote default locale messages data", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(categoriesInputFile, "r") as file:
				categoriesJson = json.load(file)
			categoriesJs = "var categoriesJson = " + json.dumps(categoriesJson)
			with open(categoriesOutputFile, "w") as file:
				file.write(categoriesJs)
			logList.append({"Action" : "Wrote categories data", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Wrote categories data", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			if copyDatabaseInputFile: # to avoid the DB being locked. Applicable to Chrome.
				shutil.copyfile(databaseInputFile, databaseInputFileCopy)
				databaseInputFile = databaseInputFileCopy
			logList.append({"Action" : "Copy browser database to unlock it if necessary", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Copy browser database to unlock it if necessary", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			connection = sqlite3.connect(databaseInputFile)
			cursor = connection.cursor()
			logList.append({"Action" : "Open connection to database", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Open connection to browser database", "Success" : False, "Error" : str(exception)})
			try: # Open instructions to user how to give access to their browser database. Applicable to Safari.
				webbrowser.open_new_tab("file:" + fullDiskAccessPage)
				logList.append({"Action" : "Open Full Disk Access page in new tab in browser", "Success" : True})
			except Exception as exception:
				logList.append({"Action" : "Open Full Disk Access page in new tab in browser", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			historyOutputData = []
			for row in cursor.execute(sqlHistoryItems):
				historyOutputData.append({"id" : row[0], "url" : row[1], "title" : row[2], "lastVisitTime" : row[3], "visitCount" : row[4], "typedCount" : row[5]})
			visitOutputData = []
			for row in cursor.execute(sqlVisitItems):
				visitOutputData.append({"id" : row[0], "visitId" : row[1], "visitTime" : row[2], "referringVisitId" : row[3], "transition" : row[4], "visitOrigin" : row[5]})
			connection.close()
			logList.append({"Action" : "Extract History and Visit Items from browser database", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Extract History and Visit Items from browser database", "Success" : False, "Error" : str(exception)})
			connection.close()
			continueBoolean = False

	if continueBoolean:
		try:
			with open(historyItemsOutputFile, "w") as outputFile:
				outputFile.write("var historyItemsJson = " + json.dumps(historyOutputData))
			logList.append({"Action" : "Write History Items to temporary directory", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Write History Items to temporary directory", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			with open(visitItemsOutputFile, "w") as outputFile:
				outputFile.write("var visitItemsJson = " + json.dumps(visitOutputData))
			logList.append({"Action" : "Write Visit Items to temporary directory", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Write Visit Items to temporary directory", "Success" : False, "Error" : str(exception)})
			continueBoolean = False

	if continueBoolean:
		try:
			webbrowser.open_new_tab("file:" + homePage)
			logList.append({"Action" : "Open Web Historian in new tab in browser", "Success" : True})
		except Exception as exception:
			logList.append({"Action" : "Open Web Historian in new tab in browser", "Success" : False, "Error" : str(exception)})

	try:
		with open(logOutputFile, "w") as outputFile:
			outputFile.write(json.dumps(logList))
	except Exception as exception:
		print("Could not write log to temporary directory: " + str(exception))
		print(json.dumps(logList))