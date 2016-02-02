#!/usr/bin/env python
#-*- encoding: utf-8 -*-

"""
GUI front end for qrencode based on the work of David Green:
<david4dev@gmail.com> https://launchpad.net/qr-code-creator/
and inspired by
http://www.omgubuntu.co.uk/2011/03/how-to-create-qr-codes-in-ubuntu/
uses python-zbar for decoding from files and webcam
"""

import sys, os
from math import ceil
from PyQt4 import QtCore, QtGui
from qrtools import QR
try:
    import pynotify
    if not pynotify.init("QtQR"):
        print "DEBUG: There was a problem initializing the pynotify module"
    NOTIFY = True
except:
    NOTIFY = False
    
__author__ = "Ramiro Algozino"
__email__ = "algozino@gmail.com"
__copyright__ = "copyright (C) 2011 Ramiro Algozino"
__credits__ = "David Green"
__license__ = "GPLv3"
__version__ = "1.1"

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle(self.trUtf8("QtQR: QR Code Generator"))
        icon = os.path.join(os.path.dirname(__file__), u'icon.png')
        if not QtCore.QFile(icon).exists():
            icon = u'/usr/share/pixmaps/qtqr.png'
        self.setWindowIcon(QtGui.QIcon(icon))
        self.w = QtGui.QWidget()
        self.setCentralWidget(self.w)
        self.setAcceptDrops(True)

        # Templates for creating QRCodes supported by qrtools
        self.templates = {
            "text": unicode(self.trUtf8("Text")),
            "url": unicode(self.trUtf8("URL")),
            "bookmark": unicode(self.trUtf8("Bookmark")),
            "emailmessage": unicode(self.trUtf8("E-Mail")),
            "telephone": unicode(self.trUtf8("Telephone Number")),
            "phonebook": unicode(self.trUtf8("Contact Information (PhoneBook)")),
            "sms": unicode(self.trUtf8("SMS")),
            "mms": unicode(self.trUtf8("MMS")),
            "geo": unicode(self.trUtf8("Geolocalization")),
            }
        # With this we make the dict bidirectional
        self.templates.update( dict((self.templates[k], k) for k in self.templates))

        # Tabs
        # We use this to put the tabs in a desired order.
        self.templateNames = (
            self.templates["text"],
            self.templates["url"],
            self.templates["bookmark"],
            self.templates["emailmessage"],
            self.templates["telephone"],
            self.templates["phonebook"],
            self.templates["sms"],
            self.templates["mms"],
            self.templates["geo"],
            )
        self.selector = QtGui.QComboBox()
        self.selector.addItems(self.templateNames)
        self.tabs = QtGui.QStackedWidget()
        self.textTab = QtGui.QWidget()
        self.urlTab = QtGui.QWidget()
        self.bookmarkTab = QtGui.QWidget()
        self.emailTab = QtGui.QWidget()
        self.telTab = QtGui.QWidget()
        self.phonebookTab = QtGui.QWidget()
        self.smsTab = QtGui.QWidget()
        self.mmsTab = QtGui.QWidget()
        self.geoTab = QtGui.QWidget()
        self.tabs.addWidget(self.textTab)
        self.tabs.addWidget(self.urlTab)
        self.tabs.addWidget(self.bookmarkTab)
        self.tabs.addWidget(self.emailTab)
        self.tabs.addWidget(self.telTab)
        self.tabs.addWidget(self.phonebookTab)
        self.tabs.addWidget(self.smsTab)
        self.tabs.addWidget(self.mmsTab)
        self.tabs.addWidget(self.geoTab)

        #Widgets for Text Tab
        self.l1 = QtGui.QLabel(self.trUtf8('Text to be encoded:'))
        self.textEdit = QtGui.QPlainTextEdit()

        #Widgets for URL Tab
        self.urlLabel = QtGui.QLabel(self.trUtf8('URL to be encoded:'))
        self.urlEdit = QtGui.QLineEdit(u'http://')

        #Widgets for BookMark Tab
        self.bookmarkTitleLabel = QtGui.QLabel(self.trUtf8("Title:"))
        self.bookmarkTitleEdit = QtGui.QLineEdit()
        self.bookmarkUrlLabel = QtGui.QLabel(self.trUtf8("URL:"))
        self.bookmarkUrlEdit = QtGui.QLineEdit()

        #Widgets for EMail Tab
        self.emailLabel = QtGui.QLabel(self.trUtf8('E-Mail address:'))
        self.emailEdit = QtGui.QLineEdit("@.com")
        self.emailSubLabel = QtGui.QLabel(self.trUtf8('Subject:'))
        self.emailSubjectEdit = QtGui.QLineEdit()
        self.emailBodyLabel = QtGui.QLabel(self.trUtf8('Message Body:'))
        self.emailBodyEdit = QtGui.QPlainTextEdit()

        #Widgets for Telephone Tab
        self.telephoneLabel = QtGui.QLabel(self.trUtf8('Telephone Number:'))
        self.telephoneEdit = QtGui.QLineEdit()

        #Widgets for Contact Information Tab
        self.phonebookNameLabel = QtGui.QLabel(self.trUtf8("Name:"))
        self.phonebookNameEdit = QtGui.QLineEdit()
        self.phonebookTelLabel = QtGui.QLabel(self.trUtf8("Telephone:"))
        self.phonebookTelEdit = QtGui.QLineEdit()
        self.phonebookEMailLabel = QtGui.QLabel(self.trUtf8("E-Mail:"))
        self.phonebookEMailEdit = QtGui.QLineEdit()
        self.phonebookNoteLabel = QtGui.QLabel(self.trUtf8("Note:"))
        self.phonebookNoteEdit = QtGui.QLineEdit()
        self.phonebookBirthdayLabel = QtGui.QLabel(self.trUtf8("Birthday:"))
        self.phonebookBirthdayEdit = QtGui.QDateEdit()
        self.phonebookBirthdayEdit.setCalendarPopup(True)
        self.phonebookAddressLabel = QtGui.QLabel(self.trUtf8("Address:"))
        self.phonebookAddressEdit =  QtGui.QLineEdit()
        self.phonebookAddressEdit.setToolTip(self.trUtf8("Insert separated by commas the PO Box, room number, house number, city, prefecture, zip code and country in order"))
        self.phonebookUrlLabel = QtGui.QLabel(self.trUtf8("URL:"))
        self.phonebookUrlEdit =  QtGui.QLineEdit()

        #Widgets for SMS Tab
        self.smsNumberLabel = QtGui.QLabel(self.trUtf8('Telephone Number:'))
        self.smsNumberEdit = QtGui.QLineEdit()
        self.smsBodyLabel = QtGui.QLabel(self.trUtf8('Message:'))
        self.smsBodyEdit = QtGui.QPlainTextEdit()
        self.smsCharCount = QtGui.QLabel(self.trUtf8("characters count: 0"))

        #Widgets for MMS Tab
        self.mmsNumberLabel = QtGui.QLabel(self.trUtf8('Telephone Number:'))
        self.mmsNumberEdit = QtGui.QLineEdit()
        self.mmsBodyLabel = QtGui.QLabel(self.trUtf8('Content:'))
        self.mmsBodyEdit = QtGui.QPlainTextEdit()

        #Widgets for GEO Tab
        self.geoLatLabel = QtGui.QLabel(self.trUtf8("Latitude:"))
        self.geoLatEdit = QtGui.QLineEdit()
        self.geoLongLabel = QtGui.QLabel(self.trUtf8("Longitude:"))
        self.geoLongEdit = QtGui.QLineEdit()

        #Widgets for QREncode Parameters Configuration
        self.optionsGroup = QtGui.QGroupBox(self.trUtf8('Parameters:'))

        self.l2 = QtGui.QLabel(self.trUtf8('&Pixel Size:'))
        self.pixelSize = QtGui.QSpinBox()

        self.l3 = QtGui.QLabel(self.trUtf8('&Error Correction:'))
        self.ecLevel = QtGui.QComboBox()
        self.ecLevel.addItems(
                (
                self.trUtf8('Lowest'),
                self.trUtf8('Medium'), 
                self.trUtf8('QuiteGood'),
                self.trUtf8('Highest')
                )
            )

        self.l4 = QtGui.QLabel(self.trUtf8('&Margin Size:'))
        self.marginSize = QtGui.QSpinBox()

        #QLabel for displaying the Generated QRCode
        self.qrcode = QtGui.QLabel(self.trUtf8('Start typing to create QR Code\n or  drop here image files for decoding.'))
        self.qrcode.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.scroll = QtGui.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.qrcode)

        #Save and Decode Buttons
        self.saveButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'document-save'), self.trUtf8('&Save QRCode'))
        self.decodeButton = QtGui.QPushButton(QtGui.QIcon.fromTheme(u'preview-file'), self.trUtf8('&Decode'))

        self.decodeMenu = QtGui.QMenu()
        self.decodeFileAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'document-open'), self.trUtf8('Decode from &File'))
        self.decodeWebcamAction = self.decodeMenu.addAction(QtGui.QIcon.fromTheme(u'image-png'), self.trUtf8('Decode from &Webcam'))
        self.decodeButton.setMenu(self.decodeMenu)

        self.exitAction = QtGui.QAction(QtGui.QIcon.fromTheme(u'application-exit'), self.trUtf8('E&xit'), self)
        self.addAction(self.exitAction)
        self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme(u"help-about"), self.trUtf8("&About"), self)
        self.addAction(self.aboutAction)

        # UI Tunning
        self.saveButton.setEnabled(False)
        self.pixelSize.setValue(3)
        self.pixelSize.setMinimum(1)
        self.marginSize.setValue(4)
        self.l1.setBuddy(self.textEdit)
        self.l2.setBuddy(self.pixelSize)
        self.l3.setBuddy(self.ecLevel)
        self.l4.setBuddy(self.marginSize)
        self.ecLevel.setToolTip(self.trUtf8('Error Correction Level'))
        self.l3.setToolTip(self.trUtf8('Error Correction Level'))
        self.decodeFileAction.setShortcut(u"Ctrl+O")
        self.decodeWebcamAction.setShortcut(u"Ctrl+W")
        self.saveButton.setShortcut(u"Ctrl+S")
        self.exitAction.setShortcut(u"Ctrl+Q")
        self.aboutAction.setShortcut(u"F1")

        self.buttons = QtGui.QHBoxLayout()
        self.buttons.addWidget(self.saveButton)
        self.buttons.addWidget(self.decodeButton)

        #Text Tab
        self.codeControls = QtGui.QVBoxLayout()
        self.codeControls.addWidget(self.l1)
        self.codeControls.addWidget(self.textEdit, 1)
        self.textTab.setLayout(self.codeControls)

        #URL Tab
        self.urlTabLayout = QtGui.QVBoxLayout()
        self.urlTabLayout.addWidget(self.urlLabel)
        self.urlTabLayout.addWidget(self.urlEdit)
        self.urlTabLayout.addStretch()
        self.urlTab.setLayout(self.urlTabLayout)

        #Bookmark Tab
        self.bookmarkTabLayout = QtGui.QVBoxLayout()
        self.bookmarkTabLayout.addWidget(self.bookmarkTitleLabel)
        self.bookmarkTabLayout.addWidget(self.bookmarkTitleEdit)
        self.bookmarkTabLayout.addWidget(self.bookmarkUrlLabel)
        self.bookmarkTabLayout.addWidget(self.bookmarkUrlEdit)
        self.bookmarkTabLayout.addStretch()
        self.bookmarkTab.setLayout(self.bookmarkTabLayout)

        #Email Tab
        self.emailTabLayout = QtGui.QVBoxLayout()
        self.emailTabLayout.addWidget(self.emailLabel)
        self.emailTabLayout.addWidget(self.emailEdit)
        self.emailTabLayout.addWidget(self.emailSubLabel)
        self.emailTabLayout.addWidget(self.emailSubjectEdit)
        self.emailTabLayout.addWidget(self.emailBodyLabel)
        self.emailTabLayout.addWidget(self.emailBodyEdit, 1)
        self.emailTabLayout.addStretch()
        self.emailTab.setLayout(self.emailTabLayout)

        #Telephone Tab
        self.telTabLayout = QtGui.QVBoxLayout()
        self.telTabLayout.addWidget(self.telephoneLabel)
        self.telTabLayout.addWidget(self.telephoneEdit)
        self.telTabLayout.addStretch()
        self.telTab.setLayout(self.telTabLayout)

        #Contact Tab
        self.phonebookTabLayout = QtGui.QVBoxLayout()
        self.phonebookTabLayout.addWidget(self.phonebookNameLabel)
        self.phonebookTabLayout.addWidget(self.phonebookNameEdit)
        self.phonebookTabLayout.addWidget(self.phonebookTelLabel)
        self.phonebookTabLayout.addWidget(self.phonebookTelEdit)
        self.phonebookTabLayout.addWidget(self.phonebookEMailLabel)
        self.phonebookTabLayout.addWidget(self.phonebookEMailEdit)
        self.phonebookTabLayout.addWidget(self.phonebookNoteLabel)
        self.phonebookTabLayout.addWidget(self.phonebookNoteEdit)
        self.phonebookTabLayout.addWidget(self.phonebookBirthdayLabel)
        self.phonebookTabLayout.addWidget(self.phonebookBirthdayEdit)
        self.phonebookTabLayout.addWidget(self.phonebookAddressLabel)
        self.phonebookTabLayout.addWidget(self.phonebookAddressEdit)
        self.phonebookTabLayout.addWidget(self.phonebookUrlLabel)
        self.phonebookTabLayout.addWidget(self.phonebookUrlEdit)
        self.phonebookTabLayout.addStretch()
        self.phonebookTab.setLayout(self.phonebookTabLayout)

        #SMS Tab
        self.smsTabLayout = QtGui.QVBoxLayout()
        self.smsTabLayout.addWidget(self.smsNumberLabel)
        self.smsTabLayout.addWidget(self.smsNumberEdit)
        self.smsTabLayout.addWidget(self.smsBodyLabel)
        self.smsTabLayout.addWidget(self.smsBodyEdit, 1)
        self.smsTabLayout.addWidget(self.smsCharCount)
        self.smsTabLayout.addStretch()
        self.smsTab.setLayout(self.smsTabLayout)

        #MMS Tab
        self.mmsTabLayout = QtGui.QVBoxLayout()
        self.mmsTabLayout.addWidget(self.mmsNumberLabel)
        self.mmsTabLayout.addWidget(self.mmsNumberEdit)
        self.mmsTabLayout.addWidget(self.mmsBodyLabel)
        self.mmsTabLayout.addWidget(self.mmsBodyEdit, 1)
        self.mmsTabLayout.addStretch()
        self.mmsTab.setLayout(self.mmsTabLayout)

        #Geolocalization Tab
        self.geoTabLayout = QtGui.QVBoxLayout()
        self.geoTabLayout.addWidget(self.geoLatLabel)
        self.geoTabLayout.addWidget(self.geoLatEdit)
        self.geoTabLayout.addWidget(self.geoLongLabel)
        self.geoTabLayout.addWidget(self.geoLongEdit)
        self.geoTabLayout.addStretch()
        self.geoTab.setLayout(self.geoTabLayout)

        #Pixel Size Controls
        self.pixControls = QtGui.QVBoxLayout()
        self.pixControls.addWidget(self.l2)
        self.pixControls.addWidget(self.pixelSize)

        #Error Correction Level Controls
        self.levelControls = QtGui.QVBoxLayout()
        self.levelControls.addWidget(self.l3)
        self.levelControls.addWidget(self.ecLevel)

        #Margin Size Controls
        self.marginControls = QtGui.QVBoxLayout()
        self.marginControls.addWidget(self.l4)
        self.marginControls.addWidget(self.marginSize)

        #Controls Layout
        self.controls = QtGui.QHBoxLayout()
        self.controls.addLayout(self.pixControls)
        self.controls.addSpacing(10)
        self.controls.addLayout(self.levelControls)
        self.controls.addSpacing(10)
        self.controls.addLayout(self.marginControls)
        self.controls.addStretch()
        self.optionsGroup.setLayout(self.controls)

        #Main Window Layout
        self.selectorBox = QtGui.QGroupBox(self.trUtf8("Select data type:"))

        self.vlayout1 = QtGui.QVBoxLayout()
        self.vlayout1.addWidget(self.selector)
        self.vlayout1.addWidget(self.tabs, 1)

        self.vlayout2 = QtGui.QVBoxLayout()
        self.vlayout2.addWidget(self.optionsGroup)
        self.vlayout2.addWidget(self.scroll, 1)
        self.vlayout2.addLayout(self.buttons)

        self.layout = QtGui.QHBoxLayout(self.w)
        self.selectorBox.setLayout(self.vlayout1)
        self.layout.addWidget(self.selectorBox)
        self.layout.addLayout(self.vlayout2, 1)

        #Signals
        self.selector.currentIndexChanged.connect(self.tabs.setCurrentIndex)
        self.tabs.currentChanged.connect(self.selector.setCurrentIndex)
        self.textEdit.textChanged.connect(self.qrencode)
        self.urlEdit.textChanged.connect(self.qrencode)
        self.bookmarkTitleEdit.textChanged.connect(self.qrencode)
        self.bookmarkUrlEdit.textChanged.connect(self.qrencode)
        self.emailEdit.textChanged.connect(self.qrencode)
        self.emailSubjectEdit.textChanged.connect(self.qrencode)
        self.emailBodyEdit.textChanged.connect(self.qrencode)
        self.phonebookNameEdit.textChanged.connect(self.qrencode)
        self.phonebookTelEdit.textChanged.connect(self.qrencode)
        self.phonebookEMailEdit.textChanged.connect(self.qrencode)
        self.phonebookNoteEdit.textChanged.connect(self.qrencode)
        self.phonebookAddressEdit.textChanged.connect(self.qrencode)
        self.phonebookBirthdayEdit.dateChanged.connect(self.qrencode)
        self.phonebookUrlEdit.textChanged.connect(self.qrencode)
        self.smsNumberEdit.textChanged.connect(self.qrencode)
        self.smsBodyEdit.textChanged.connect(self.qrencode)
        self.smsBodyEdit.textChanged.connect(
            lambda: self.smsCharCount.setText(
                unicode(self.trUtf8("characters count: %s - %d message(s)")) % (
                len(self.smsBodyEdit.toPlainText()),
                ceil(len(self.smsBodyEdit.toPlainText()) / 160.0)
                )                    
                )
            )
        self.mmsNumberEdit.textChanged.connect(self.qrencode)
        self.mmsBodyEdit.textChanged.connect(self.qrencode)
        self.telephoneEdit.textChanged.connect(self.qrencode)
        self.geoLatEdit.textChanged.connect(self.qrencode)
        self.geoLongEdit.textChanged.connect(self.qrencode)
        self.pixelSize.valueChanged.connect(self.qrencode)
        self.ecLevel.currentIndexChanged.connect(self.qrencode)
        self.marginSize.valueChanged.connect(self.qrencode)
        self.saveButton.clicked.connect(self.saveCode)
        self.exitAction.triggered.connect(self.close)
        self.aboutAction.triggered.connect(self.about)
        self.decodeFileAction.triggered.connect(self.decodeFile)
        self.decodeWebcamAction.triggered.connect(self.decodeWebcam)

        self.qrcode.setAcceptDrops(True)
        self.qrcode.__class__.dragEnterEvent = self.dragEnterEvent
        self.qrcode.__class__.dropEvent = self.dropEvent

    def qrencode(self):
        #Functions to get the correct data
        data_fields = {
            "text": unicode(self.textEdit.toPlainText()),
            "url": unicode(self.urlEdit.text()),
            "bookmark": ( unicode(self.bookmarkTitleEdit.text()), unicode(self.bookmarkUrlEdit.text()) ),
            "email": unicode(self.emailEdit.text()),
            "emailmessage": ( unicode(self.emailEdit.text()), unicode(self.emailSubjectEdit.text()), unicode(self.emailBodyEdit.toPlainText()) ),
            "telephone": unicode(self.telephoneEdit.text()),
            "phonebook": (('N',unicode(self.phonebookNameEdit.text())),
                          ('TEL', unicode(self.phonebookTelEdit.text())),
                          ('EMAIL',unicode(self.phonebookEMailEdit.text())),
                          ('NOTE', unicode(self.phonebookNoteEdit.text())),
                          ('BDAY', unicode(self.phonebookBirthdayEdit.date().toString("yyyyMMdd"))), #YYYYMMDD
                          ('ADR', unicode(self.phonebookAddressEdit.text())),  #The fields divided by commas (,) denote PO box, room number, house number, city, prefecture, zip code and country, in order.
                          ('URL', unicode(self.phonebookUrlEdit.text())),
                          # ('NICKNAME', ''),
                        ),
            "sms": ( unicode(self.smsNumberEdit.text()), unicode(self.smsBodyEdit.toPlainText()) ),
            "mms": ( unicode(self.mmsNumberEdit.text()), unicode(self.mmsBodyEdit.toPlainText()) ),
            "geo": ( unicode(self.geoLatEdit.text()), unicode(self.geoLongEdit.text()) ),
        }

        data_type = unicode(self.templates[unicode(self.selector.currentText())])
        data = data_fields[data_type]
        
        level = (u'L',u'M',u'Q',u'H')

        if data:
            if data_type == 'emailmessage' and data[1] == '' and data[2] == '':
                data_type = 'email'
                data = data_fields[data_type]
            qr = QR(pixel_size = unicode(self.pixelSize.value()),
                    data = data,
                    level = unicode(level[self.ecLevel.currentIndex()]),
                    margin_size = unicode(self.marginSize.value()),
                    data_type = data_type,
                    )
            if qr.encode() == 0:
                self.qrcode.setPixmap(QtGui.QPixmap(qr.filename))
                self.saveButton.setEnabled(True)
            else:
                if NOTIFY:
                    n = pynotify.Notification(
                        "QtQR",
                        unicode(self.trUtf8("ERROR: Something went wrong while trying to generate the QR Code.")),
                        "qtqr"
                        )
                    n.show()
                else:
                    print "Something went worng while trying to generate the QR Code"
        else:
            self.saveButton.setEnabled(False)

    def saveCode(self):
        fn = QtGui.QFileDialog.getSaveFileName(
            self,
            self.trUtf8('Save QRCode'), 
            filter=self.trUtf8('PNG Images (*.png);; All Files (*.*)')
            )
        if fn:
            if not fn.toLower().endsWith(u".png"):
                fn += u".png"
            self.qrcode.pixmap().save(fn)
            if NOTIFY:
                n = pynotify.Notification(
                    unicode(self.trUtf8("Save QR Code")),
                    unicode(self.trUtf8("QR Code succesfully saved to %s")) % fn,
                    "qtqr"
                    )
                n.show()
            else:
               QtGui.QMessageBox.information(
                    self, 
                    unicode(self.trUtf8('Save QRCode')),
                    unicode(self.trUtf8('QRCode succesfully saved to <b>%s</b>.')) % fn
                    )

    def decodeFile(self, fn=None):
        if not fn:
            fn = unicode(QtGui.QFileDialog.getOpenFileName(
                self,
                self.trUtf8('Open QRCode'),
                filter=self.trUtf8('Images (*.png *.jpg);; All Files (*.*)')
                )
            )
        if os.path.isfile(fn):
            qr = QR(filename=fn)
            if qr.decode():
                self.showInfo(qr)
            else:
                QtGui.QMessageBox.information(
                    self,
                    self.trUtf8('Decode File'),
                    unicode(self.trUtf8('No QRCode could be found in file: <b>%s</b>.')) % fn
                )
