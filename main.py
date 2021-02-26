# Imports #
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import tkinter as tk
import tkinter.ttk as ttk
import urllib.request
import zipfile
from pathlib import Path
from shutil import copy
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

import wget
from bs4 import BeautifulSoup
from github import Github
from github import RateLimitExceededException
from ttkthemes import ThemedTk

# Licenses #

# Wget is under a Public Domain License #
# TtkThemes has various licenses, these being  BSD-2-clause-like Tcl License, GNU GPLv2+ and GNU GPLv3. #
# Material Icon used by the software licensed under the Apache License Version 2.0 #
# The ScreamAPI itself is under a CC zero license #
# BeautifulSoup is under the MIT license #
# PyGitHub is under the LGPL-3.0 License #
# Icon designed by Freepik from Flaticon" #


# Some Globals and definitions #

global directory
directory = False

global executable
executable = False

global renamed_64
global renamed_32
global renamed_32_2
global renamed_64_2
renamed_32 = None
renamed_64 = None
renamed_64_2 = None
renamed_32_2 = None

url_exe = None

replaced = None

EOS32_str = "EOSSDK-Win32-Shipping"
EOS64_str = "EOSSDK-Win64-Shipping"

filename_folder = None
filename_game = None

SixtyFour = None
ThirtyTwo = None

url = None
dll = None
exe = None

global g_dir
g_dir = None
game_name = None

architecture = None

repository = "acidicoala/ScreamAPI"

g = Github()


def rootkill():
    root.destroy()


def fin():
    sys.exit()


def restart_program():
    if directory:
        global filename_folder
        filename_folder = askdirectory(title='Select Folder')
        global g_dir
        g_dir = str(filename_folder)
    elif executable:
        global filename_game
        filename_game = askopenfilename(title='Select Game')
        g_dir = os.path.dirname(filename_game)


def center(win):  # Script from user Honest Abe from Stack Overflow
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    title_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + title_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def ask_directory():
    global filename_folder
    filename_folder = askdirectory(title='Select Folder')
    print('Variable filename_folder is: ' + filename_folder)
    rootkill()
    global directory
    directory = True


# I'm not very happy with this way of resetting the program, as it is a rather bruteforce approach, #
# but other options just wouldn't work for me, this may cause extra ram to be used, I hope it won't be a problem #


def reset():
    rootkill()
    subprocess.call([sys.executable, os.path.realpath(__file__)])
    sys.exit()


def ask_game():
    global filename_game
    g_or_dll = "Game or Dll"
    filename_game = str(askopenfilename(title='Select Game', filetypes=[(g_or_dll, ".exe"), (g_or_dll, ".dll"),
                                                                        (g_or_dll, ".url")]))
    print('The suffix of the variable filename_game is: ' + Path(filename_game).suffix)
    suffix = Path(filename_game).suffix

    if suffix == '.exe':
        global exe
        exe = True
        print('Exe found')
        global executable
        executable = True
        rootkill()

    elif suffix == ".dll":
        global dll
        dll = True
        print('Dll found')
        executable = True
        rootkill()
    elif suffix == ".url":
        print('Url file')
        global url
        url = True
        executable = True
        data = open(filename_game, mode='r')
        data_read = data.read()
        data_index = data_read.index("IconFile=")

        print(data_read[data_index:])

        exe = data_read[data_index:].replace('IconFile=', '')
        global url_exe
        url_exe = exe
        global replaced
        replaced = os.path.basename(exe)
        rootkill()

    else:
        tk.Tk().withdraw()
        tk.messagebox.showwarning('Error', 'The file selected is not an executable, please try again')
        reset()


def theme_ada():
    root.set_theme(theme_name='adapta')
    global Theme
    Theme = 'adapta'


def theme_arc():
    root.set_theme(theme_name='arc')
    global Theme
    Theme = 'arc'


def theme_black():
    root.set_theme(theme_name='black')
    global Theme
    Theme = 'black'


def theme_bree():
    root.set_theme(theme_name='breeze')
    global Theme
    Theme = 'breeze'


def theme_clear():
    root.set_theme(theme_name='clearlooks')
    global Theme
    Theme = 'clearlooks'


