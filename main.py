from pdfTools import PDFReader
from validateTools import ValidateDocument

pdf_opener = PDFReader()
pdf_validator = ValidateDocument()

pdf_opener.get_pdf_data("./Docs/test_task.pdf")

"""The check fails because there is no value for REMARK."""
pdf_validator.validate_document("./Docs/test_task.pdf")
