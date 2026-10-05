from __future__ import annotations

from dataclasses import dataclass, field

import pdfplumber


@dataclass
class PdfText:
    text: str
    x0: float
    top: float
    x1: float
    bottom: float
    fontname: str | None = None
    size: float | None = None


@dataclass
class PdfTable:
    rows: list[list[str]]
    x0: float
    top: float
    x1: float
    bottom: float


@dataclass
class PdfPage:
    number: int
    width: float
    height: float

    texts: list[PdfText] = field(
        default_factory=list
    )

    tables: list[PdfTable] = field(
        default_factory=list
    )


def clean_text(value: object) -> str:
    if value is None:
        return ""

    return (
        str(value)
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )


def extract_pdf_content(
    file_path: str,
) -> list[PdfPage]:

    pages: list[PdfPage] = []

    with pdfplumber.open(file_path) as pdf:

        for page_number, page in enumerate(
            pdf.pages,
            start=1,
        ):

            pdf_page = PdfPage(
                number=page_number,
                width=page.width,
                height=page.height,
            )

            # --------------------------------
            # Extract text with coordinates
            # --------------------------------

            words = page.extract_words(
                keep_blank_chars=False,
                use_text_flow=True,
                extra_attrs=[
                    "fontname",
                    "size",
                ],
            )

            for word in words:

                text = clean_text(
                    word.get("text")
                )

                if not text:
                    continue

                pdf_page.texts.append(
                    PdfText(
                        text=text,
                        x0=float(
                            word.get("x0", 0)
                        ),
                        top=float(
                            word.get("top", 0)
                        ),
                        x1=float(
                            word.get("x1", 0)
                        ),
                        bottom=float(
                            word.get("bottom", 0)
                        ),
                        fontname=word.get(
                            "fontname"
                        ),
                        size=(
                            float(word["size"])
                            if word.get("size")
                            else None
                        ),
                    )
                )

            # --------------------------------
            # Extract tables
            # --------------------------------

            tables = page.find_tables()

            for table in tables:

                extracted = table.extract()

                if not extracted:
                    continue

                cleaned_rows: list[list[str]] = []

                for row in extracted:

                    if not row:
                        continue

                    cleaned_row = [
                        clean_text(cell)
                        for cell in row
                    ]

                    # Skip completely empty rows
                    if not any(cleaned_row):
                        continue

                    cleaned_rows.append(
                        cleaned_row
                    )

                if not cleaned_rows:
                    continue

                bbox = table.bbox

                pdf_page.tables.append(
                    PdfTable(
                        rows=cleaned_rows,
                        x0=float(bbox[0]),
                        top=float(bbox[1]),
                        x1=float(bbox[2]),
                        bottom=float(bbox[3]),
                    )
                )

            pages.append(pdf_page)

    return pages