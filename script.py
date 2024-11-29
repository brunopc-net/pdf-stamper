# QR code
from qr_builder import QrBuilder

# PDF tools
from pdf_editor import PdfEditor

# Logging
import logging
from log_config import LogConfig
LogConfig().setup_logging()

# Performance metrics
import os
import time
import psutil

def with_metrics(func):
    def metrics():
        process = psutil.Process(os.getpid())
        start_time = time.time()

        func()

        elapsed_time = time.time() - start_time
        mem_usage = process.memory_info().rss
        logging.info(f"Executed in {elapsed_time:.3f}s")
        logging.info(f"Memory usage: {mem_usage/ (1024 * 1024):.2f}mb")
    return metrics

def main():
    qr_data = f"""BEGIN:VCARD
    VERSION:3.0
    FN:John Doe
    TEL:+1234567890
    EMAIL:johndoe@example.com
    ADR:123 Business St, Suite 400, City, Country
    END:VCARD"""
    qr_image = QrBuilder(qr_data).export()
    pdf_editor = PdfEditor()
    qr_size = 10
    qr_pdf = pdf_editor.build_img_pdf(qr_image, x=5, y=5, w=qr_size, h=qr_size)
    pdf_editor.add_watermark(qr_pdf, 'input/original.pdf')

execute = with_metrics(main)
execute()