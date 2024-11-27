import qrcode
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import logging
import uuid

# Performance metrics
import os
import time
import psutil

# Generation an execution id for debugging and log retrieving
# Collision are not a big deal since we can also differentiate by timestamp
exec_id = str(uuid.uuid4()).split('-')[0];
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.execid = exec_id
    return record

logging.basicConfig(
    level=logging.NOTSET,
    format='%(asctime)s.%(msecs)03d %(execid)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logging.setLogRecordFactory(record_factory)

qr_size = 10
buyer_info = {
  "full_name": "John Doe",
  "phone": "+1234567890",
  "email": "johndoe@example.com",
  "company": "Company XYZ",
  "address": "123 Business St, Suite 400, City, Country"
}

def build_vcard(buyer_info):
    """
    Generate a vCard format string from buyer information.
    """
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{buyer_info['full_name']}
TEL:{buyer_info['phone']}
EMAIL:{buyer_info['email']}
ADR:{buyer_info['address']}
END:VCARD"""
    return vcard

# Function to generate QR code image
def build_qr_code(data):
    logging.info(f"Building QR code from data")
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr_image_path = "/qr_code.png"  # Temporary path for saving QR code image
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_image_path)
    logging.info(f"Done")
    return qr_image_path

# Function to create a PDF with the QR code image as a watermark
def build_qr_pdf(qr_image_path):
    logging.info(f"Building QR pdf")
    # Create a temporary PDF to store the QR code image
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Add the image to the canvas
    c.drawImage(qr_image_path, 5, 5, width=qr_size, height=qr_size)  # Adjust the position as needed
    c.save()

    # Create PDF with QR code
    packet.seek(0)
    new_pdf = PdfReader(packet)
    logging.info(f"Done")
    return new_pdf.pages[0]

def create_signed_pdf(input_path, output_path, qr_pdf):
    logging.info(f"Signing pdf {input_path}")
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(qr_pdf)  # Merge the QR code PDF onto the page
        writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)
        logging.info(f"Signed as {output_path}")

process = psutil.Process(os.getpid())
start_time = time.time()

qr_data = build_vcard(buyer_info)
qr_image = build_qr_code(qr_data)
qr_pdf = build_qr_pdf(qr_image)
create_signed_pdf('input/original.pdf', 'output/signed.pdf', qr_pdf)

elapsed_time = time.time() - start_time
mem_usage = process.memory_info().rss
logging.info(f"Executed in {elapsed_time:.4f}s")
logging.info(f"Memory usage: {mem_usage/ (1024 * 1024):.2f}mb")