#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk
import webkit
import jswebkit



class GDorkTextView(gtk.TextView):
    def add_gdork(self, gdork):
        i = self.get_all_text().find(gdork)
        if i < 0:
            buff = self.get_buffer()
            buff.insert(buff.get_end_iter(), ' ' + gdork)


    def get_all_text(self):
        buff = self.get_buffer()
        bounds = buff.get_bounds()
        return buff.get_text(bounds[0], bounds[1]).replace("\n", " ")



class WebViewJs(webkit.WebView):
    def eval_js(self, js):
        frame = self.get_main_frame ()
        ctx = jswebkit.JSContext (frame.get_global_context ())
        r = ctx.EvaluateScript (js)
        return r


    get_html = lambda self: self.eval_js("document.documentElement.innerHTML;")



class ScrapeTab(gtk.VBox):
    def __init__(self):
        super(ScrapeTab, self).__init__()

        # dork textview with label
        self.tv_gdork = GDorkTextView()
        self.tv_gdork.show()
        self.tv_gdork.set_wrap_mode(gtk.WRAP_WORD)
        sw = gtk.ScrolledWindow()
        sw.show()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.tv_gdork)

        vb_dork = gtk.VBox()
        vb_dork.show()
        lbl = gtk.Label("Google Dork:")
        lbl.show()
        lbl.set_alignment(0, 0)
        vb_dork.pack_start(lbl, False, False, 2)
        vb_dork.pack_start(sw, True, True, 2)

        # pack buttons together
        self.btn_search = gtk.Button()
        self.btn_search.set_label("S_earch")
        self.btn_search.show()

        self.btn_clear = gtk.Button()
        self.btn_clear.set_label("_Clear")
        self.btn_clear.show()

        self.btn_scrape_page = gtk.Button()
        self.btn_scrape_page.set_label("Scrape _Page")
        self.btn_scrape_page.show()

        self.btn_scrape_all = gtk.Button()
        self.btn_scrape_all.set_label("Scrape _All")
        self.btn_scrape_all.show()

        vb_buttons = gtk.VBox()
        vb_buttons.show()
        for i in (self.btn_search, self.btn_clear, self.btn_scrape_page, self.btn_scrape_all):
            vb_buttons.pack_start(i, False, False, 2)

        # top
        hb_top = gtk.HBox()
        hb_top.show()
        hb_top.pack_start(vb_dork, True, True, 2)
        hb_top.pack_end(vb_buttons, False, False, 2)

        # webview controls
        self.btn_prev = gtk.Button()
        self.btn_prev.show()
        self.btn_prev.set_label(gtk.STOCK_GO_BACK)
        self.btn_prev.set_use_stock(True)

        self.btn_next = gtk.Button()
        self.btn_next.show()
        self.btn_next.set_label(gtk.STOCK_GO_FORWARD)
        self.btn_next.set_use_stock(True)

        self.btn_reload = gtk.Button()
        self.btn_reload.show()
        self.btn_reload.set_label(gtk.STOCK_REFRESH)
        self.btn_reload.set_use_stock(True)

        self.btn_home = gtk.Button()
        self.btn_home.show()
        self.btn_home.set_label(gtk.STOCK_HOME)
        self.btn_home.set_use_stock(True)

        self.btn_stop = gtk.Button()
        self.btn_stop.show()
        self.btn_stop.set_label(gtk.STOCK_STOP)
        self.btn_stop.set_use_stock(True)

        self.pb_load = gtk.ProgressBar()
        self.pb_load.show()
        self.pb_load.set_fraction(0)

        self.hb_load = gtk.HBox()
        self.hb_load.pack_start(self.btn_stop, False, False, 2)
        self.hb_load.pack_end(self.pb_load, True, True, 2)

        hb_wvctrl = gtk.HBox()
        hb_wvctrl.show()
        for i in (self.btn_prev, self.btn_next, self.btn_reload, self.btn_home):
            hb_wvctrl.pack_start(i, False, False, 2)
        hb_wvctrl.pack_start(self.hb_load, True, True, 2)

        # webview
        self.webview = WebViewJs()
        self.webview.show()
        self.webview.__prefs_stage__ = 0
        sw = gtk.ScrolledWindow()
        sw.show()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.webview)

        # add everything together
        self.pack_start(hb_top, False, False, 2)
        self.pack_start(hb_wvctrl, False, False, 2)
        self.pack_start(sw, True, True, 2)

