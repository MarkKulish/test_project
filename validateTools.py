from pdfTools import PDFReader


class ValidateDocument(PDFReader):

    def validate_document(self, path_to_doc):

        """Since the template document and the examined document are checked in the same way, you can be sure that if
        the keys do not match, in the examined document, they were placed incorrectly.
        Likewise, if they do not match by name, the examined document had the wrong name."""
        benchmark_document_data = self.get_pdf_data("./Docs/test_task.pdf")
        auditable_document_data = self.get_pdf_data(path_to_doc)

        benchmark_list = list(benchmark_document_data.keys())
        auditable_list = list(auditable_document_data.keys())

        try:
            for i in range(len(auditable_list)):
                if benchmark_list[i] != auditable_list[i]:
                    raise Exception('incorrect document order')

            auditable_list_values = list(auditable_document_data.values())

            if 'value not found!' in auditable_list_values:
                raise Exception("incomplete data")

        except IndexError:
            raise Exception('incorrect amount of data')
