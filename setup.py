#!/usr/bin/python

from distutils.core import setup

setup(
    name='python-escpos',
    version='1.0.3',
    url='http://code.google.com/p/python-escpos',
    download_url='https://github.com/mosquito/python-escpos/archive/master.zip',
    description='Python library to manipulate ESC/POS Printers',
    license='GNU GPL v3',
    long_description=open('README').read(),
    author='Manuel F Martinez',
    author_email='manpaz@bashlinux.com',
    platforms=['linux'],
    packages=[
        'escpos',
    ],
    package_data={'': ['COPYING']},
    install_requires=[
        'pyusb',
        'Pillow>=2.0',
        'qrcode>=4.0',
        'pyserial',
    ],
)
