#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk

from all import ResultsCommon



class FiletypesTab(ResultsCommon):
    DEFAULT_MAX_EXT_SIZE = 10

    def __init__(self):
        super(FiletypesTab, self).__init__()

        self.ed_filetype_size = gtk.Entry()
        self.ed_filetype_size.set_text(str(self.DEFAULT_MAX_EXT_SIZE))
        self.ed_filetype_size.set_max_length(2)
        self.ed_filetype_size.set_width_chars(3)
        self.ed_filetype_size.show()

        self.btn_refresh = gtk.Button("_Refresh")
        self.btn_refresh.show()

        l = gtk.Label("Max. extension size:")
        l.set_alignment(0, 0.5)
        l.show()

        self.hb_bottom.pack_start(l, False, False, 2)
        self.hb_bottom.pack_start(self.ed_filetype_size, False, False, 2)
        self.hb_bottom.pack_start(self.btn_refresh, False, False, 2)


    COLUMN_NAME = "Filetypes"


    def __get_max_extension_size__(self):
        t = self.ed_filetype_size.get_text()
        try:
            return int(t)
        except:
            self.ed_filetype_size.set_text(str(self.DEFAULT_MAX_EXT_SIZE))
            return self.DEFAULT_MAX_EXT_SIZE


    def __filetype__(self, l):
        ft = l.split("?")[0].split(".")[-1:][0]
        if (not ft or
            len(ft) > self.__get_max_extension_size__() or
            "/" in ft):
                return None
        return ft.lower()


    def __get_node__(self, link):
        ft = self.__filetype__(link)
        if not ft:
            ft = "No file type"
        if ft in self.__main_dict__:
            node = self.__main_dict__[ft]
        else:
            node = self.store.append(None, [ft])
            self.__main_dict__[ft] = node
        return node




