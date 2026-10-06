import csv
import os
from datetime import datetime
from typing import Any


EXPECTED_COLUMNS = [
    "reference",
    "partner",
    "date",
    "duration_seconds",
    "volume_kb",
    "charge",
]


class RaFileError(ValueError):
    """Raised when an input file cannot be parsed."""


def _parse_float(
    value: Any,
    field: str,
    row_number: int,
) -> float:

    try:
        return float(value)
    except (TypeError, ValueError):
        raise RaFileError(
            f"Row {row_number}: "
            f"'{field}' must be a number "
            f"(got {value!r})."
        )


def _parse_datetime(
    value: str,
    row_number: int,
) -> datetime:

    value = (value or "").strip()

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ):
        try:
            return datetime.strptime(
                value,
                fmt,
            )
        except ValueError:
            continue

    raise RaFileError(
        f"Row {row_number}: "
        f"'date' has unsupported format "
        f"(got {value!r})."
    )


def read_ra_file(
    path: str,
    side: str,
) -> tuple[list[dict], list[str]]:

    """
    Read a roaming CDR CSV file and
    return (records, warnings).

    Expected columns:
        reference, partner, date,
        duration_seconds, volume_kb, charge
    """

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Input file not found: {path}"
        )

    records: list[dict] = []

    warnings: list[str] = []

    with open(
        path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise RaFileError(
                f"{os.path.basename(path)}: "
                f"file is empty."
            )

        missing = [
            column
            for column in EXPECTED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing:
            raise RaFileError(
                f"{os.path.basename(path)}: "
                f"missing columns: "
                f"{', '.join(missing)}."
            )

        for row_number, row in enumerate(
            reader,
            start=2,
        ):

            reference = (
                row.get("reference")
                or ""
            ).strip()

            if not reference:
                warnings.append(
                    f"Row {row_number}: "
                    f"skipped (empty reference)."
                )

                continue

            try:
                record_date = _parse_datetime(
                    row.get("date", ""),
                    row_number,
                )
            except RaFileError as exc:

                warnings.append(
                    str(exc)
                    + " Row skipped."
                )

                continue

            try:

                duration = int(
                    _parse_float(
                        row.get(
                            "duration_seconds",
                        ),
                        "duration_seconds",
                        row_number,
                    ),
                )

                volume = _parse_float(
                    row.get("volume_kb"),
                    "volume_kb",
                    row_number,
                )

                charge = _parse_float(
                    row.get("charge"),
                    "charge",
                    row_number,
                )

            except RaFileError as exc:

                warnings.append(
                    str(exc)
                    + " Row skipped."
                )

                continue

            records.append(
                {
                    "side": side,
                    "reference": reference,
                    "partner": (
                        row.get("partner")
                        or ""
                    ).strip(),
                    "record_date": record_date,
                    "duration_seconds": duration,
                    "volume_kb": volume,
                    "charge": charge,
                    "row_number": row_number,
                },
            )

    return records, warnings
