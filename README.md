Steam AppManifest generator
===========================

This is a short python script that tricks Steam for Linux into downloading non-Linux apps.

## How it works

When you tell Steam to download an app, it first checks whether a Linux version exists. If it doesn't exist, it tells you so ("[App] is not available on your current platform.") and doesn't do anything. If it exists, it creates an `appmanifest` file (which contains game meta-data: name, size on hard-disk, time of last update, etc), and then proceeds to download it.

I found that if the `appmanifest` file is created manually, Steam will still download the app regardless of platform. There are a minimum of three variables that have to be set in order for this to work. The first is the `AppID` -- the ID of the app you're trying to download. The second is the `Universe`. [Refer to the Valve Developer Wiki for more info.](https://developer.valvesoftware.com/wiki/SteamID#Universes_Available_for_Steam_Accounts) The last and the most magical one is the `StateFlags`. I couldn't find any documentation on this, but as far as I've figured out, setting this to `1026` tells the Steam client that this the app download has been paused but should be continued when Steam starts.

## Using the script

You need Python 3 and Python 3 GObject Bindings for the script to run.

* Debian and Ubuntu (and derivatives) don't have these installed by default. The packages are `python3` and `python3-gi`.
* ArchLinux and derivatives can install `python` and `python-gobject`.
* Fedora should have everything installed by default.

After you have installed these, [download `steam-manifest.py`.](https://raw2.github.com/dotfloat/steam-appmanifest/master/steam-manifest.py) Make the file executable (`$ chmod +x steam-manifest.py`) and start it. A dialog should appear. Type in your Steam Community ID in the top textbox and hit `Refresh`. Make sure your profile is publicly viewable. A list of titles should appear. Install the apps that you want by clicking the checkbox to the left of the Title (and AppID). After you finish, restart Steam.

## Manual

I created the python script for ease of use. However, it is also possible to create the `appmanifest` files manually, without the script.

1. Find the `AppID` of the app you're trying to download. This can be easily done by going on [SteamDB](http://steamdb.info) and searching for it.
2. Go to `~/.steam/steam/SteamApps` or wherever your main SteamApps folder is.
3. Create and open a new file called "`appmanifest_APPID.acf`", replace `APPID` with the actual AppID you found in Step 1.
4. Copy and paste the following and replace `APPID` (the all-caps one) with the one you found in Step 1:

```
    "AppState"
    {
      "AppID"  "APPID"
      "Universe" "1"
      "StateFlags" "1026"
    }
```

Save and restart Steam.
