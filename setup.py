from setuptools import setup

setup(
    name="qrtools",
    version="0.0.1",
    author="David Green & Gefu Tang",
    author_email="tanggefu@gmail.com",
    description=("qrtools is a suite of tools for handling QR codes."),
    license="GNU",
    keywords="QR code",
    url="https://github.com/primetang/qrtools",
    packages=['qrtools'],
    package_dir={'qrtools': 'src'},
)
