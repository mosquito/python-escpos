""" ESC/POS Commands (Constants) """

# Feed control sequences
CTL_LF    = '\x0a'             # Print and line feed
CTL_FF    = '\x0c'             # Form feed
CTL_CR    = '\x0d'             # Carriage return
CTL_HT    = '\x09'             # Horizontal tab
CTL_VT    = '\x0b'             # Vertical tab
# Printer hardware
HW_INIT   = '\x1b\x40'         # Clear data in buffer and reset modes
HW_SELECT = '\x1b\x3d\x01'     # Printer select
HW_RESET  = '\x1b\x3f\x0a\x00' # Reset printer hardware
# Cash Drawer
CD_KICK_2 = '\x1b\x70\x00'     # Sends a pulse to pin 2 []
CD_KICK_5 = '\x1b\x70\x01'     # Sends a pulse to pin 5 []
# Paper
PAPER_FULL_CUT  = '\x1d\x56\x00' # Full cut paper
PAPER_PART_CUT  = '\x1d\x56\x01' # Partial cut paper
# Text format

BARCODE_TXT_OFF = '\x1d\x48\x00' # HRI barcode chars OFF
BARCODE_TXT_ABV = '\x1d\x48\x01' # HRI barcode chars above
BARCODE_TXT_BLW = '\x1d\x48\x02' # HRI barcode chars below
BARCODE_TXT_BTH = '\x1d\x48\x03' # HRI barcode chars both above and below
BARCODE_FONT_A  = '\x1d\x66\x00' # Font type A for HRI barcode chars
BARCODE_FONT_B  = '\x1d\x66\x01' # Font type B for HRI barcode chars
BARCODE_HEIGHT  = '\x1d\x68\x64' # Barcode Height [1-255]
BARCODE_WIDTH   = '\x1d\x77\x03' # Barcode Width  [2-6]
BARCODE_UPC_A   = '\x1d\x6b\x00' # Barcode type UPC-A
BARCODE_UPC_E   = '\x1d\x6b\x01' # Barcode type UPC-E
BARCODE_EAN13   = '\x1d\x6b\x02' # Barcode type EAN13
BARCODE_EAN8    = '\x1d\x6b\x03' # Barcode type EAN8
BARCODE_CODE39  = '\x1d\x6b\x04' # Barcode type CODE39
BARCODE_ITF     = '\x1d\x6b\x05' # Barcode type ITF
BARCODE_NW7     = '\x1d\x6b\x06' # Barcode type NW7

# Image format
S_RASTER_N      = '\x1d\x76\x30\x00' # Set raster image normal size
S_RASTER_2W     = '\x1d\x76\x30\x01' # Set raster image double width
S_RASTER_2H     = '\x1d\x76\x30\x02' # Set raster image double height
S_RASTER_Q      = '\x1d\x76\x30\x03' # Set raster image quadruple

RESET           = '\x1b\x40'

TEXT_STYLE = {
    'bold': {
        0: '\x1b\x45\x00',          # Bold font OFF
        1: '\x1b\x45\x01',          # Bold font ON
    },
    'underline': {
        None: '\x1b\x2d\x00',       # Underline font OFF
        1: '\x1b\x2d\x01',          # Underline font 1-dot ON
        2: '\x1b\x2d\x02',          # Underline font 2-dot ON
    },
    'size': {
        'normal': '\x1b\x21\x00',   # Normal text
        '2h': '\x1b\x21\x10',       # Double height text
        '2w': '\x1b\x21\x20',       # Double width text
        '2x': '\x1b\x21\x30',       # Quad area text
    },
    'font': {
        'a': '\x1b\x4d\x00',        # Font type A
        'b': '\x1b\x4d\x01',        # Font type B
        'c': '\x1b\x4d\x02',        # Font type C (may not support)
    },
    'align': {
        'left': '\x1b\x61\x00',     # Left justification
        'right': '\x1b\x61\x02',    # Right justification
        'center': '\x1b\x61\x01',   # Centering
    },
    'inverted': {
        False: '\x1d\x42\x00',      # Inverted mode ON
        True: '\x1d\x42\x01',       # Inverted mode OFF
    },
    'color': {
        1: '\x1b\x72\x00',          # Select 1st printing color
        2: '\x1b\x72\x00',          # Select 2nd printing color
    }
}

PAGE_CP_SET_COMMAND = '\x1b\x74'
PAGE_CP_CODE = {
    'cp437'       : 0,
    # 'katakana'  : 1,
    'cp850'       : 2,
    'cp860'       : 3,
    'cp863'       : 4,
    'cp865'       : 5,
    'cp1251'      : 6,
    'cp866'       : 7,
    'mac_cyrillic': 8,
    'cp775'       : 9,
    'cp1253'      : 10,
    'cp737'       : 11,
    'cp857'       : 12,
    'iso8859_9'   : 13,
    'cp864'       : 14,
    'cp862'       : 15,
    'iso8859_2'   : 16,
    'cp1253'      : 17,
    'cp1250'      : 18,
    'cp858'      : 19,
    'cp1254'      : 20,
    # 'TIS_14'    : 21,
    # 'TIS_17'    : 22,
    # 'TIS_11'    : 23,
    'cp737'       : 24,
    'cp1257'      : 25,
    'cp847'       : 26,
    # 'cp720'     : 27,
    'cp885'       : 28,
    'cp857'       : 29,
    'cp1250'      : 30,
    'cp775'       : 31,
    'cp1254'      : 32,
    # ''          : 33,
    'cp1256'      : 34,
    'cp1258'      : 35,
    'iso8859_2'   : 36,
    'iso8859_3'   : 37,
    'iso8859_4'   : 38,
    'iso8859_5'   : 39,
    'iso8859_6'   : 40,
    'iso8859_7'   : 41,
    'iso8859_8'   : 42,
    'iso8859_9'   : 43,
    'iso8859_15'  : 44,
    # '???'       : 45,
    'cp856'       : 46,
    'cp874'       : 47,
}
