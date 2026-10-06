from __future__ import annotations

from datetime import datetime


def classify_root_cause(
    charge_variance: float,
    duration_variance: int,
    volume_variance: float,
    date_a: datetime,
    date_b: datetime,
    partner_a: str,
    partner_b: str,
) -> str:
    """
    Deterministic rules, ordered from
    most to least specific.
    """

    # 1. Different partners: likely a
    #    reference collision across carriers.
    if (
        partner_a
        and partner_b
        and partner_a != partner_b
    ):
        return "partner_mismatch"

    # 2. Different dates: possible day
    #    boundary / timezone issue.
    if date_a.date() != date_b.date():
        return "date_mismatch"

    # 3. Same charge but usage differs:
    #    rating data issue.
    if (
        abs(charge_variance) <= 0.01
        and (
            duration_variance != 0
            or abs(volume_variance) > 0.01
        )
    ):
        return "usage_mismatch"

    # 4. Charge differs while usage is
    #    identical: tariff/rate difference.
    if (
        duration_variance == 0
        and abs(volume_variance) <= 0.01
    ):
        return "rate_mismatch"

    # 5. Side B charged more.
    if charge_variance < 0:
        return "undercharge_side_a"

    # 6. Side A charged more.
    if charge_variance > 0:
        return "overcharge_side_a"

    return "unclassified"