#        else:
#            QtGui.QMessageBox.information(
#                self,
#                u"Decode from file",
#                u"The file <b>%s</b> doesn't exist." %
#                os.path.abspath(fn),
#                QtGui.QMessageBox.Ok
#            )

    def showInfo(self, qr):
        dt = qr.data_type
        print dt.encode(u"utf-8") + ':',
        data = qr.data_decode[dt](qr.data)
        if type(data) == tuple:
            for d in data:
                print d.encode(u"utf-8")
        elif type(data) == dict:
                # FIX-ME: Print the decoded symbols
                print "Dict"
                print data.keys()
                print data.values()
        else:
            print data.encode(u"utf-8")
        msg = {
            'text': lambda : unicode(self.trUtf8("QRCode contains the following text:\n\n%s")) % (data),
            'url': lambda : unicode(self.trUtf8("QRCode contains the following url address:\n\n%s")) % (data),
            'bookmark': lambda: unicode(self.trUtf8("QRCode contains a bookmark:\n\nTitle: %s\nURL: %s")) % (data),
            'email': lambda : unicode(self.trUtf8("QRCode contains the following e-mail address:\n\n%s")) % (data),
            'emailmessage': lambda : unicode(self.trUtf8("QRCode contains an e-mail message:\n\nTo: %s\nSubject: %s\nMessage: %s")) % (data),
            'telephone': lambda : unicode(self.trUtf8("QRCode contains a telephone number: ")) + (data),
            'phonebook': lambda : unicode(self.trUtf8("QRCode contains a phonebook entry:\n\nName: %s\nTel: %s\nE-Mail: %s\nNote: %s\nBirthday: %s\nAddress: %s\nURL: %s")) %
                (data.get('N') or "", 
                 data.get('TEL') or "", 
                 data.get('EMAIL') or "", 
                 data.get('NOTE') or "",
                 QtCore.QDate.fromString(data.get('BDAY') or "",'yyyyMMdd').toString(), 
                 data.get('ADR') or "",
                 data.get('URL') or ""),
            'sms': lambda : unicode(self.trUtf8("QRCode contains the following SMS message:\n\nTo: %s\nMessage: %s")) % (data),
            'mms': lambda : unicode(self.trUtf8("QRCode contains the following MMS message:\n\nTo: %s\nMessage: %s")) % (data),
            'geo': lambda : unicode(self.trUtf8("QRCode contains the following coordinates:\n\nLatitude: %s\nLongitude:%s")) % (data),
        }
        wanna = self.trUtf8("\n\nDo you want to ")
        action = {
            'text': u"",
            'url': wanna + self.trUtf8("open it in a browser?"),
            'bookmark': wanna + self.trUtf8("open it in a browser?"),
            'email': wanna + self.trUtf8("send an e-mail to the address?"),
            'emailmessage': wanna + self.trUtf8("send the e-mail?"),
            'telephone': u"",
            'phonebook': u"",
            'sms': u"",
            'mms': u"",
            'geo': wanna + self.trUtf8("open it in Google Maps?"),
        }
        if action[qr.data_type] != u"":
            msgBox = QtGui.QMessageBox(
                QtGui.QMessageBox.Question,
                self.trUtf8('Decode QRCode'),
                msg[qr.data_type]() + action[qr.data_type],
                QtGui.QMessageBox.No |
                QtGui.QMessageBox.Yes,
                self
                )
            msgBox.addButton(self.trUtf8("&Edit"), QtGui.QMessageBox.ApplyRole)
            msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
            rsp = msgBox.exec_()
        else:
            msgBox = QtGui.QMessageBox(
                QtGui.QMessageBox.Information,
                self.trUtf8("Decode QRCode"),
                msg[qr.data_type]() + action[qr.data_type],
                QtGui.QMessageBox.Ok,
                self
                )
            msgBox.addButton(self.trUtf8("&Edit"), QtGui.QMessageBox.ApplyRole)
            msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
            rsp = msgBox.exec_()

        if rsp == QtGui.QMessageBox.Yes:
            #Open Link
            if qr.data_type == 'email':
                link = 'mailto:'+ data
            elif qr.data_type == 'emailmessage':
                link = 'mailto:%s?subject=%s&body=%s' % (data)
            elif qr.data_type == 'geo':
                link = 'http://maps.google.com/maps?q=%s,%s' % data
            elif qr.data_type == 'bookmark':
                link = data[1]
            else:
                link = qr.data_decode[qr.data_type](qr.data)
            print u"Opening " + link
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(link))
        elif rsp == 0:
            #Edit the code
            data = qr.data_decode[qr.data_type](qr.data)
            try:
                tabIndex = self.templateNames.index(self.templates[qr.data_type])
            except KeyError:
                if qr.data_type == 'email':
                    #We have to use the same tab index as EMail Message
                    tabIndex = self.templateNames.index(self.templates["emailmessage"])
            if qr.data_type == 'text':
                self.tabs.setCurrentIndex(tabIndex)
                self.textEdit.setPlainText(data)
            elif qr.data_type == 'url':
                self.tabs.setCurrentIndex(tabIndex)
                self.urlEdit.setText(data)
            elif qr.data_type == 'bookmark':
                self.bookmarkTitleEdit.setText(data[0])
                self.bookmarkUrlEdit.setText(data[1])
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'emailmessage':
                self.emailEdit.setText(data[0])
                self.emailSubjectEdit.setText(data[1])
                self.emailBodyEdit.setPlainText(data[2])
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'email':
                self.emailEdit.setText(data)
                self.emailSubjectEdit.setText("")
                self.emailBodyEdit.setPlainText("")
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'telephone':
                self.telephoneEdit.setText(data)
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'phonebook':
                self.phonebookNameEdit.setText(data.get("N") or "")
                self.phonebookTelEdit.setText(data.get("TEL") or "")
                self.phonebookEMailEdit.setText(data.get("EMAIL") or "")
                self.phonebookNoteEdit.setText(data.get("NOTE") or "")
                self.phonebookBirthdayEdit.setDate(QtCore.QDate.fromString(data.get("BDAY") or "", "yyyyMMdd"))
                self.phonebookAddressEdit.setText(data.get("ADR") or "")
                self.phonebookUrlEdit.setText(data.get("URL") or "")
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'sms':
                self.smsNumberEdit.setText(data[0])
                self.smsBodyEdit.setPlainText(data[1])
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'mms':
                self.mmsNumberEdit.setText(data[0])
                self.mmsBodyEdit.setPlainText(data[1])
                self.tabs.setCurrentIndex(tabIndex)
            elif qr.data_type == 'geo':
                self.geoLatEdit.setText(data[0])
                self.geoLongEdit.setText(data[1])
                self.tabs.setCurrentIndex(tabIndex)

    def decodeWebcam(self):
        vdDialog = VideoDevices()
        if vdDialog.exec_():
            device = vdDialog.videoDevices[vdDialog.videoDevice.currentIndex()][1]
            qr = QR()
            qr.decode_webcam(device=device)
            if qr.data_decode[qr.data_type](qr.data) == 'NULL':
                QtGui.QMessageBox.warning(
                    self,
                    self.trUtf8("Decoding Failed"),
                    self.trUtf8("<p>Oops! no code was found.<br /> Maybe your webcam didn't focus.</p>"),
                    QtGui.QMessageBox.Ok
                )
            else:
                self.showInfo(qr)

    def about(self):
        QtGui.QMessageBox.about(
            self,
            self.trUtf8("About QtQR"),
            unicode(self.trUtf8('<h1>QtQR %s</h1><p>A simple software for creating and decoding QR Codes that uses <a href="https://code.launchpad.net/~qr-tools-developers/qr-tools/python-qrtools-trunk">python-qrtools</a> as backend. Both are part of the <a href="https://launchpad.net/qr-tools">QR Tools</a> project.</p><p></p><p>This is Free Software: GNU-GPLv3</p><p></p><p>Please visit our website for more information and to check out the code:<br /><a href="https://launchpad.net/~qr-tools-developers/qtqr">https://launchpad.net/~qr-tools-developers/qtqr</p><p>copyright &copy; Ramiro Algozino &lt;<a href="mailto:algozino@gmail.com">algozino@gmail.com</a>&gt;</p>')) % __version__,
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for fn in event.mimeData().urls():
            fn = fn.toLocalFile()
            self.decodeFile(unicode(fn))


class VideoDevices(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.videoDevices = []
        for vd in self.getVideoDevices():
            self.videoDevices.append(vd)

        self.setWindowTitle(self.tr('Decode from Webcam'))
        self.cameraIcon = QtGui.QIcon.fromTheme("camera")
        self.icon = QtGui.QLabel()
        self.icon.setPixmap(self.cameraIcon.pixmap(64,64).scaled(64,64))
        self.videoDevice = QtGui.QComboBox()
        self.videoDevice.addItems([vd[0] for vd in self.videoDevices])
        self.label = QtGui.QLabel(self.tr("You are about to decode from your webcam. Please put the code in front of your camera with a good light source and keep it steady.\nOnce you see a green rectangle you can close the window by pressing any key.\n\nPlease select the video device you want to use for decoding:"))
        self.label.setWordWrap(True)
        self.Buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.Buttons.accepted.connect(self.accept)
        self.Buttons.rejected.connect(self.reject)
        self.layout = QtGui.QVBoxLayout()
        self.hlayout = QtGui.QHBoxLayout()
        self.vlayout = QtGui.QVBoxLayout()
        self.hlayout.addWidget(self.icon, 0, QtCore.Qt.AlignTop)
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.videoDevice)
        self.hlayout.addLayout(self.vlayout)
        self.layout.addLayout(self.hlayout)
        self.layout.addStretch()
        self.layout.addWidget(self.Buttons)
        
        self.setLayout(self.layout)
        

    def getVideoDevices(self):
        for dev in os.listdir("/dev/v4l/by-id"):
            try:
                yield([
                    " ".join(dev.split("-")[1].split("_")), 
                    os.path.join("/dev/v4l/by-id", dev)
                ])
            except:
                yield([
                    dev, 
                    os.path.join("/dev/v4l/by-id", dev)
                ])


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # This is to make Qt use locale configuration; i.e. Standard Buttons
    # in your system's language. 
    locale = unicode(QtCore.QLocale.system().name())
    translator=QtCore.QTranslator()
    # translator.load(os.path.join(os.path.abspath(
        # os.path.dirname(__file__)),
        # "qtqr_" + locale))
    # We load from standard location the translations
    translator.load("qtqr_" + locale,
                    QtCore.QLibraryInfo.location(
                    QtCore.QLibraryInfo.TranslationsPath)
                    )
    app.installTranslator(translator)    
    qtTranslator=QtCore.QTranslator()
    qtTranslator.load("qt_" + locale,
                    QtCore.QLibraryInfo.location(
                    QtCore.QLibraryInfo.TranslationsPath)
                    )
    app.installTranslator(qtTranslator);   
    
    mw = MainWindow()
    mw.show()
    if len(app.argv())>1:
        #Open the file and try to decode it
        for fn in app.argv()[1:]:
            # We should check if the file exists.
            mw.decodeFile(fn)
    sys.exit(app.exec_())
