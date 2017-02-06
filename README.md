qrtools
=============

###1. Introduction

qrtools is a suite of tools for handling [QR codes](http://www.qrcode.com/en/index.html).

###2. Dependencies

This module requires the ZBar Bar Code Reader, which may be obtained from [here](http://zbar.sourceforge.net/).

Than, you might need to install PyPNG, the Python bindings for ZBar and PIL(pillow) modules:
```
[sudo] pip install pypng
[sudo] pip install zbar
[sudo] pip install pillow
```

###3. Install

This package uses distutils, which is the default way of installing python modules. To install in your home directory, securely run the following:
```
git clone https://github.com/primetang/qrtools.git
cd qrtools
[sudo] python setup.py install
```

Or directly through `pip` to install it:
```
[sudo] pip install qrtools
```

###4. Usage

Use it just like the following code:
```
import qrtools
qr = qrtools.QR()
qr.decode("bookmark.png")
print qr.data
```

And here is the `bookmark.png`:
![](https://github.com/primetang/qrtools/blob/master/samples/bookmark.png)
