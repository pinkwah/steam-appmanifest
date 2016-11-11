#!/usr/bin/env python3

# by dotfloat
# complaints go to dotfloat at gmail dot com

# Running:
# You need to have 'python3' and 'python3-gi' installed.
#
# On Debian/Ubuntu and derivatives, you have to run this:
# $ sudo apt-get install python3 python3-gi
#
# On ArchLinux and derivatives:
# $ sudo pacman -S python python-gobject
#

from gi.repository import Gtk
from xml.etree.ElementTree import ElementTree
from urllib.request import urlopen
from os import path, listdir, remove, system, popen
from os.path import isfile, join
import re

# Change this to where your SteamApps folder is located.
# The default ('~/.steam/steam/SteamApps') should be valid for all Linux installations.
# "~/.steam/steam" is a symlink to "$XDG_DATA_HOME/Steam" (normally "~/.local/share/Steam")
SteamApps = path.expanduser('~/.steam/steam/steamapps')

class DlgToggleApp(Gtk.Dialog):

    def __init__(self, parent, exists, appid, name):
        Gtk.Dialog.__init__(self, "Install appmanifest", parent, 0)
        self.set_default_size(300, 100)

        label0 = Gtk.Label("Install \""+ name +"\"?")
        label1 = Gtk.Label("appmanifest_"+ str(appid) +".acf")

        if exists:
            self.set_title("appmanifest already exists")
            self.add_buttons( "Cancel", Gtk.ResponseType.CANCEL,
                              "Delete anyway", Gtk.ResponseType.OK )
            label0.set_text("This will just remove the appmanifest file")
            label1.set_text("Use Steam to remove all of \""+ name +"\".")
        else:
            self.add_buttons("Cancel", Gtk.ResponseType.CANCEL,
                             "Install", Gtk.ResponseType.OK,)

        self.get_content_area().add(label0)
        self.get_content_area().add(label1)
        self.show_all()

class DlgManual(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Manually install appmanifest", parent, 0,
                           ("Cancel", Gtk.ResponseType.CANCEL,
                            "Install", Gtk.ResponseType.OK))

        self.set_default_size(200, 50)

        appidlabel = Gtk.Label("Game AppID:")
        self.appidentry = Gtk.Entry()

        appidhbox = Gtk.HBox()
        appidhbox.pack_start(appidlabel, False, False, True)
        appidhbox.pack_start(self.appidentry, False, False, True)

        instdirlabel = Gtk.Label("Game directory name:")
        self.instdirentry = Gtk.Entry()

        instdirhbox = Gtk.HBox()
        instdirhbox.pack_start(instdirlabel, False, False, True)
        instdirhbox.pack_start(self.instdirentry, False, False, True)

        vbox = Gtk.VBox()
        vbox.pack_start(appidhbox, False, False, True)
        vbox.pack_start(instdirhbox, False, False, True)

        self.get_content_area().add(vbox)
        self.show_all()

