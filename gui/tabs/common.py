#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk



class CaseInsensitiveString(unicode):
    def __eq__(self, x):
        if self.lower() == x.lower():
            return True
        return False



class ResultsCommon(gtk.VBox):
    def __init__(self):
        super(ResultsCommon, self).__init__()

        # treeview
        self.tv_results = gtk.TreeView()
        self.tv_results.show()
        sw = gtk.ScrolledWindow()
        sw.show()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.tv_results)

        # buttons
        self.btn_include = gtk.Button()
        self.btn_include.set_label("_Include")
        self.btn_include.show()

        self.btn_exclude = gtk.Button()
        self.btn_exclude.set_label("E_xclude")
        self.btn_exclude.show()

        self.hb_bottom = gtk.HBox()
        self.hb_bottom.pack_end(self.btn_exclude, False, False, 2)
        self.hb_bottom.pack_end(self.btn_include, False, False, 2)
        self.hb_bottom.show()

        # pack everything together
        self.pack_start(sw, True, True, 2)
        self.pack_end(self.hb_bottom, False, False, 2)

        self.__build_store__()
        self.__main_dict__ = {}


    COLUMN_NAME = "Results"


    def __build_store__(self):
        self.store = gtk.TreeStore(str)
        col = gtk.TreeViewColumn(self.COLUMN_NAME, gtk.CellRendererText(), text = 0)
        self.tv_results.append_column(col)
        self.tv_results.set_model(self.store)


    def __get_node__(self, link):
        pass


    def __find_node__(self, parent_node, link):
        childnode = self.store.iter_children(parent_node)
        while childnode:
            if link.lower() == self.store.get_value(childnode, 0).lower():
                break
            childnode = self.store.iter_next(childnode)
        return childnode


    def append(self, links):
        for l in links:
            node = self.__get_node__(l)
            links[l][self.COLUMN_NAME.lower()] = self.store.append(node, [l])


    def remove(self, links):
        for l in links:
            node = links[l][self.COLUMN_NAME.lower()]
            pnode = self.store.iter_parent(node)
            self.store.remove(node)
            if not self.store.iter_n_children(pnode):
                self.store.remove(pnode)


    get_selected = lambda self: self.tv_results.get_selection().get_selected()


    def get_selected_text(self):
        tm, ti = self.get_selected()
        return tm.get_value(ti, 0)


    def clear(self):
        self.store.clear()
        self.__main_dict__ = {}