def theme_equilux():
    root.set_theme(theme_name='equilux')
    global Theme
    Theme = 'equilux'


def theme_plastik():
    root.set_theme(theme_name='plastik')
    global Theme
    Theme = 'plastik'


def theme_yaru():
    root.set_theme(theme_name='yaru')
    global Theme
    Theme = 'yaru'


def title():
    root.title('ScreamGUI')


def icon():
    root.iconbitmap('koala.ico')


# def icon():
# root.iconbitmap('Placeholder.ico')


# Defaults #

global Theme
Theme = 'Equilux'

# Start of script #

root = ThemedTk(theme=Theme)
frame = tk.Frame(root)
title()
icon()

# Menu #

menu_bar = tk.Menu(root)

theme_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label="Adapta", command=theme_ada)
theme_menu.add_command(label="Arc", command=theme_arc)
theme_menu.add_command(label="Black", command=theme_black)
theme_menu.add_command(label="Breeze", command=theme_bree)
theme_menu.add_command(label="Clearlooks", command=theme_clear)
theme_menu.add_command(label="Equilux", command=theme_equilux)
theme_menu.add_command(label="Plastik", command=theme_plastik)
theme_menu.add_command(label="Yaru", command=theme_yaru)

menu_bar.add_cascade(label="Themes", menu=theme_menu)

root.config(menu=menu_bar)

# Labels, Buttons and Definitions therein #

text = tk.StringVar()
text.set(
    'Welcome to the ScreamGUI, this program\'s purpose is to patch any game using the EOS SDK with the ScreamAPI '
    'created by acidicoala')
label = ttk.Label(textvariable=text)
label.pack(pady=15)


def please_select():
    exe_select = ttk.Button(frame, text='Select game\'s/EOSSDK\'s file', command=ask_game)
    root_select = ttk.Button(frame, text='Select game\'s main folder', command=ask_directory)
    exit_self = ttk.Button(frame, text="Exit", command=fin)
    text.set('Please select among the following options')
    button.destroy()
    button_2.destroy()

    frame.pack()

    # Can't center the label for some god forsaken reason #

    exit_self.pack(padx=25, side=tk.LEFT)
    exe_select.pack(padx=25, side=tk.LEFT)
    root_select.pack(padx=25, side=tk.LEFT)


button = ttk.Button(text="Continue", command=please_select)
button.pack(pady=2, side=tk.RIGHT, anchor=tk.SW)
button_2 = ttk.Button(text="Exit", command=fin)
button_2.pack(pady=2, side=tk.LEFT, anchor=tk.SE)

center(root)
root.mainloop()


# Check if not found #

def not_found():
    tk.Tk().withdraw()
    tk.messagebox.showerror('Error', 'Something went wrong, please try again.')
    restart_program()


if directory:
    if filename_folder:
        g_dir = str(filename_folder)
    else:
        if not filename_game and (directory is True or executable is True):
            not_found()
        # print('Directory problem') | this was used for debugging #
elif executable:
    if dll:
        g_dir = os.path.dirname(filename_game)
        tk.Tk().withdraw()
        tk.messagebox.showinfo('Warning',
                               'DLL detection is experimental, though it should work in most cases, '
                               'if this method does not work for you please try the game folder option instead.')
    elif url:
        g_dir = os.path.dirname(url_exe)
        print(url_exe)
        tk.Tk().withdraw()
        tk.messagebox.showinfo('Warning',
                               'Url detection is not recommended whatsoever, it is very likely to not work, please'
                               ' try other options instead if there are any errors.')
    elif filename_game:
        g_dir = os.path.dirname(filename_game)
        tk.Tk().withdraw()
        tk.messagebox.showinfo('Warning',
                               'Executable detection is experimental, though it will work in most cases, '
                               'if this method does not work for you please try the game folder option'
                               ' instead.')
    else:
        if not filename_folder and (directory is True or executable is True):
            not_found()
        # print('Exe problem') | this was used for debugging #

# These two are fairly simple, one is to check the number of times the EOSSDK is found and the other sets up a #
# dictionary, this will give me every path to the EOSSDK it can find in the architecture_check() #

