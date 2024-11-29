import qrcode
import logging

class QrBuilder:
    # The version parameter is an integer from 1 to 40 that controls the size of the QR Code
    # The smallest, version 1, is a 21x21 matrix
    # Set to None and use the fit parameter when making the code to determine this automatically
    QR_VERSION = None
    # The error_correction parameter controls the error correction used for the QR Code.
    # The following four constants are made available on the qrcode package:
    # ERROR_CORRECT_L: About 7% or less errors can be corrected.
    # ERROR_CORRECT_M (default): About 15% or less errors can be corrected.
    # ERROR_CORRECT_Q: About 25% or less errors can be corrected.
    # ERROR_CORRECT_H: About 30% or less errors can be corrected.
    QR_ERROR_CORRECT = qrcode.constants.ERROR_CORRECT_L
    # The box_size parameter controls how many pixels each “box” of the QR code is.
    QR_BOX_SIZE = 10
    # The border parameter controls how many boxes thick the border should be (the default is 4, which is the minimum according to the specs).
    QR_BORDER = 4
    #cfill_color and back_color can change the background and the painting color of the QR, when using the default image factory. Both parameters accept RGB color tuples.
    # img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
    QR_FILL_COLOR = "black"
    QR_BACK_COLOR = "white"

    def __init__(self, data):
        self.data = data
        self.qr = qrcode.QRCode(
            version=self.QR_VERSION,
            error_correction=self.QR_ERROR_CORRECT,
            box_size=self.QR_BOX_SIZE,
            border=self.QR_BORDER
        )
        self.qr.add_data(self.data)
        self.qr.make(fit=True)

    def export(self, path='/qr_code.png'):
        logging.info(f"Building QR code image")
        img = self.qr.make_image(fill_color=self.QR_FILL_COLOR, back_color=self.QR_BACK_COLOR)
        img.save(path)
        logging.info(f"QR code exported to {path}")
        return path

    def __str__(self):
        return f"{self.data}"