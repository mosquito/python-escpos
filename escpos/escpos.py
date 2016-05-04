#!/usr/bin/python
'''
@author: Manuel F Martinez <manpaz@bashlinux.com>
@organization: Bashlinux
@copyright: Copyright (c) 2012 Bashlinux
@license: GPL
'''

try:
    import Image
except ImportError:
    from PIL import Image

import qrcode
import time

from constants import *
from exceptions import *

class EscposIO(object):
    ''' ESC/POS Printer IO object'''
    def __init__(self, printer, autocut=True, autoclose=True):
        self.printer = printer
        self.params = {}
        self.autocut = autocut
        self.autoclose = autoclose


    def set(self, **kwargs):
        """
        :type bold:         bool
        :param bold:        set bold font
        :type underline:    [None, 1, 2]
        :param underline:   underline text
        :type size:         ['normal', '2w', '2h' or '2x']
        :param size:        Text size
        :type font:         ['a', 'b', 'c']
        :param font:        Font type
        :type align:        ['left', 'center', 'right']
        :param align:       Text position
        :type inverted:     boolean
        :param inverted:    White on black text
        :type color:        [1, 2]
        :param color:       Text color
        :rtype:             NoneType
        :returns:            None
        """

        self.params.update(kwargs)


    def writelines(self, text, **kwargs):
        params = dict(self.params)
        params.update(kwargs)

        if isinstance(text, unicode) or isinstance(text, str):
            lines = text.split('\n')
        elif isinstance(text, list) or isinstance(text, tuple):
            lines = text
        else:
            lines = ["{0}".format(text),]

        for line in lines:
            self.printer.set(**params)
            if isinstance(text, unicode):
                self.printer.text(u"{0}\n".format(line))
            else:
                self.printer.text("{0}\n".format(line))


    def close(self):
        self.printer.close()


    def __enter__(self, **kwargs):
        return self


    def __exit__(self, type, value, traceback):
        if not (type is not None and issubclass(type, Exception)):
            if self.autocut:
                self.printer.cut()

        if self.autoclose:
            self.close()



