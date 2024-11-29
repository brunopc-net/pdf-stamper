import logging
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PdfEditor:

    def __init__(self):
        pass

    # Build pdf from an image 
    def build_img_pdf(self, img_path, x, y, w, h):
        logging.info(f"Building pdf from image {img_path}")
        # Create a temporary PDF to store the QR code image
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)

        # Add the image to the canvas
        c.drawImage(img_path, x, y, width=w, height=h)
        c.save()

        # Create PDF
        packet.seek(0)
        new_pdf = PdfReader(packet)
        logging.info(f"Building pdf: done")
        return new_pdf.pages[0]

    # Add image watermark to a pdf
    # to_pdf_path: output pdf path
    # watermark_pdf: the pdf watermark to add
    # pages: array of the pages to add the watermark to, or "all" for all pages
    def add_watermark(self, watermark_pdf_path: str, input_pdf_path:str, output_pdf_path="output/watermarked.pdf", pages="all"):
        logging.info(f"Addding watermark to pdf {input_pdf_path}")
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        
        if pages == "all":
            pages = range(len(reader.pages))

        for page_num in pages:
            page = reader.pages[page_num]
            page.merge_page(watermark_pdf_path)  # Merge the QR code PDF onto the page
            writer.add_page(page)

        with open(output_pdf_path, 'wb') as output_pdf:
            writer.write(output_pdf)
        
        logging.info(f"Watermarked, exported to {output_pdf_path}")