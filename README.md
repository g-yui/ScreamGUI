# ScreamGUI
A simple GUI to automatically copy [acidicoala's ScreamAPI](https://github.com/acidicoala/ScreamAPI) to a target game, written on Python.

# Features
- Simple to use GUI with automatic .url, .exe, .dll and folder detection for easier usage.
- Can patch up to two instances of the EOSSDK dll, as there isn't a need for more, whether they are 32 or 64 bit. 
- Fetches latest release of the API via PyGitHub.
- Clean installation, no unnecesary files will be left.
- Automatic UAC prompt.
- Themes! Using the ttkthemes library.

# Requirements
- Wget
- BeautifulSoup
- PyGitHub
- Python 3

# Known bugs
- The github API may cause a crash for exceeding the allowed traffic for a given IP. 
- Drives other than c:/ are not currently supported.

# Licenses 
- The ScreamAPI itself is under a CC zero license 
- Wget is under a Public Domain License 
- TtkThemes has various licenses, these being  BSD-2-clause-like Tcl License, GNU GPLv2+ and GNU GPLv3. 
- BeautifulSoup is under the MIT license 
- PyGitHub is under the LGPL-3.0 License

# Acknlowledgments 
Acidicoala for the invaluable help provided.<br />
Icon designed by Freepik from Flaticon.
