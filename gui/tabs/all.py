#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk

from common import ResultsCommon



class AllTab(ResultsCommon):
    def __init__(self):
        super(AllTab, self).__init__()


    COLUMN_NAME = "All"

    def __build_store__(self):
        self.store = gtk.ListStore(str)
        col = gtk.TreeViewColumn(self.COLUMN_NAME, gtk.CellRendererText(), text = 0)
        col.set_sort_column_id(0)
        self.tv_results.append_column(col)
        self.tv_results.set_model(self.store)


    def append(self, links):
        for l in links:
            links[l]['all'] = self.store.append((l,))


    def remove(self, links):
        for l in links:
            self.store.remove(links[l][self.COLUMN_NAME.lower()])




