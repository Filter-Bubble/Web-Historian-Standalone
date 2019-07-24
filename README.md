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

- Configure your edition of Web Historian in the submodule directory. The only supported one is the Community edition. Standalone versions of Web Historian Habits or Web Historian Education are possible in principle, but currently not implemented.
- Run `pyinstaller Build[OS][Browser][WebHistorianEdition].spec` where [OS] currently is either Windows or Mac, [Browser] is only Chrome for Windows and either Chrome or Safari for Mac and, finally, the choice for [WebHistorianEdition] is only Community.
- When building on Mac, also run `Disk Utility` and choose `File` > `New Image` > `Image from Folder` (see [here](https://support.apple.com/en-gb/guide/disk-utility/dskutl11888/mac)). Then select the directory with the Web Historian app. This will generate a _.dmg_ file which allows the app to be distributed more easily.

### Additional commands

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

### Build[OS][Browser][WebHistorianEdition].spec

This file contains the instructions for `pyinstaller` to build the application.

### FullDiskAccess.gif

This GIF shows how to add the app to the _Full Disk Access_ list and grant it permission to access browser history data.

### FullDiskAccess.html

This webpage explains how to add the app to the _Full Disk Access_ list and grant it permission to access browser history data. 

### GenerateStandalone.py

This script copies the relevant files to a temporary location on the user's computer. It also extracts the browsing history from their browser and converts this to _JSON_ files. For Safari, if the script cannot get access to the browsing history, the _FullDiskAccess.html_ page is launched in the user's default browser. If everything goes well, the default browser is launched with a standalone version of _Web Historian_ including the browsing history.

### icon-128.[icns/ico]

This icon (.icns for Mac, .ico for Windows) contains the logo of the Web Historian browser extension which is used for the app.

### LoadJson.js

When running a web page with _JavaScript_ locally, many browsers disable the ability to load _JSON_ data files. The _jQuery_ `get` function, used in Web Historian, would give an error. This file overrides the `get` function and bypasses the loading of _JSON_ files by defining the data as variables and passing these on.

### Standalone[OS][Browser].py

These Python scripts contain the configurations to create standalone versions of Web Historian for various OS's and various browsers. It imports the _GenerateStandalone.py_ script and subsequently runs the `generateStandalone` function.