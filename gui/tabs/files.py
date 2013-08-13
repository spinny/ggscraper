#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk

from all import ResultsCommon


class FilesTab(ResultsCommon):

    COLUMN_NAME = "Files"


    __filename__ = lambda self, uri: uri.split('?')[0]


    def __get_node__(self, link):
        fn = self.__filename__(link)
        if fn in self.__main_dict__:
            node = self.__main_dict__[fn]
        else:
            node = self.store.append(None, [fn])
            self.__main_dict__[fn] = node
        return node




