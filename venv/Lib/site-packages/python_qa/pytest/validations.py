from PyPDF2 import PdfFileReader
from python_qa.logging.logging import Logging


def validate_pdf(
        file_path: str, title: str = None, pages: int = None, text: str = None
):
    # ToDo: check module installed
    Logging.logger.info("Validation PDF:")
    with open(file_path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        if title:
            pdf_title = info.title
            Logging.logger.info(f"\nExpected title: {title}\nActual title: {pdf_title}")
            assert title in pdf_title, f"\nExpected title: {title}\nActual title: {pdf_title}"
        if pages:
            number_of_pages = pdf.getNumPages()
            Logging.logger.info(f"\nExpected number of pages: {pages}\nActual number of pages: {number_of_pages}")
            assert number_of_pages == pages, f"\nExpected number of pages: {pages}\nActual number of pages: {number_of_pages}"
        if text:
            page = pdf.getPage(0)
            pdf_text = page.extractText()
            Logging.logger.info(f"\nExpected text: {text}\nActual title: {pdf_text}")
            assert text in pdf_text, f"\nExpected text: {text}\nActual title: {pdf_text}"
