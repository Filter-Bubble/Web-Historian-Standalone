# Web Historian Standalone

This repository contains scripts to convert the _Web Historian_ browser extension to a standalone executable.

## Background

Online and mobile news consumption leaves digital traces that are used to personalize news supply, possibly creating filter bubbles where people are exposed to a low diversity of issues and perspectives that match their preferences. The [JEDS Filter Bubble](http://ccs.amsterdam/projects/jeds/) project aims to understand the filter bubble effect by performing deep semantic analyses on mobile news consumption traces. This project is a collaboration between the [VU](https://www.vu.nl/nl/index.aspx), the [UvA](http://www.uva.nl/) and [NLeSC](https://www.esciencecenter.nl/), lead by [Wouter van Atteveldt](http://vanatteveldt.com/).

Part of this project makes use of the [Web Historian](http://www.webhistorian.org/) browser extension, developed by [Ericka Menchen-Trevino](http://www.ericka.cc/). In some cases, it is beneficial to run this extension as a standalone executable. For example, _Safari_ does not support the [WebExtensions API](https://developers.chrome.com/extensions). This project allows _Web Historian_ to run as a _MacOS_ app for the _Safari_ browser. Another benefit of this method is that it gives access to additional entries in the browser history database. For example, in _Chrome_, the device origin of a URL is not accessible via the _WebExtensions API_, but it is via a direct query on the database. This project uses _Python_ to orchestrate the code, _SQL_ to query the browser database and a _JavaScript_ [web extension shim](https://github.com/Filter-Bubble/Web-Extension-Shim), which implements some of the _WebExtensions API_ calls, to allow the extension to run as a local web page.

## Installation

### Prerequisites

- Clone the repository and its submodules using `git clone --recurse-submodules`.
- Install `pyinstaller` using `pip install pyinstaller`.

### Build the app

- Configure your edition of Web Historian in the submodule directory. Currently, the only supported edition is the _Community_ edition. Standalone versions of _Web Historian Habits_ or _Web Historian Education_ are possible in principle, but currently not implemented.
- Run `pyinstaller Build[OS][Browser][WebHistorianEdition].spec` where [OS] is either _Windows_ or _Mac_, [Browser] is only _Chrome_ for _Windows_ and either _Chrome_ or _Safari_ for _Mac_ and, finally, the choice for [WebHistorianEdition] is only _Community_. These choices may be extended in the future.
- When building the app on _Mac_, also run `Disk Utility` and choose `File` > `New Image` > `Image from Folder` (see [here](https://support.apple.com/en-gb/guide/disk-utility/dskutl11888/mac)). Then select the directory with the _Web Historian_ app. This will generate a _.dmg_ file which allows the app to be distributed more easily.

### Additional commands

- Run `git submodule update --init --recursive` to initiate and update all submodules if you forgot during the clone.
- Run `git submodule foreach git pull origin master` to pull the latest commit for each submodule.

## Repository content

### Web-Extension-Shim

This directory contains the [Web Extension Shim](https://github.com/Filter-Bubble/Web-Extension-Shim/) submodule which contains a _JavaScript_ file that implements some of the _WebExtensions API_ calls.

### Web-Historian-Community

This directory contains the [Web Historian - Community Edition](https://github.com/WebHistorian/community/) submodule which contains all the source code of the _Web Historian Community Edition_ browser extension.

### Web-Historian-Education

This directory contains the [Web Historian - Education Edition](https://github.com/erickaakcire/webhistorian/) submodule which contains all the source code of the _Web Historian Education Edition_ browser extension.

### Web-Historian-Habits

This directory contains the [Web Historian - Habits Edition](https://github.com/WebHistorian/habits/) submodule which contains all the source code of the _Web Historian Habits Edition_ browser extension.

### Build[OS][Browser][WebHistorianEdition].spec

These files contain the instructions for `pyinstaller` to build the application.

### FullDiskAccess.gif

This _GIF_ shows how to add the app to the _Full Disk Access_ list and grant it permission to access browser history data on _MacOS_.

### FullDiskAccess.html

This webpage explains how to add the app to the _Full Disk Access_ list and grant it permission to access their browser history database on _MacOS_. 

### GenerateStandalone.py

This _Python_ script copies the relevant files to a temporary location on the user's computer. It also extracts the browsing history from their browser and converts this to _JSON_ files. For _Mac_ users, if the script cannot get access to the browsing history, the _FullDiskAccess.html_ page is launched in the user's default browser. If everything goes well, the default browser is launched with a standalone version of _Web Historian_ including the browsing history.

### icon-128.[icns/ico]

This icon (.icns for _Mac_, .ico for _Windows_) contains the logo of the Web Historian browser extension which is used for the app.

### LoadJson.js

When running a web page with _JavaScript_ locally, many browsers disable the ability to load _JSON_ data files. The _jQuery_ `get` function, which is used in _Web Historian_, would give an error. This file overrides the `get` function and bypasses the loading of _JSON_ files by defining the data as variables and passing these on directly.

### Standalone[OS][Browser].py

These _Python_ scripts contain the configurations to create standalone versions of _Web Historian_ for various OS's and various browsers. It imports the _GenerateStandalone.py_ script and subsequently runs the `generateStandalone` function.