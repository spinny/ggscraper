#!/usr/bin/env python
## -*- coding: UTF -*-

import gtk

import google

from tabs.scrape import ScrapeTab
from tabs.domains import DomainsTab
from tabs.filetypes import FiletypesTab
from tabs.files import FilesTab
from tabs.all import AllTab



class MainNotebook(gtk.Notebook):
    def __init__(self):
        super(MainNotebook, self).__init__()

        self.tab_scrape = ScrapeTab()
        self.tab_scrape.show()
        l = gtk.Label("Scrape")
        self.append_page(self.tab_scrape, l)

        self.tab_domains = DomainsTab()
        self.tab_domains.show()
        l = gtk.Label("Domains")
        self.append_page(self.tab_domains, l)

        self.tab_filetypes = FiletypesTab()
        self.tab_filetypes.show()
        l = gtk.Label("Filetypes")
        self.append_page(self.tab_filetypes, l)

        self.tab_files = FilesTab()
        self.tab_files.show()
        l = gtk.Label("Files")
        self.append_page(self.tab_files, l)

        self.tab_all = AllTab()
        self.tab_all.show()
        l = gtk.Label("All")
        self.append_page(self.tab_all, l)



class MainWindow(gtk.Window):
    def __build_menu__(self, root, items):
        for i in items:
            if not i["label"]:
                t = gtk.SeparatorMenuItem()
                t.show()
                root.append(t)
            else:
                t = gtk.MenuItem()
                t.set_use_underline(True)
                t.set_label(i["label"])
                t.show()
                if "connect" in i:
                    t.connect(*i["connect"])
                if "accel" in i:
                    key, mod = gtk.accelerator_parse(i["accel"])
                    t.add_accelerator("activate", self.accel_group, key, mod, gtk.ACCEL_VISIBLE)
                if "sub" in i:
                    tt = gtk.Menu()
                    tt.show()
                    self.__build_menu__(tt, i["sub"])
                    t.set_submenu(tt)
                root.append(t)


    def __init__(self):
        super(MainWindow, self).__init__()

        # set window properties
        self.set_title("GTK Google Scraper")
        self.set_position(gtk.WIN_POS_CENTER)
        scr = self.get_screen()
        self.set_default_size(int(scr.get_width() * 0.8), int(scr.get_height() * 0.8))

        # add accelerator group
        self.accel_group = gtk.AccelGroup()
        self.add_accel_group(self.accel_group)

        # build menu bar
        self.mnu_main = gtk.MenuBar()
        self.mnu_main.show()
        self.__build_menu__(self.mnu_main, [
            {"label":"_File", "sub":[
                {
                    "label":"_New",
                    "connect":("activate", self.__mnu_main_new__),
                    "accel":"<Control>N"
                },
                {"label":None},
                {
                    "label":"_Save",
                    "connect":("activate", self.__mnu_main_save__),
                    "accel":"<Control>S"
                },
                {
                    "label":"Save _As",
                    "connect":("activate", self.__mnu_main_save_as__),
                    "accel":"<Control>E"
                },
                {
                    "label":"_Open",
                    "connect":("activate", self.__mnu_main_open__),
                    "accel":"<Control>O"
                },
                {"label":None},
                {
                    "label":"_Quit",
                    "connect":("activate", self.__win_main_on_delete_event__),
                    "accel":"<Control>Q"
                }
                ]}
            ])

        # build notebook
        self.notebook = MainNotebook()
        self.notebook.show()

        # build status bar
        self.status_bar = gtk.Statusbar()
        self.status_bar.show()

        # main VBox
        vb = gtk.VBox()
        vb.pack_start(self.mnu_main, False, False, 2)
        vb.pack_start(self.notebook, True, True, 2)
        vb.pack_end(self.status_bar, False, False, 2)
        vb.show()
        self.add(vb)

        # set google preferences
        self.notebook.tab_scrape.webview.load_uri("http://www.google.com/ncr")


