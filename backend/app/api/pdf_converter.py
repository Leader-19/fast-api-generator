from __future__ import annotations

import os
import shutil
import tempfile
import traceback
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from fastapi.responses import FileResponse

from starlette.background import BackgroundTask

from app.auth.dependencies import (
    require_permission,
)

from app.services.pdf_converter_service import (
    PdfConverterService,
)


router = APIRouter(
    prefix="/api/pdf-converter",
    tags=["PDF Converter"],
)


pdf_converter_service = (
    PdfConverterService()
)


def cleanup_path(
    path: str | None,
) -> None:

    if not path:
        return

    try:

        if os.path.isdir(path):

            shutil.rmtree(
                path,
                ignore_errors=True,
            )

        elif os.path.exists(path):

            os.remove(path)

    except OSError:

        pass


def cleanup_paths(
    *paths: str | None,
) -> None:

    for path in paths:
        cleanup_path(path)


def validate_pdf(
    file: UploadFile,
) -> None:

    if not file.filename:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select a PDF file.",
        )

    if not file.filename.lower().endswith(
        ".pdf"
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )


async def save_uploaded_file(
    file: UploadFile,
) -> tuple[str, str]:

    upload_directory = tempfile.mkdtemp(
        prefix="pdf_upload_"
    )

    pdf_path = os.path.join(
        upload_directory,
        "source.pdf",
    )

    try:

        with open(
            pdf_path,
            "wb",
        ) as output:

            shutil.copyfileobj(
                file.file,
                output,
            )

        return (
            upload_directory,
            pdf_path,
        )

    except Exception:

        cleanup_path(
            upload_directory
        )

        raise


@router.post(
    "/excel",
    dependencies=[
        Depends(
            require_permission(
                "pdf_converter.create"
            )
        )
    ],
)
async def convert_pdf_to_excel(
    file: UploadFile = File(...),
):

    validate_pdf(file)

    upload_directory = None
    output_path = None
    output_directory = None

    try:

        (
            upload_directory,
            pdf_path,
        ) = await save_uploaded_file(
            file
        )

        output_path = (
            pdf_converter_service.convert_to_excel(
                pdf_path
            )
        )

        output_directory = os.path.dirname(
            output_path
        )

        original_name = Path(
            file.filename
        ).stem

        download_name = (
            f"{original_name}.xlsx"
        )

        return FileResponse(
            path=output_path,
            filename=download_name,
            media_type=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            background=BackgroundTask(
                cleanup_paths,
                upload_directory,
                output_directory,
            ),
        )

    except HTTPException:

        cleanup_paths(
            upload_directory,
            output_directory,
        )

        raise

    except Exception as exc:

        print(
            "\n========== PDF → EXCEL ERROR =========="
        )

        print(
            repr(exc)
        )

        traceback.print_exc()

        print(
            "========================================\n"
        )

        cleanup_paths(
            upload_directory,
            output_directory,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "PDF to Excel conversion failed: "
                f"{exc}"
            ),
        )

    finally:

        await file.close()


@router.post(
    "/word",
    dependencies=[
        Depends(
            require_permission(
                "pdf_converter.create"
            )
        )
    ],
)
async def convert_pdf_to_word(
    file: UploadFile = File(...),
):

    validate_pdf(file)

    upload_directory = None
    output_path = None
    output_directory = None

    try:

        (
            upload_directory,
            pdf_path,
        ) = await save_uploaded_file(
            file
        )

        output_path = (
            pdf_converter_service.convert_to_word(
                pdf_path
            )
        )

        output_directory = os.path.dirname(
            output_path
        )

        original_name = Path(
            file.filename
        ).stem

        download_name = (
            f"{original_name}.docx"
        )

        return FileResponse(
            path=output_path,
            filename=download_name,
            media_type=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            background=BackgroundTask(
                cleanup_paths,
                upload_directory,
                output_directory,
            ),
        )

    except HTTPException:

        cleanup_paths(
            upload_directory,
            output_directory,
        )

        raise

    except Exception as exc:

        print(
            "\n========== PDF → WORD ERROR =========="
        )

        print(
            repr(exc)
        )

        traceback.print_exc()

        print(
            "======================================\n"
        )

        cleanup_paths(
            upload_directory,
            output_directory,
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "PDF to Word conversion failed: "
                f"{exc}"
            ),
        )

    finally:

        await file.close()