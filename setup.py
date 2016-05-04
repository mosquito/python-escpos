#!/usr/bin/python

from distutils.core import setup

setup(
    name='python-escpos',
    version='1.1.0',
    url='https://github.com/mosquito/python-escpos',
    download_url='https://github.com/mosquito/python-escpos/archive/master.zip',
    description='Python library to manipulate ESC/POS Printers',
    long_description=open('README.rst').read(),
    license='LGPL',
    author=['Manuel F Martinez', 'Dmitry Orlov'],
    author_email=['manpaz@bashlinux.com', 'me@mosquito.su'],
    platforms=['linux'],
    packages=[
        'escpos',
    ],
    install_requires=[
        'pyusb',
        'Pillow>=2.0',
        'qrcode>=4.0',
        'pyserial',
    ],
)