times = 0
global d
d = {}


# Script contributed by acidicoala himself! Thank you so much!!! #
def architecture_check():
    global results, arch
    results = list(Path(r"" + g_dir + "").rglob(r"EOSSDK-Win*-Shipping.dll"))
    global architecture
    architecture = None
    for result in results:
        print('Result is: ' + str(result))
        d[result] = results
        global arch
        arch = tk.re.search(r'EOSSDK-Win(.*)-Shipping', str(result)).group(1)
        print(f'Architecture: {arch}')
        global times
        times = times + 1
        print("The time variable is: " + str(times))
        if "64" in str(arch):
            global SixtyFour
            SixtyFour = True
        if "32" in str(arch):
            global ThirtyTwo
            ThirtyTwo = True

        elif str("EOSSDK") not in str(results):
            print('EOSSDK not found')
            tk.Tk().withdraw()
            tk.messagebox.showerror('Not found',
                                    'No EOSSDK found in the specified location, make sure it exists and try again'
                                    ' or just exit the program')
            reset()
        else:
            print('EOSSDK found')


def arch_display():
    global architecture
    if SixtyFour and ThirtyTwo:
        architecture = "both"
    elif SixtyFour:
        architecture = "64"
    elif ThirtyTwo:
        architecture = "32"
    else:
        architecture = None


global patched
patched = False

n_of_patches = 0
check_if_patched = list(Path(r"" + g_dir + "").rglob(r"EOSSDK-Win*-Shipping_o.dll"))
for i in check_if_patched:
    patched = True
    n_of_patches = n_of_patches + 1

if patched:
    tk.Tk().withdraw()
    tk.messagebox.showinfo('Patch Found',
                           'The patched EOSSDK has been found ' + str(n_of_patches) + ' time(s), as such '
                                                                                      'this game seems to '
                                                                                      'have been already patched, if you only wish to update the ScreamAPI please just delete the \nEOSSDK-Win*-Shipping'
                                                                                      '_o.dll file from the folder and restart the program')
    sys.exit()

root = ThemedTk(theme=Theme)
title()
icon()
frame = tk.Frame(root)
frame.pack()

# Why do I have to define this again is beyond me #

menu_bar2 = tk.Menu(root)

theme_menu = tk.Menu(menu_bar2, tearoff=0)
theme_menu.add_command(label="Adapta", command=theme_ada)
theme_menu.add_command(label="Arc", command=theme_arc)
theme_menu.add_command(label="Black", command=theme_black)
theme_menu.add_command(label="Breeze", command=theme_bree)
theme_menu.add_command(label="Clearlooks", command=theme_clear)
theme_menu.add_command(label="Equilux", command=theme_equilux)
theme_menu.add_command(label="Plastik", command=theme_plastik)
theme_menu.add_command(label="Yaru", command=theme_yaru)

menu_bar2.add_cascade(label="Themes", menu=theme_menu)

root.config(menu=menu_bar2)

# I have no idea why I now have to wrap everything under the frame, otherwise it won't show up #
if executable:
    print('Executable detected')
    architecture_check()
    arch_display()
    if architecture is None:
        root.withdraw()
        tk.Tk().withdraw()
        tk.messagebox.showerror('Not found',
                                'No EOSSDK found in the specified location, make sure it exists and try again'
                                ' or just exit the program')
        reset()
    print('Architecture is: ' + str(architecture))
    print('Basename of filename_game is: ' + str(os.path.basename(filename_game)))

    if exe:
        game_name = str(os.path.basename(filename_game)).replace('.exe', '')
    elif dll:
        fileExt = r"*.exe"
        listing = list(pathlib.Path(g_dir).glob(fileExt))
        # I know there has to be a better way to do this, and that this is an eyesore, but it beats me. #
        game_name = str(listing).replace(g_dir, '').replace("[WindowsPath('", '').replace("')]", '').replace('/', '')
    elif url:
        game_name = str(replaced)
        if game_name is None:
            game_name = "None found?"
    if game_name is None:
        root.withdraw()
        tk.Tk().withdraw()
        tk.messagebox.showerror('Not found',
                                'No EOSSDK found in the specified location, make sure it exists and try again'
                                ' or just exit the program')
        reset()
    arch_display()
    # My IDE may make the following text a mess, honestly don't know why it does that.#

    label = ttk.Label(frame, text="The game selected is " + '"' + str(game_name) + '"' + " and the detected EOSSDK "
                                                                                         "corresponds to a " + str(
        architecture) + " bit architecture, do you wish to proceed?")

