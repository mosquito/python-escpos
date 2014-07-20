ESCPOS
======

Python library to manipulate ESC/POS Printers.

1. Dependencies
---------------

In order to start getting access to your printer, you must ensure
you have previously installed the following python modules:

  * pyusb (python-usb)
  * Pillow

2. Description
--------------

Python ESC/POS is a library which lets the user have access to all
those printers handled by ESC/POS commands, as defined by Epson,
from a Python application.

The standard usage is send raw text to the printer, but in also
helps the user to enhance the experience with those printers by
facilitating the bar code printing in many different standards,
as well as manipulating images so they can be printed as brand
logo or any other usage images migh have.

Text can be aligned/justified and fonts can be changed by size,
type and weight.

Also, this module handles some hardware functionalities like, cut
paper, carrier return, printer reset and others concerned to the
carriage alignment.

3. Define your printer
----------------------

Before start create your Python ESC/POS printer instance, you must
see at your system for the printer parameters. This is done with
the 'lsusb' command.

First run the command to look for the "Vendor ID" and "Product ID",
then write down the values, these values are displayed just before
the name of the device with the following format:

    xxxx:xxxx

Example:

    Bus 002 Device 001: ID 1a2b:1a2b Device name

Write down the the values in question, then issue the following
command so you can get the "Interface" number and "End Point"

    lsusb -vvv -d xxxx:xxxx | grep iInterface
    lsusb -vvv -d xxxx:xxxx | grep bEndpointAddress | grep OUT

The first command will yields the "Interface" number that must
be handy to have and the second yields the "Output Endpoint"
address.

By default the "Interface" number is "0" and the "Output Endpoint"
address is "0x82",  if you have other values then you can define
with your instance.


4. Define your instance
-----------------------

The following example shows how to initialize the Epson TM-TI88IV

**NOTE**: Always finish the sequence with Epson.cut() otherwise you will endup with weird chars being printed.


.. code:: python

    from escpos import *

    """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
    Epson = escpos.Escpos(0x04b8,0x0202,0)
    Epson.text("Hello World")
    Epson.image("logo.gif")
    Epson.barcode
    Epson.barcode('1324354657687','EAN13',64,2,'','')
    Epson.cut()


or use with statement:

.. code:: python

    with EscposIO(printer.Network('192.168.1.87', port=9100)) as p:
        p.set(font='a', codepage='cp1251', size='normal', align='center', bold=True)
        p.printer.set(align='center')
        p.printer.image('logo.gif')
        p.writelines('Big line\n', font='b')
        p.writelines(u'Привет', color=2)
        p.writelines(u'BIG TEXT', size='2x')

    # After exit of with, printer will cut the paper

5. API
------

* Escpos() - main class
* Escpos.image(path_img) - Open image file
* Escpos.qr(text, \*args, \*\*kwargs) - Print QR Code for the provided string
* Escpos.barcode(code, bc, width, height, pos, font) - Print Barcode
* Escpos.text(text) - Print any text
* Escpos.set(codepage=None, \*\*kwargs) - kwargs should be:  
    * bold:        set bold font
    * underline:   underline text
    * size:        Text size
    * font:        Font type
    * align:       Text position
    * inverted:    White on black text
    * color:       Text color
    
* Escpos.cut() - Cut the paper
* Escpos.cashdraw(pin) - Send open cashdraw signal to printer pin.
* Escpos.control() and Escpos.hw() - Should be use it when you want to do another operations.

* EscposIO(printer, autocut=True, autoclose=True) - class for using with 'with' statement. When autocut=False printer not cut the paper after exit of "with".
* EscposIO.set(\*\*kwargs) - set the params in printing stream
    * bold:        set bold font
    * underline:   underline text
    * size:        Text size
    * font:        Font type
    * align:       Text position
    * inverted:    White on black text
    * color:       Text color
* EscposIO.writelines(text, \*\*params) - Accept params like "set", and apply them for this lines. You should use set() for setting common params.



6. Links
--------

Please visit project homepage at:
http://repo.bashlinux.com/projects/escpos.html

* Manuel F Martinez <manpaz@bashlinux.com>
* Dmitry Orlov <me@mosquito.su>
