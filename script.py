import qrcode
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Performance metrics
import os
import time
import psutil

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
    return qr_image_path

# Function to create a PDF with the QR code image as a watermark
def build_qr_pdf(qr_image_path):
    # Create a temporary PDF to store the QR code image
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Add the image to the canvas
    c.drawImage(qr_image_path, 5, 5, width=qr_size, height=qr_size)  # Adjust the position as needed
    c.save()

    # Create PDF with QR code
    packet.seek(0)
    new_pdf = PdfReader(packet)
    return new_pdf.pages[0]

def create_signed_pdf(input_path, output_path, qr_pdf):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        page.merge_page(qr_pdf)  # Merge the QR code PDF onto the page
        writer.add_page(page)

    with open(output_path, 'wb') as output_pdf:
        writer.write(output_pdf)
        print(f"Watermarked PDF saved as: {output_path}")

print()
print(f"***************************************** EXECUTION *****************************************")
print(f"*********************************************************************************************")
process = psutil.Process(os.getpid())
start_time = time.time()

qr_data = build_vcard(buyer_info)
qr_image = build_qr_code(qr_data)
qr_pdf = build_qr_pdf(qr_image)
create_signed_pdf('original.pdf', 'output/signed.pdf', qr_pdf)

elapsed_time = time.time() - start_time
mem_usage = process.memory_info().rss
print(f"Execution Time: {elapsed_time:.4f} seconds")
print(f"Memory usage: {mem_usage/ (1024 * 1024):.4f} MB")
print(f"*********************************************************************************************")
print()