elif directory:
    print('Directory detected')
    architecture_check()
    arch_display()
    if architecture is None:
        root.withdraw()
        tk.Tk().withdraw()
        tk.messagebox.showerror('Not found',
                                'No EOSSDK found in the specified location, make sure it exists and try again'
                                ' or just exit the program')
        reset()
    print('Architecture is: ' + str(architecture))
    print('Basename of filename_folder is: ' + os.path.basename(filename_folder))
    folder_name = str(os.path.basename(filename_folder))

    # Architecture check , again my IDE keeps messing with the text, tried to fix it but it gets messed up again #
    # I cannot be bothered any longer to fix it  :') #
    if architecture is None:
        tk.Tk().withdraw()
        root.withdraw()
        tk.messagebox.showerror('Not found',
                                'No EOSSDK found in the specified location, make sure it exists and try again'
                                ' or just exit the program')
        reset()

    if architecture == "both":
        label = ttk.Label(frame, text='The folder selected is ' + '"' + folder_name + '"' + " and diverse instances of"
                                                                                            " the EOSSDK have been detected, being " + str(
            times) + " in total, with both 64 and a 32 bit architectures,"
                     "do you wish to patch all of them?")

    elif times > 1:
        label = ttk.Label(frame, text="The folder selected is " + '"' + folder_name + '"' + " and diverse instances of"
                                                                                            " the EOSSDK have been detected, being " + str(
            times) + " in total, all of which have a " + architecture +
                                      " bit architecture, do you wish to patch all of them?")

    else:
        label = ttk.Label(frame, text="The folder selected is " + '"' + folder_name + '"' + " and the detected EOSSDK "
                                                                                            "corresponds to a " + architecture + " bit architecture, do you wish to proceed?")

label.pack(pady=15, padx=45)

temp_dir = tempfile.TemporaryDirectory()
print("Temp Dir: " + temp_dir.name)

# This simply gets the listing of directories where the EOSSDK is located from the architecture_check function #
# The conversion to a string is absolutely necessary, otherwise it will launch an error #
est_list = list(set(d))
est_list.__str__()
dic_str = str(est_list)
# Still as bruteforce and ugly as ever, though it works, I guess (ﾉ´･ω･)ﾉ ﾐ ┸━┸ #
dic_str_just_path = dic_str.replace("WindowsPath", '').replace("')]", '')
dic_str_just_path_1_dot_1 = dic_str_just_path.replace("')", '').replace("]", '').replace("[", '').replace("('", '')
dic_str_just_path_2 = dic_str_just_path_1_dot_1


# Gets latest release with PyGitHub and downloads it using Wget, with some json and BS4 for decoding and reading #

def download_file():
    try:
        asset_one = g.get_repo(repository).get_latest_release().get_assets()[0]
        print('Variable asset_one is: ' + str(asset_one))
        print('asset_one.name is: ' + asset_one.name)
        print('asset_one.url is: ' + asset_one.url)
        print('Beginning file download with wget module')
        url_json = asset_one.url
        print('Variable url_json is: ' + url_json)
        url_req = urllib.request.urlopen(url_json)
        content = url_req.read()
        soup = BeautifulSoup(content, "html.parser")
        data = json.loads(str(soup))
        download_url = (str(data['browser_download_url']))
        try:
            print("Please standby...")
            scream_api = wget.download(download_url)
            os.rename(str(scream_api), "ScreamAPI_Latest.zip")

        except WindowsError:
            print('Windows Error')
    except RateLimitExceededException:
        root.withdraw()
        tk.Tk().withdraw()
        tk.messagebox.showerror('Rate exceeded', 'You have exceeded the GitHub API rate limit for this IP, please'
                                                 'change your IP or wait a few moments.')
        sys.exit()