class Escpos(object):
    """ ESC/POS Printer object """
    device    = None
    _codepage  = None
    stored_args = {}


    def _check_image_size(self, size):
        """ Check and fix the size of the image to 32 bits """
        if size % 32 == 0:
            return (0, 0)
        else:
            image_border = 32 - (size % 32)
            if (image_border % 2) == 0:
                return (image_border / 2, image_border / 2)
            else:
                return (image_border / 2, (image_border / 2) + 1)


    def _print_image(self, line, size):
        """ Print formatted image """
        i = 0
        cont = 0
        buffer = ""

        self._raw(S_RASTER_N)
        buffer = "%02X%02X%02X%02X" % (((size[0]/size[1])/8), 0, size[1], 0)
        self._raw(buffer.decode('hex'))
        buffer = ""

        while i < len(line):
            hex_string = int(line[i:i+8],2)
            buffer += "%02X" % hex_string
            i += 8
            cont += 1
            if cont % 4 == 0:
                self._raw(buffer.decode("hex"))
                buffer = ""
                cont = 0


    def _convert_image(self, im):
        """ Parse image and prepare it to a printable format """
        pixels   = []
        pix_line = ""
        im_left  = ""
        im_right = ""
        switch   = 0
        img_size = [ 0, 0 ]


        if im.size[0] > 512:
            print  ("WARNING: Image is wider than 512 and could be truncated at print time ")
        if im.size[1] > 255:
            raise ImageSizeError()

        im_border = self._check_image_size(im.size[0])
        for i in range(im_border[0]):
            im_left += "0"
        for i in range(im_border[1]):
            im_right += "0"

        for y in range(im.size[1]):
            img_size[1] += 1
            pix_line += im_left
            img_size[0] += im_border[0]
            for x in range(im.size[0]):
                img_size[0] += 1
                RGB = im.getpixel((x, y))
                im_color = (RGB[0] + RGB[1] + RGB[2])
                im_pattern = "1X0"
                pattern_len = len(im_pattern)
                switch = (switch - 1 ) * (-1)
                for x in range(pattern_len):
                    if im_color <= (255 * 3 / pattern_len * (x+1)):
                        if im_pattern[x] == "X":
                            pix_line += "%d" % switch
                        else:
                            pix_line += im_pattern[x]
                        break
                    elif im_color > (255 * 3 / pattern_len * pattern_len) and im_color <= (255 * 3):
                        pix_line += im_pattern[-1]
                        break
            pix_line += im_right
            img_size[0] += im_border[1]

        self._print_image(pix_line, img_size)


    def image(self,path_img):
        """ Open image file """
        im_open = Image.open(path_img)
        im = im_open.convert("RGB")
        # Convert the RGB image in printable image
        self._convert_image(im)


    def qr(self, text, *args, **kwargs):
        """ Print QR Code for the provided string """
        qr_args = dict(
            version=4,
            box_size=4,
            border=1,
            error_correction=qrcode.ERROR_CORRECT_M
        )

        qr_args.update(kwargs)
        qr_code = qrcode.QRCode(**qr_args)

        qr_code.add_data(text)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        im = qr_img._img.convert("RGB")
        # Convert the RGB image in printable image
        self._convert_image(im)


    def barcode(self, code, bc, width, height, pos, font):
        """ Print Barcode """
        # Align Bar Code()
        self._raw(TXT_ALIGN_CT)
        # Height
        if height >=2 or height <=6:
            self._raw(BARCODE_HEIGHT)
        else:
            raise BarcodeSizeError()
        # Width
        if width >= 1 or width <=255:
            self._raw(BARCODE_WIDTH)
        else:
            raise BarcodeSizeError()
        # Font
        if font.upper() == "B":
            self._raw(BARCODE_FONT_B)
        else: # DEFAULT FONT: A
            self._raw(BARCODE_FONT_A)
        # Position
        if pos.upper() == "OFF":
            self._raw(BARCODE_TXT_OFF)
        elif pos.upper() == "BOTH":
            self._raw(BARCODE_TXT_BTH)
        elif pos.upper() == "ABOVE":
            self._raw(BARCODE_TXT_ABV)
        else:  # DEFAULT POSITION: BELOW
            self._raw(BARCODE_TXT_BLW)
        # Type
        if bc.upper() == "UPC-A":
            self._raw(BARCODE_UPC_A)
        elif bc.upper() == "UPC-E":
            self._raw(BARCODE_UPC_E)
        elif bc.upper() == "EAN13":
            self._raw(BARCODE_EAN13)
        elif bc.upper() == "EAN8":
            self._raw(BARCODE_EAN8)
        elif bc.upper() == "CODE39":
            self._raw(BARCODE_CODE39)
        elif bc.upper() == "ITF":
            self._raw(BARCODE_ITF)
        elif bc.upper() == "NW7":
            self._raw(BARCODE_NW7)
        else:
            raise BarcodeTypeError()
        # Print Code
        if code:
            self._raw(code)
        else:
            raise exception.BarcodeCodeError()


    def text(self, text):
        """ Print alpha-numeric text """
        if text:
            if self._codepage:
                self._raw(unicode(text).encode(self._codepage))
            else:
                self._raw(text)
        else:
            raise TextError()


    def set(self, codepage=None, **kwargs):
        """
        :type bold:         bool
        :param bold:        set bold font
        :type underline:    [None, 1, 2]
        :param underline:   underline text
        :type size:         ['normal', '2w', '2h' or '2x']
        :param size:        Text size
        :type font:         ['a', 'b', 'c']
        :param font:        Font type
        :type align:        ['left', 'center', 'right']
        :param align:       Text position
        :type inverted:     boolean
        :param inverted:    White on black text
        :type color:        [1, 2]
        :param color:       Text color
        :rtype:             NoneType
        :returns:            None
        """

        for key in kwargs.iterkeys():
            if not TEXT_STYLE.has_key(key):
                raise KeyError('Parameter {0} is wrong.'.format(key))

        for key, value in TEXT_STYLE.iteritems():
            if kwargs.has_key(key):
                cur = kwargs[key]
                if isinstance(cur, str) or isinstance(cur, unicode):
                    cur = cur.lower()

                if value.has_key(cur):
                    self._raw(value[cur])
                else:
                    raise AttributeError(
                        'Attribute {0} is wrong.'.format(cur)
                    )

        # Codepage
        if codepage:
            self._codepage = codepage
            self._raw(PAGE_CP_SET_COMMAND + chr(PAGE_CP_CODE[codepage]))

    def cut(self, mode='', postfix="\n\n\n\n\n"):
        """ Cut paper """
        # Fix the size between last line and cut
        # TODO: handle this with a line feed
        self._raw(postfix)
        if mode.upper() == "PART":
            self._raw(PAPER_PART_CUT)
        else: # DEFAULT MODE: FULL CUT
            self._raw(PAPER_FULL_CUT)


    def cashdraw(self, pin):
        """ Send pulse to kick the cash drawer """
        if pin == 2:
            self._raw(CD_KICK_2)
        elif pin == 5:
            self._raw(CD_KICK_5)
        else:
            raise CashDrawerError()


    def hw(self, hw):
        """ Hardware operations """
        if hw.upper() == "INIT":
            self._raw(HW_INIT)
        elif hw.upper() == "SELECT":
            self._raw(HW_SELECT)
        elif hw.upper() == "RESET":
            self._raw(HW_RESET)
        else: # DEFAULT: DOES NOTHING
            pass

        self._codepage = None


    def control(self, ctl):
        """ Feed control sequences """
        if ctl.upper() == "LF":
            self._raw(CTL_LF)
        elif ctl.upper() == "FF":
            self._raw(CTL_FF)
        elif ctl.upper() == "CR":
            self._raw(CTL_CR)
        elif ctl.upper() == "HT":
            self._raw(CTL_HT)
        elif ctl.upper() == "VT":
            self._raw(CTL_VT)

    def close(self):
        self._raw(RESET)
        self.__del__()