class AppManifest(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="appmanifest.acf Generator")

        self.set_default_size(480, 300)

        if not path.exists(SteamApps):
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                       Gtk.ButtonsType.OK, "Couldn't find a Steam install")
            dialog.format_secondary_text('Looked in "'+ SteamApps +'"')
            dialog.run()
            dialog.destroy()
            exit()

        # first row
        row0_label = Gtk.Label("https://steamcommunity.com/id/")
        self.steamid = Gtk.Entry()
        row0_btn = Gtk.Button("Refresh")

        row0_btn.connect("clicked", self.onRefreshClick)

        row0 = Gtk.Box(spacing=6)
        row0.pack_start(row0_label, True, True, 0)
        row0.pack_start(self.steamid, True, True, 0)
        row0.pack_start(row0_btn, True, True, 0)

        # second row
        row1 = Gtk.Label("Restart Steam for the changes to take effect.")

        # third row
        self.game_liststore = Gtk.ListStore(bool, int, str)

        row2_treeview = Gtk.TreeView(model=self.game_liststore)

        row2_renderer_text = Gtk.CellRendererText()
        row2_renderer_check = Gtk.CellRendererToggle()

        row2_col_toggle = Gtk.TreeViewColumn("", row2_renderer_check, active=0)
        row2_col_appid = Gtk.TreeViewColumn("AppID", row2_renderer_text, text=1)
        row2_col_title = Gtk.TreeViewColumn("Title", row2_renderer_text, text=2)

        row2_renderer_check.connect("toggled", self.onAppToggle)

        row2_treeview.append_column( row2_col_toggle )
        row2_treeview.append_column( row2_col_appid )
        row2_treeview.append_column( row2_col_title )

        row2 = Gtk.ScrolledWindow()
        row2.set_size_request(200, 400)
        row2.add(row2_treeview)

        # fourth row
        row3_manual = Gtk.Button("Manual")
        row3_quit = Gtk.Button("Quit")

        row3_manual.connect("clicked", self.onManualClick)
        row3_quit.connect("clicked", self.onQuitClick)

        row3 = Gtk.Box()
        row3.pack_start(row3_manual, True, True, 0)
        row3.pack_start(row3_quit, True, True, 0)

        # vbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        vbox.pack_start(row0, False, False, True)
        vbox.pack_start(row1, False, False, 0)
        vbox.pack_start(row2, True, True, 0)
        vbox.pack_start(row3, False, False, 0)

        self.add(vbox)

    # slots
    def onRefreshClick(self, widget):
        if not self.steamid.get_text():
            return

        files = [ f for f in listdir(SteamApps) if isfile(join(SteamApps,f)) ]
        appids = []

        for file in files:
            m = re.search(r"appmanifest_([0-9]+).acf", file)
            if m:
                appids.append( int( m.groups(1)[0] ) )

        url = "http://steamcommunity.com/id/"+ self.steamid.get_text() +"/games?tab=all&xml=1"
        html = urlopen(url)
        tree = ElementTree()
        tree.parse(html)
        games_xml = tree.getiterator('game')
        for game in games_xml:
            appid = int(game.find('appID').text)
            name = game.find('name').text
            exists = appid in appids
            self.game_liststore.append([exists, appid, name])

    def onAppToggle(self, widget, path):
        appid = self.game_liststore[path][1]
        name = self.game_liststore[path][2]
        exists = self.refreshSingleRow(path)

        dialog = DlgToggleApp(self, exists, appid, name)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            p = SteamApps + "/appmanifest_"+ str(appid) +".acf"
            if exists:
                remove(p)
            else:
                self.addGame( appid, name )
        dialog.destroy()

        self.refreshSingleRow(path)

    def onManualClick(self, widget):
        dialog = DlgManual(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.addGame( int(dialog.appidentry.get_text()), dialog.instdirentry.get_text() )

        dialog.destroy()

    def onQuitClick(self, widget):
        self.destroy()
        Gtk.main_quit()

    # other
    def refreshSingle(self, appid):
        p = SteamApps + "/appmanifest_"+ str(appid) +".acf"
        exists = path.isfile( p )

        for row in self.game_liststore:
            if row[1] == appid:
                row[0] = exists
                break

        return exists

    def refreshSingleRow(self, row):
        p = SteamApps + "/appmanifest_"+ str(self.game_liststore[row][1]) +".acf"
        exists = path.isfile( p )

        self.game_liststore    [row][0] = exists

        return exists

    def addGame(self, appid, name):
        p = SteamApps + "/appmanifest_"+ str(appid) +".acf"
        f = open(p, 'w')
        name = name.replace("/", "-")
        f.write( '"AppState"\n{\n\t"appid"\t"'+ str(appid) +'"\n\t"Universe"'+
                 '\t"1"\n\t"installdir"\t"'+ name +'"\n\t"StateFlags"\t"1026"\n}')
        f.close()

win = AppManifest()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