# Use of temp_dir for temporary housing of the unzipped files and easier tracking of such #


def unzip():
    with zipfile.ZipFile("ScreamAPI_Latest.zip", "r") as zip_ref:
        zip_ref.extractall(temp_dir.name)
        print("Decompression successful")


real_dir = ''
real_dir2 = ''
two_dirs = False


def directory_check():
    # Works for now, with support for more than just the c:/ drive!!! #
    if str(",") in dic_str_just_path_2:
        global real_dir, real_dir2
        drive = str(pathlib.PureWindowsPath(real_dir).drive).upper()
        drive_2 = str(pathlib.PureWindowsPath(real_dir2).drive).upper()
        global usable_drive, usable_drive_2
        usable_drive = drive + "/"
        usable_drive_2 = drive_2 + "/"
        real_dir_index = dic_str_just_path_2.index(",")
        real_dir = dic_str_just_path_2[real_dir_index:].replace(',', '').strip()
        real_dir2_index = dic_str_just_path_2.index(",")
        real_dir2 = dic_str_just_path_2[:real_dir2_index].replace(',', '').strip()
        global two_dirs
        two_dirs = True

    else:
        real_dir = dic_str_just_path_2

# The name pretty much describes what this does, it renames the files and then copies. #

def copy():
    global Fatal, renamed_32, renamed_64, renamed_32_2, renamed_64_2
    Fatal = False

    global eos_64
    global eos_32
    global scr_ini

    eos_64 = str(temp_dir.name) + r"\EOSSDK-Win64-Shipping.dll"
    scr_ini = str(temp_dir.name) + r"\ScreamAPI.ini"
    eos_32 = str(temp_dir.name) + r"\EOSSDK-Win32-Shipping.dll"

    global self
    self = None

    global self2
    self2 = None

    # These two get the destination from the sauce ¬w¬ #

    def destiny():
        if EOS64_str in real_dir:
            global self
            self = str(real_dir.replace('EOSSDK-Win64-Shipping.dll', 'EOSSDK-Win64-Shipping_o.dll'))
            print('Self: ' + str(self))
        elif EOS32_str in real_dir:
            self = str(real_dir.replace('EOSSDK-Win32-Shipping.dll', 'EOSSDK-Win32-Shipping_o.dll'))
            print('Self: ' + str(self))
        else:
            global Fatal
            Fatal = True

    def destiny2():
        if EOS64_str in real_dir2:
            global self2
            self2 = str(real_dir2.replace('EOSSDK-Win64-Shipping.dll', 'EOSSDK-Win64-Shipping_o.dll'))
            print('Self2: ' + str(self2))
        elif EOS32_str in real_dir2:
            self2 = str(real_dir2.replace('EOSSDK-Win32-Shipping.dll', 'EOSSDK-Win32-Shipping_o.dll'))
            print('Self2: ' + str(self2))
        else:
            global no_dir_2
            no_dir_2 = True

    destiny()
    destiny2()

    # Checks for self2 working as intended #

    if real_dir2 is None:
        print('No real_dir2 found')
    if self2 is None:
        if EOS64_str in real_dir2:
            self2 = str(real_dir2.replace('EOSSDK-Win64-Shipping.dll', 'EOSSDK-Win64-Shipping_o.dll'))
            print('Self: ' + str(self2))
        elif EOS32_str in real_dir2:
            self2 = str(real_dir2.replace('EOSSDK-Win32-Shipping.dll', 'EOSSDK-Win32-Shipping_o.dll'))
            print('Self: ' + str(self2))
        else:
            global no_dir_2
            no_dir_2 = True

    destination = str(self)
    destination2 = str(self2)
    global path_destination
    global path_destination2

    path_destination = None
    path_destination2 = None

    if EOS32_str in destination:
        path_destination = str(self).replace('EOSSDK-Win32-Shipping_o.dll', '')
    elif EOS64_str in destination:
        path_destination = str(self).replace('EOSSDK-Win64-Shipping_o.dll', '')

    if EOS32_str in destination2:
        path_destination2 = str(self2).replace('EOSSDK-Win32-Shipping_o.dll', '')
    elif EOS64_str in destination2:
        path_destination2 = str(self2).replace('EOSSDK-Win64-Shipping_o.dll', '')

    print('Path destinations: Path one is (' + str(path_destination) + "), and Path two is (" + str(path_destination2) +
          ")")
    # This checks if the variable real_dir 2 (i.e, there are two EOSSDK's) does exist #

    if str(real_dir2) != '' and not None:
        try:
            print("real_dir2 is not '' and is not None")
            print(real_dir + destination)
            # Renaming real_dir's EOSSDK #
            os.rename(real_dir, destination)
            if EOS32_str in destination:
                renamed_32 = True
            elif EOS64_str in destination:
                renamed_64 = True

            print("real is: " + real_dir)
            print("real2 is: " + real_dir2)

            print('source is: ' + real_dir + " and source2 is: " + real_dir2)
            print('destination is: ' + destination + " and destination2 is: " + destination2)

            os.rename(real_dir2, destination2)
            if str(EOS32_str) in str(destination2):
                renamed_32_2 = True
            elif str(EOS64_str) in str(destination2):
                renamed_64_2 = True

            # Copying files #
            if renamed_32:
                shutil.copy(eos_32, path_destination), shutil.copy(scr_ini, path_destination)
            if renamed_64:
                shutil.copy(eos_64, path_destination), shutil.copy(scr_ini, path_destination)
            if renamed_32_2:
                shutil.copy(eos_32, path_destination2), shutil.copy(scr_ini, path_destination2)
            if renamed_64_2:
                shutil.copy(eos_64, path_destination2), shutil.copy(scr_ini, path_destination2)

        except FileExistsError:
            print('File Already Exists')
        except FileNotFoundError:
            print('Something wasn\'t found')
            print(FileNotFoundError)
        except PermissionError:
            tk.Tk().withdraw()
            tk.messagebox.showerror('Access Denied', 'Please restart the program as administrator')
            sys.exit()
        finally:
            print('Copying done')

    if str(real_dir2) == '' or real_dir2 is None:
        try:
            print("real_dir_2 is equal to '' or is None")
            # Renaming real_dir2's EOSSDK #
            os.rename(real_dir, destination)
            if str("EOSSDK-Win32-Shipping") in str(destination):
                renamed_32 = True
            elif str("EOSSDK-Win64-Shipping") in str(destination):
                renamed_64 = True
            if renamed_32:
                shutil.copy(eos_32, path_destination), shutil.copy(scr_ini, path_destination)
            if renamed_64:
                shutil.copy(eos_64, path_destination), shutil.copy(scr_ini, path_destination)
        except FileExistsError:
            print('File Already Exists')
        except FileNotFoundError:
            print('Something wasn\'t found')
            print(FileNotFoundError)
        except WindowsError:
            tk.Tk().withdraw()
            tk.messagebox.showerror('Access Denied', 'Please restart the program as administrator')
            sys.exit()
        finally:
            print('Copying done')

    printer()

    if not Fatal:
        tk.Tk().withdraw()
        tk.messagebox.showinfo('Done!', 'The game has been patched!')
        sys.exit()
    if Fatal:
        tk.Tk().withdraw()
        tk.messagebox.showerror('Fatal', 'Something went very wrong, please try again!')
        reset()


# Main purpose for this one is debugging #
def printer():
    print('eos_64 is: ' + eos_64)
    print('eos_32 is: ' + eos_32)
    print('scr_ini is: ' + scr_ini)


def patcher():
    print('real_dir without the label is: ' + real_dir.replace('EOSSDK-Win64-Shipping.dll', ''))
    tk.Tk().withdraw()
    tk.messagebox.showinfo('Patching', 'The process will begin now')
    root.withdraw()
    download_file()
    unzip()
    os.remove("ScreamAPI_Latest.zip")
    print('The zip file has been removed')
    directory_check()
    copy()


directory_check()

button = ttk.Button(frame, text="Yes", command=patcher)
button.pack(pady=2, side=tk.RIGHT, anchor=tk.SW)

button2 = ttk.Button(frame, text="No", command=reset)
button2.pack(pady=2, side=tk.LEFT, anchor=tk.SE)

center(root)
root.mainloop()
