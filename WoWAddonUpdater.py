import zipfile, configparser
from io import *
from os.path import isfile
import SiteHandler
import packages.requests as requests
from tkinter import *
from tkinter import scrolledtext
from tkinter.ttk import *
import queue
from threading import Thread


def confirmExit():
    input('\nPress the Enter key to exit')
    exit(0)

def cleanupExit():
    # Do stuff to stop update thread.
    exit(0)



class AddonUpdater:
    def __init__(self):
        # Read config file
        if not isfile('config.ini'):
            print('Failed to read configuration file. Are you sure there is a file called "config.ini"?\n')
            confirmExit()

        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            self.WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
            self.INSTALLED_VERS_FILE = config['WOW ADDON UPDATER']['Installed Versions File']
            self.AUTO_CLOSE = config['WOW ADDON UPDATER']['Close Automatically When Completed']
        except Exception:
            print('Failed to parse configuration file. Are you sure it is formatted correctly?\n')
            confirmExit()

        if not isfile(self.ADDON_LIST_FILE):
            print('Failed to read addon list file. Are you sure the file exists?\n')
            confirmExit()

        if not isfile(self.INSTALLED_VERS_FILE):
            with open(self.INSTALLED_VERS_FILE, 'w') as newInstalledVersFile:
                newInstalledVers = configparser.ConfigParser()
                newInstalledVers['Installed Versions'] = {}
                newInstalledVers.write(newInstalledVersFile)
        self.initgui()
        return

    def initgui(self):
        self.textqueue = queue.Queue()
        self.progressqueue = queue.Queue()
        root = Tk()
        root.title("WoW Addon Updater")

        mainframe = Frame(root, padding="3 3 3 3")
        mainframe.grid(sticky=(N, W, E, S))
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        mainframe.rowconfigure(0, weight=1)
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=1)
        mainframe.columnconfigure(1, weight=1)
        mainframe.rowconfigure(2, weight=1)
        mainframe.columnconfigure(2, weight=1)

        Sizegrip(root).grid(row=3, sticky=(S,E))

        Label(mainframe, text="WoW Addon Updater", font=("Helvetica", 20)).grid(column=0, row=0, sticky=(N), columnspan=3)

        output_text = scrolledtext.ScrolledText(mainframe, width=110, height=20, wrap=WORD)
        output_text.grid(column=0, row=2, sticky=(N,S,E,W), columnspan=3)

        progressbar = Progressbar(mainframe, orient="horizontal", mode="determinate")
        progressbar.grid(column=0, row=3, sticky=(E,W), columnspan=3)
        with open(self.ADDON_LIST_FILE, "r") as fin:
            length = len(fin.read().splitlines())
            progressbar.configure(value=0, maximum = length)

        self.root = root
        self.output_text = output_text
        self.progressbar = progressbar

        self.cancelbutton = Button(mainframe, text="Cancel", command=cleanupExit)
        self.cancelbutton.grid(column=0, row=4)
        self.startbutton = Button(mainframe, text="Start", command=self.startUpdating)
        self.startbutton.grid(column=2, row=4)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        self.output_text.insert(END, 'Welcome to WoW Addon Updater. If you\'ve already made an in.txt file, click Start to begin.\n')
        self.updateGUI()
        return

    def updateGUI(self):
        try:
            text = self.textqueue.get_nowait()
            self.output_text.insert(END, '\n' + text)
        except queue.Empty:
            pass
        try:
            progress = self.progressqueue.get_nowait()
            self.progressbar.step()
        except queue.Empty:
            pass
        self.root.after(200, self.updateGUI)
        return

    def addtext(self, text):
        self.textqueue.put(str(text))
        print(str(text))
        return

    def addprogress(self):
        self.progressqueue.put("step")
        return

    def startUpdating(self):
        self.startbutton['state'] = DISABLED
        self.updatethread = Thread(target=self.update)
        self.updatethread.start()
        return

    def finishUpdating(self):
        self.startbutton['state'] = NORMAL
        return

    def update(self):
        # Main process (yes I formatted the project badly)
        uberlist = []
        with open(self.ADDON_LIST_FILE, "r") as fin:
            for line in fin:
                current_node = []
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                currentVersion = SiteHandler.getCurrentVersion(line)
                if currentVersion is None:
                    currentVersion = 'Not Available'
                current_node.append(line.split("/")[-1])
                current_node.append(SiteHandler.getCurrentVersion(line))
                installedVersion = self.getInstalledVersion(line)
                addonName = line.split('/').pop()
                self.addprogress()
                if not currentVersion == installedVersion:
                    self.addtext('Installing/updating addon: ' + addonName + ' to version: ' + currentVersion)
                    ziploc = SiteHandler.findZiploc(line)
                    self.getAddon(ziploc)
                    current_node.append(self.getInstalledVersion(line))
                    if currentVersion is not '':
                        self.setInstalledVersion(line, currentVersion)
                else:
                    self.addtext('Up to date: ' + addonName + ' version ' + currentVersion)
                    current_node.append("Up to date")
                uberlist.append(current_node)
        if self.AUTO_CLOSE == 'False':
            col_width = max(len(word) for row in uberlist for word in row) + 2  # padding
            print("".join(word.ljust(col_width) for word in ("Name","Iversion","Cversion")))
            for row in uberlist:
                print("".join(word.ljust(col_width) for word in row), end='\n')
        self.addtext('\n' + 'All done!')
        return

    def getAddon(self, ziploc):
        if ziploc == '':
            return
        try:
            r = requests.get(ziploc, stream=True)
            z = zipfile.ZipFile(BytesIO(r.content))
            z.extractall(self.WOW_ADDON_LOCATION)
        except Exception:
            self.addtext('Failed to download or extract zip file for addon. Skipping...\n')
            return

    def getInstalledVersion(self, addonpage):
        addonName = addonpage.replace('https://mods.curse.com/addons/wow/', '')
        addonName = addonName.replace('https://www.curseforge.com/wow/addons/', '')
        addonName = addonName.replace('https://wow.curseforge.com/projects/', '')
        addonName = addonName.replace('http://www.wowinterface.com/downloads/', '')
        installedVers = configparser.ConfigParser()
        installedVers.read(self.INSTALLED_VERS_FILE)
        try:
            return installedVers['Installed Versions'][addonName]
        except Exception:
            return 'version not found'

    def setInstalledVersion(self, addonpage, currentVersion):
        addonName = addonpage.replace('https://mods.curse.com/addons/wow/', '')
        addonName = addonName.replace('https://www.curseforge.com/wow/addons/', '')
        addonName = addonName.replace('https://wow.curseforge.com/projects/', '')
        addonName = addonName.replace('http://www.wowinterface.com/downloads/', '')
        installedVers = configparser.ConfigParser()
        installedVers.read(self.INSTALLED_VERS_FILE)
        installedVers.set('Installed Versions', addonName, currentVersion)
        with open(self.INSTALLED_VERS_FILE, 'w') as installedVersFile:
            installedVers.write(installedVersFile)


def main():
    addonupdater = AddonUpdater()
    addonupdater.root.mainloop()
    return


if __name__ == "__main__":
    # execute only if run as a script
    main()
