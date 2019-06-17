# Web Historian Standalone

This repository contains scripts to convert the _Web Historian_ browser extension to a standalone _MacOS_ app running on the _Safari_ browser.

## Background

Online and mobile news consumption leaves digital traces that are used to personalize news supply, possibly creating filter bubbles where people are exposed to a low diversity of issues and perspectives that match their preferences. The [JEDS Filter Bubble](http://ccs.amsterdam/projects/jeds/) project aims to understand the filter bubble effect by performing deep semantic analyses on mobile news consumption traces. This project is a collaboration between the [VU](https://www.vu.nl/nl/index.aspx), the [UvA](http://www.uva.nl/) and [NLeSC](https://www.esciencecenter.nl/), lead by [Wouter van Atteveldt](http://vanatteveldt.com/).

Part of this project makes use of the [Web Historian](http://www.webhistorian.org/) browser extension, developed by [Ericka Menchen-Trevino](http://www.ericka.cc/). As Safari does not support the [WebExtensions API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions), to use this extension on _MacOS_, it should be packaged as a standalone app. This app will include a _JavaScript_ [web extension shim](https://github.com/Filter-Bubble/Web-Extension-Shim) which implements some of the _WebExtensions API_ calls.

## Installation

### Prerequisites

- Clone the repository and its submodules using `git clone --recurse-submodules`.
- Install `pyinstaller` using `pip install pyinstaller`.

### Build the app

- Run `pyinstaller GenerateStandalone.py --onefile --windowed --name="WebHistorian" --icon="icon-128.icns" --add-data="Web-Historian-xx/:Web-Historian/" --add-data="Web-Extension-Shim/WebExtensionShim.js:Web-Historian/" --add-data="FullDiskAccess.html:Web-Historian/" --add-data="FullDiskAccess.gif:Web-Historian/"`.
- Substitute `Web-Historian-Community`, `Web-Historian-Education` or `Web-Historian-Habits` for `Web-Historian-xx`.

### Additional commands

- Run `pyinstaller WebHistorian.spec` to build the app using the options specified in the _spec_ file.
- Run `git submodule foreach git pull origin master` to pull the latest commit for each submodule.

## Repository content

### Web-Extension-Shim

This directory contains the [Web Extension Shim](https://github.com/Filter-Bubble/Web-Extension-Shim/) submodule which contains a JavaScript script that implements some of the _WebExtensions API_ calls.

### Web-Historian-Community

This directory contains the [Web Historian - Community Edition](https://github.com/WebHistorian/community/) submodule which contains all the source code of the Web Historian browser extension.

### Web-Historian-Education

This directory contains the [Web Historian - Education Edition](https://github.com/erickaakcire/webhistorian/) submodule which contains all the source code of the Web Historian browser extension.

### Web-Historian-Habits

This directory contains the [Web Historian - Habits Edition](https://github.com/WebHistorian/habits/) submodule which contains all the source code of the Web Historian browser extension.

### FullDiskAccess.gif

This GIF shows how to add the app to the _Full Disk Access_ list and grant it permission to access browser history data.

### FullDiskAccess.html

This webpage explains how to add the app to the _Full Disk Access_ list and grant it permission to access browser history data. 

### GenerateStandalone.py

This script copies the relevant files to a temporary location on the user's computer. It also extracts the browsing history from their _Safari_ browser and converts this to _JSON_ files. If the script cannot get access to the browsing history, the _FullDiskAccess.html_ page is launched in the user's default browser. If everything goes well, the default browser is launched with a standalone version of _Web Historian_ including the Safari browsing history.

### icon-128.icns

This icon contains the logo of the Web Historian browser extension which is used for the app.
