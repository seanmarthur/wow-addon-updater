# wow-addon-updater - Now supports Tukui!

This utility provides an alternative to the Twitch/Curse client for management and updating of addons for World of Warcraft. The Twitch/Curse client is rather bloated and buggy, and comes with many features that most users will not ever use in the first place. This utility, however, is lightweight and makes it very easy to manage which addons are being updated, and to update them just by running a python script.

Changelog located in changelog.txt

## GUI
This version of wow-addon-updater use the primitive GUI from zurohki, if you don't want it to boot, change the config file "Use GUI" to False.

## First-time setup

This utility has two dependencies:

* A version of [Python](https://www.python.org/) 3 (Any version of Python 3 should do)

* The [requests](http://docs.python-requests.org/en/master/) module

Thanks to https://github.com/Saritus, the requests module is now included in the download as a package, so there is no longer any need to install those yourself. Just install Python 3, download this app, configure the utility, and double click "WoWAddonUpdater.py" to start.

## Configuring the utility

The "config.ini" file is used by the utility to find where to install the addons to, and where to get the list of mods from.

The default location to install the addons to is "D:\Jeux\World of Warcraft\_retail_\Interface\AddOns". If this is not the location where you have World of Warcraft installed, you will need to edit "config.ini" to point to your addons folder.

The default location of the addon list file is simply "addons.txt", but this file will not exist on your PC, so you should either create "addons.txt" in the same location as the utility, or name the file something else and edit "config.ini" to point to the new file.

The "config.ini" file also has two other properties that you may not need to change. "Installed Versions File" determines where to store the file that keeps track of the current versions of your addons, and I don't recommend changing that.

The "Close Automatically When Completed" property determines whether the window automatically closes when the process completes (both successfully and unsuccessfully). It defaults to "False" so that you can see if any errors occurred. If you run this utility as a scheduled job (e.g. upon startup, every x hours, etc), we recommend changing this to "True".

## Input file format

Whatever file you use for your list of mods needs to be formatted in a particular way. Each line corresponds to a mod, and the line just needs to contain the link to the Curse or WoWInterface page for the mod. For example:

    https://www.curseforge.com/wow/addons/world-quest-tracker
    https://www.curseforge.com/wow/addons/deadly-boss-mods
    https://www.curseforge.com/wow/addons/auctionator
    http://www.wowinterface.com/downloads/info24005-RavenousMounts.html
    
    
Each link needs to be the main page for the addon, as shown above.

There is a special syntax for TukUI & ElvUI mods should be added to the list like :

    https://www.tukui.org/+tukui
    https://www.tukui.org/+elvui

Example show both, use one or the other (or both I don't judge).

because the downloadable zip from this website contains a subfolder called "ElvUI" containing the actual mod.

### Install from github

There is no 'standard' for raw source code of addons in github repositories, so not all are guaranteed to work out of the box. We support these scenarios:

* addon at the root of the repo (i.e. the *.toc file is at the root)
* addon in a folder with the same name as the addon (i.e. the *.toc file is in a subfolder of the same name)

You **must** use the subfolder syntax for addons installed from github, like:

    https://github.com/cannonpalms/FasterLooting|FasterLooting
    https://github.com/Aviana/LunaUnitFrames|LunaUnitFrames


TODO: support installing from a named branch. Right now we assume the 'master' branch.

## macOS Installation Instructions - Thanks to https://github.com/melwan

1. Install Python 3 for macOS
2. Run get-pip.py (Run menu > Run Module)
3. Run get-requests.py (Run menu > Run Module)
4. Edit config.ini (using TextEdit.app)
5. Create in.txt (using TextEdit.app)
6. Run WoWAddonUpdater.py (Run menu > Run Module)

The standard addon location on macOS is /Applications/World of Warcraft/Interface/AddOns

*Note: To save to a .txt file in TextEdit, go to Preferences > "New Document" tab > Under the "Format" section, choose "Plain Text".*

## Running the utility

After configuring the utility and setting up your input file, updating your addons is as simple as double clicking the "WoWAddonUpdater.py" file.

*Note: The more addons you have in your list, the longer it will take to update them... Duh.*

## Contact info

Have any questions, concerns, issues, or suggestions for the utility? Feel free to either submit an issue through Github or email me at kuhnerdm@gmail.com. Please put in the subject line that this is for the WoW Addon Updater.

## Future plans

* Make a video guide detailing all the above information

* Update to the visual interface  - The actual UI is very barebone
    - Implement the ability to add a addon
    - General redesign
    - Logo



Thanks for checking this out; hopefully it helps a lot of you :)
