#!/usr/bin/env python
## -*- coding: UTF -*-

import gtk
import urllib
import time

import google

from main_window import MainWindow
from dialogs import *
from tabs.common import CaseInsensitiveString


class EmptyResult(dict):
    def __init__(self, arg = None):
        if arg:
            super(EmptyResult, self).__init__(arg)
        else:
            super(EmptyResult, self).__init__()
        self.update({'domains':None, 'filetypes':None, 'files':None, 'all':None})



class GtkGoogleScraper(MainWindow):
    def __init__(self):
        super(GtkGoogleScraper, self).__init__()
        self.__connect__()
        self.__filename__ = None
        self.results = {}
        self.results_saved = True


    def __connect__(self):
        # main window delete evemt
        self.connect("delete-event", self.__win_main_on_delete_event__)

        # scraping buttons
        self.notebook.tab_scrape.btn_search.connect("clicked", self.__btn_search_clicked__)
        self.notebook.tab_scrape.btn_clear.connect("clicked", lambda w: self.notebook.tab_scrape.tv_gdork.get_buffer().set_text(""))
        self.notebook.tab_scrape.btn_scrape_page.connect("clicked", self.__btn_scrape_page_clicked__)
        self.notebook.tab_scrape.btn_scrape_all.connect("clicked", self.__btn_scrape_all_clicked__)

        # webview controls
        self.notebook.tab_scrape.btn_prev.connect("clicked", lambda w: self.notebook.tab_scrape.webview.go_back())
        self.notebook.tab_scrape.btn_next.connect("clicked", lambda w: self.notebook.tab_scrape.webview.go_forward())
        self.notebook.tab_scrape.btn_reload.connect("clicked", lambda w: self.notebook.tab_scrape.webview.reload())
        self.notebook.tab_scrape.btn_stop.connect("clicked", lambda w: self.notebook.tab_scrape.webview.stop_loading())
        self.notebook.tab_scrape.btn_home.connect("clicked", lambda w: self.notebook.tab_scrape.webview.load_uri("http://google.com/ncr"))

        # webview
        self.notebook.tab_scrape.webview.connect("grab-focus", lambda w: w.emit_stop_by_name("grab-focus"))
        self.notebook.tab_scrape.webview.connect("load-started", self.__webview_start_loading__)
        self.notebook.tab_scrape.webview.connect("load-finished", lambda w, wf: self.notebook.tab_scrape.hb_load.hide())
        self.notebook.tab_scrape.webview.connect("load-progress-changed", self.__webview_load_progress__)
        self.notebook.tab_scrape.webview.connect("load-error", lambda w, a, b, c: self.notebook.tab_scrape.hb_load.hide())
        self.notebook.tab_scrape.webview.connect("load-finished", self.__webview_load_finished__)
        self.notebook.tab_scrape.webview.connect("load-finished", self.__webview_setup_google_prefs__)

        # refresh button in filetypes tab
        self.notebook.tab_filetypes.btn_refresh.connect("clicked", self.__btn_refresh_clicked__)

        # include / exclude buttons in "domains", "filetypes", "files" and "all" tabs
        self.notebook.tab_all.btn_include.connect("clicked", self.__btn_all_include__)
        self.notebook.tab_all.btn_exclude.connect("clicked", self.__btn_all_exclude__)
        self.notebook.tab_domains.btn_include.connect("clicked", self.__btn_domain_include__)
        self.notebook.tab_domains.btn_exclude.connect("clicked", self.__btn_domain_exclude__)
        self.notebook.tab_filetypes.btn_include.connect("clicked", self.__btn_filetype_include__)
        self.notebook.tab_filetypes.btn_exclude.connect("clicked", self.__btn_filetype_exclude__)
        self.notebook.tab_files.btn_include.connect("clicked", self.__btn_files_include__)
        self.notebook.tab_files.btn_exclude.connect("clicked", self.__btn_files_exclude__)

        # accelerators
        key, mod = gtk.accelerator_parse("<Control>C")
        self.accel_group.connect_group(key, mod, gtk.ACCEL_VISIBLE, self.__ctrl_c__)
        key, mod = gtk.accelerator_parse("<Control>D")
        self.accel_group.connect_group(key, mod, gtk.ACCEL_VISIBLE, self.__ctrl_d__)


    def __webview_start_loading__(self, widget, webframe):
        self.notebook.tab_scrape.pb_load.set_fraction(0)
        self.notebook.tab_scrape.hb_load.show()


    def __webview_load_progress__(self, widget, gint):
        self.notebook.tab_scrape.pb_load.set_fraction(float(gint) / 100)


    def __mnu_main_new__(self, widget):
        # new
        self.results = {}
        self.results_saved = True
        self.__filename__ = None
        for i in (self.notebook.tab_all, self.notebook.tab_domains, self.notebook.tab_filetypes, self.notebook.tab_files):
            i.clear()


    def __mnu_main_save_as__(self, widget):
        self.__filename__ = None
        self.__mnu_main_save__(widget)


    def __mnu_main_save__(self, widget):
        # save dialog
        if not self.__filename__:
            dlg = SaveAsDialog(self)
            if dlg.run():
                self.__filename__ = dlg.get_filename()
            dlg.destroy()
        if not self.__filename__:
            return
        f = file(self.__filename__, "w")
        for i in self.results:
            f.write(i + "\n")
        f.close()
        self.results_saved = True


    def __mnu_main_open__(self, widget):
        # open dialog
        dlg = OpenDialog(self)
        if dlg.run():
            f = dlg.get_filename()
        dlg.destroy()
        self.__mnu_main_new__(widget)
        self.__filename__ = f
        f = file(self.__filename__)
        lines = [CaseInsensitiveString(i.strip()) for i in f.readlines()]
        f.close()
        l = {}
        for ll in lines:
            l[ll] = EmptyResult()
        self.__add_links__(l)
        self.results_saved = True


    def __win_main_on_delete_event__(self, widget, *args):
        # asks to save the results before closing the main window
        if self.results_saved:
            gtk.main_quit()
            return True
        d = AskToSaveDialog(self)
        dlg_res = d.run()
        d.destroy()
        if dlg_res == gtk.RESPONSE_OK:
            gtk.main_quit()
        elif dlg_res == gtk.RESPONSE_YES:
            if self.__mnu_main_save__(widget):
                gtk.main_quit()
            else:
                return True
        else:
            return True


    def __webview_load_finished__(self, widget, webframe):
        if self.__got_captcha__():
            dlg = CaptchaDialog(self)
            dlg.run()
            dlg.destroy()



    def __webview_setup_google_prefs__(self, widget, webframe):
        # setup google preferences
        widget.emit_stop_by_name("load-finished")
        if widget.__prefs_stage__ == 0:
            widget.load_uri("http://www.google.com/preferences")
            widget.__prefs_stage__ += 1
        elif widget.__prefs_stage__ == 1:
            widget.disconnect_by_func(self.__webview_setup_google_prefs__)
            widget.load_uri(google.get_preferences_link(widget.get_html()))


    def __btn_search_clicked__(self, widget):
        # search button
        url = "http://www.google.com/search?num=100&hl=en&safe=off&filter=0&btnG=Search&start=0&"
        url += urllib.urlencode({'q':self.notebook.tab_scrape.tv_gdork.get_all_text()})
        self.notebook.tab_scrape.webview.load_uri(url)


    def __filter_links__(self, links):
        r = {}
        for i in links:
            l = CaseInsensitiveString(i)
            if not l in self.results:
                r[l] = EmptyResult()
        return r


    __get_links__ = lambda self: self.__filter_links__(google.LinkScraper(self.notebook.tab_scrape.webview.get_html()))
    __got_captcha__ = lambda self: self.notebook.tab_scrape.webview.get_html().find("To continue, please type the characters below:") >= 0
    __scrape_current_page__ = lambda self: self.__add_links__(self.__get_links__())


    def __add_links__(self, links):
        self.results.update(links)
        if len(links):
            self.results_saved = False
        for i in self.__enum_tabs__():
            i.append(links)
        return len(links)


    def __btn_scrape_page_clicked__(self, widget):
        dlg = MessageBox(self, str(self.__scrape_current_page__()) + " links added")
        dlg.run()
        dlg.destroy()


    def __auto_scrape__(self, widget, webframe):
        if not self.__got_captcha__():
            self.__link_count__ += self.__scrape_current_page__()
            if self.__pages__:
                l = self.__pages__.pop()
                self.notebook.tab_scrape.webview.load_uri(l)
            else:
                self.notebook.tab_scrape.webview.disconnect_by_func(self.__auto_scrape__)
                dlg = MessageBox(self, str(self.__link_count__) + " links added")
                dlg.run()
                dlg.destroy()


    def __btn_scrape_all_clicked__(self, widget):
        self.__pages__ = [str(i.href) for i in self.notebook.tab_scrape.webview.eval_js("document.getElementById('nav').getElementsByTagName('a')")]
        self.__link_count__ = 0
        self.notebook.tab_scrape.webview.connect("load-finished", self.__auto_scrape__)
        self.__auto_scrape__(widget, None)


    def __btn_refresh_clicked__(self, widget):
        self.notebook.tab_filetypes.clear()
        self.notebook.tab_filetypes.append(self.results)


    def __include_gdork(self, gdorktype, store, tview, show_dialog = True, add_double_quotes = False):
        i = tview.get_cursor()[0]
        if not i:
            return
        i = i[0]
        ed_txt = gdorktype
        if add_double_quotes:
            ed_txt += '"' + store[i][0] + '"'
        else:
            ed_txt += store[i][0]
        dlg = AskForDork(self, ed_txt)
        if dlg.run() == gtk.RESPONSE_OK:
            self.notebook.tab_scrape.tv_gdork.add_gdork(dlg.gdork)
        dlg.destroy()


    def __btn_all_include__(self, widget):
        self.__include_gdork('inurl:', self.notebook.tab_all.store, self.notebook.tab_all.tv_results, True, True)


    def __btn_all_exclude__(self, widget):
        self.__include_gdork('-inurl:', self.notebook.tab_all.store, self.notebook.tab_all.tv_results, True, True)


    def __btn_domain_include__(self, widget):
        self.__include_gdork('site:', self.notebook.tab_domains.store, self.notebook.tab_domains.tv_results)


    def __btn_domain_exclude__(self, widget):
        self.__include_gdork('-site:', self.notebook.tab_domains.store, self.notebook.tab_domains.tv_results)


    def __btn_filetype_include__(self, widget):
        self.__include_gdork('filetype:', self.notebook.tab_filetypes.store, self.notebook.tab_filetypes.tv_results)


    def __btn_filetype_exclude__(self, widget):
        self.__include_gdork('-filetype:', self.notebook.tab_filetypes.store, self.notebook.tab_filetypes.tv_results)


    def __btn_files_include__(self, widget):
        self.__include_gdork('inurl:', self.notebook.tab_files.store, self.notebook.tab_files.tv_results, True, True)


    def __btn_files_exclude__(self, widget):
        self.__include_gdork('-inurl:', self.notebook.tab_files.store, self.notebook.tab_files.tv_results, True, True)


    def __get_focus_tv_results__(self):
        for t in self.__enum_tabs__():
            if t.tv_results.is_focus():
                return t
        return None

    def __ctrl_c__(self, accelgroup, acceleratable, accel_key, accel_mods):
        tab = self.__get_focus_tv_results__()
        if tab:
            gtk.Clipboard().set_text(tab.get_selected_text())


    __enum_tabs__ = lambda self: iter((
        self.notebook.tab_domains,
        self.notebook.tab_filetypes,
        self.notebook.tab_files,
        self.notebook.tab_all
        ))


    def __ctrl_d__(self, accelgroup, acceleratable, accel_key, accel_mods):
        tab = self.__get_focus_tv_results__()
        if tab:
            delitem = tab.get_selected()
            if delitem[1]:
                ipath = delitem[0].get_path(delitem[1])
                if len(ipath) > 1 or tab == self.notebook.tab_all:
                    links = {tab.get_selected_text(): self.results[tab.get_selected_text()]}
                else:
                    links = {}
                    for i in tab.store[ipath].iterchildren():
                        links[i[0]] = self.results[i[0]]
                for t in self.__enum_tabs__():
                    t.remove(links)
                self.results_saved = False
                for l in links:
                    del self.results[l]





