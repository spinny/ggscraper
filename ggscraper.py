#!/usr/bin/env python
## -*- coding: UTF -*-

import gtk

from gui.ggscraper import GtkGoogleScraper



if __name__ == "__main__":
    win_main = GtkGoogleScraper()
    win_main.show()

    gtk.main()




