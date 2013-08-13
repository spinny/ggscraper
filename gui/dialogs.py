#!/usr/bin/env python
# -*- coding: UTF8 -*-

import gtk



class AskToSaveDialog(gtk.Dialog):
    Q = "Exit without saving ?"

    def __init__(self, parent):
        super(AskToSaveDialog, self).__init__(self.Q,parent,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (
                gtk.STOCK_OK, gtk.RESPONSE_OK,
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_SAVE, gtk.RESPONSE_YES)
            )

        self.set_title(self.Q)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_response(gtk.RESPONSE_CANCEL)

        lbl = gtk.Label(self.Q)
        lbl.show()
        self.vbox.pack_start(lbl, False, False, 8)



class MessageBox(gtk.MessageDialog):
    def __init__(self, parent, msg):
        super(MessageBox, self).__init__(
            parent,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO,
            gtk.BUTTONS_OK,
            msg
            )



class BaseFileChooserDialog(gtk.FileChooserDialog):
    Q = ""
    A = None

    def __init__(self, parent):
        super(BaseFileChooserDialog, self).__init__(self.Q, parent, self.A, (
            gtk.STOCK_OK, gtk.RESPONSE_OK,
            gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
            ))
        self.set_title(self.Q)
        self.set_resizable(True)
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER)


    def run(self):
        r = super(BaseFileChooserDialog, self).run()
        if r == gtk.RESPONSE_OK:
            return True
        return False



class SaveAsDialog(BaseFileChooserDialog):
    Q = "Save as"
    A = gtk.FILE_CHOOSER_ACTION_SAVE

    def __init__(self, parent):
        super(SaveAsDialog, self).__init__(parent)
        self.set_do_overwrite_confirmation(True)



class OpenDialog(BaseFileChooserDialog):
    Q = "Open"
    A = gtk.FILE_CHOOSER_ACTION_OPEN

    def __init__(self, parent):
        super(OpenDialog, self).__init__(parent)



class CaptchaDialog(gtk.Dialog):
    Q = "Please enter the text in the CAPTCHA image"

    def __init__(self, parent):
        self.__parent__ = parent
        super(CaptchaDialog, self).__init__(self.Q, self.__parent__,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_OK, gtk.RESPONSE_OK, ))

        self.set_title(self.Q)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_response(gtk.RESPONSE_OK)
        self.connect("response", self.__dlg_response__)

        lbl = gtk.Label(self.Q)
        lbl.show()
        self.ed_captcha = gtk.Entry()
        self.ed_captcha.show()

        self.vbox.pack_start(lbl, False, False, 8)
        self.vbox.pack_end(self.ed_captcha, False, False, 2)


    def __fill_captcha__(self, captcha):
        self.__parent__.notebook.tab_scrape.webview.execute_script(
        """
document.getElementById('captcha').value = '%(c)s';
e = document.forms[0].submit.click();
""" % {'c':captcha})


    def __dlg_response__(self, widget, response_id):
        if response_id == gtk.RESPONSE_OK:
            self.__fill_captcha__(self.ed_captcha.get_text())



class AskForDork(gtk.Dialog):
    T = "Confirm dork"
    def __init__(self, parent, gdork):
        self.__parent__ = parent
        self.gdork = None
        super(AskForDork, self).__init__(self.T, self.__parent__,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            (gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))

        self.set_title(self.T)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_default_response(gtk.RESPONSE_OK)
        self.connect("response", self.__dlg_response__)

        lbl = gtk.Label("Dork:")
        lbl.set_alignment(0, 0.5)
        lbl.show()
        self.ed_gdork = gtk.Entry()
        self.ed_gdork.set_text(gdork)
        self.ed_gdork.show()

        self.vbox.pack_start(lbl, False, False, 2)
        self.vbox.pack_end(self.ed_gdork, True, True, 2)


    def __dlg_response__(self, widget, response_id):
        if response_id == gtk.RESPONSE_OK:
            self.gdork = self.ed_gdork.get_text()



