from __future__ import annotations

import os
import shutil
import tempfile

from app.utils.pdf_converter.pdf_reader import (
    extract_pdf_content,
)

from app.utils.pdf_converter.excel_exporter import (
    export_to_excel,
)

from app.utils.pdf_converter.word_exporter import (
    export_to_word,
)


class PdfConverterService:

    def convert_to_excel(
        self,
        pdf_path: str,
    ) -> str:

        if not os.path.exists(pdf_path):

            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        pages = extract_pdf_content(
            pdf_path
        )

        if not pages:

            raise ValueError(
                "The PDF contains no readable pages."
            )

        output_directory = tempfile.mkdtemp(
            prefix="pdf_excel_"
        )

        output_path = os.path.join(
            output_directory,
            "converted.xlsx",
        )

        try:

            export_to_excel(
                pages,
                output_path,
            )

            if not os.path.exists(
                output_path
            ):

                raise RuntimeError(
                    "Excel file was not created."
                )

            return output_path

        except Exception:

            shutil.rmtree(
                output_directory,
                ignore_errors=True,
            )

            raise

    def convert_to_word(
        self,
        pdf_path: str,
    ) -> str:

        if not os.path.exists(pdf_path):

            raise FileNotFoundError(
                f"PDF file not found: {pdf_path}"
            )

        pages = extract_pdf_content(
            pdf_path
        )

        if not pages:

            raise ValueError(
                "The PDF contains no readable pages."
            )

        output_directory = tempfile.mkdtemp(
            prefix="pdf_word_"
        )

        output_path = os.path.join(
            output_directory,
            "converted.docx",
        )

        try:

            export_to_word(
                pages,
                output_path,
            )

            if not os.path.exists(
                output_path
            ):

                raise RuntimeError(
                    "Word file was not created."
                )

            return output_path

        except Exception:

            shutil.rmtree(
                output_directory,
                ignore_errors=True,
            )

            raise