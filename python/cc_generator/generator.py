"""Generate Luhn-valid test credit card numbers and fake identities."""
from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Optional

# Common BINs
VISA_BINS = [
    {"bin": "415464440635", "brand": "visa", "lengths": [16], "cvv": 3},
    {"bin": "400000", "brand": "visa", "lengths": [16], "cvv": 3},
]

UNIONPAY_BINS = [
    {"bin": "6233586370", "brand": "unionpay", "lengths": [16, 17, 18, 19], "cvv": 3},
]

MASTERCARD_BINS = [
    {"bin": "555555", "brand": "mastercard", "lengths": [16], "cvv": 3},
]

AMEX_BINS = [
    {"bin": "378282", "brand": "amex", "lengths": [15], "cvv": 4},
]

DISCOVER_BINS = [
    {"bin": "601111", "brand": "discover", "lengths": [16], "cvv": 3},
]

DEFAULT_BINS = VISA_BINS + UNIONPAY_BINS + MASTERCARD_BINS + AMEX_BINS + DISCOVER_BINS


# --------------------------------------------------------------------------- Luhn

def luhn_ok(number: str) -> bool:
    """Return True if the digit string passes the Luhn check."""
    total, alt = 0, False
    for ch in reversed(re.sub(r"\D", "", number)):
        n = int(ch)
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        total += n
        alt = not alt
    return total % 10 == 0


def luhn_complete(prefix: str, length: int) -> str:
    """Append random digits + a valid check digit so the result passes Luhn."""
    body = prefix + "".join(random.choice("0123456789") for _ in range(length - 1 - len(prefix)))
    for d in "0123456789":
        cand = body + d
        if luhn_ok(cand):
            return cand
    raise RuntimeError("luhn: no check digit found")


# --------------------------------------------------------------------------- card

def gen_card(bin_spec: Optional[dict] = None, bins: Optional[list] = None) -> dict:
    """Generate a single fake card dict.

    Args:
        bin_spec: Explicit BIN dict. If None, picks from ``bins``.
        bins: List of BIN dicts. Defaults to ``DEFAULT_BINS``.

    Returns:
        dict with keys: number, bin, brand, exp_month, exp_year, exp, cvv, luhn.
    """
    spec = bin_spec or random.choice(bins or DEFAULT_BINS)
    length = random.choice(spec["lengths"])
    number = luhn_complete(spec["bin"], length)
    month = random.randint(1, 12)
    year_offset = random.randint(2, 6)
    year = 2026 + year_offset
    cvv_len = spec.get("cvv", 3)
    cvv = "".join(random.choice("0123456789") for _ in range(cvv_len))
    return {
        "number": number,
        "bin": spec["bin"],
        "brand": spec["brand"],
        "exp_month": f"{month:02d}",
        "exp_year": str(year),
        "exp": f"{month:02d}/{str(year)[-2:]}",
        "cvv": cvv,
        "luhn": luhn_ok(number),
    }


def gen_cards(count: int = 1, bins: Optional[list] = None) -> list[dict]:
    """Generate ``count`` cards."""
    return [gen_card(bins=bins) for _ in range(count)]


# --------------------------------------------------------------------------- identity

_FIRST = [
    "Marcus", "Delaney", "Elena", "Tobias", "Priya", "Owen", "Nadia", "Felix",
    "Iris", "Jonah", "Celine", "Rafael", "Maya", "Dorian", "Sofia",
]
_LAST = [
    "Whitfield", "Navarro", "Lindqvist", "Okafor", "Brennan", "Halvorsen",
    "Castellano", "Duarte", "Mercer", "Ashford", "Kowalski", "Ferreira",
]
_STREETS = [
    "Sunset Ridge Drive", "Maple Court", "Easton Avenue", "Willow Bend Road",
    "Chestnut Street", "Harbor View Lane", "Kingsway Boulevard",
]
_CITIES = [
    ("Austin", "Texas", "78701"),
    ("Denver", "Colorado", "80202"),
    ("Portland", "Oregon", "97204"),
    ("Raleigh", "North Carolina", "27601"),
    ("Boise", "Idaho", "83702"),
    ("Tampa", "Florida", "33602"),
]


def gen_identity() -> dict:
    """Generate a fake US identity."""
    fn, ln = random.choice(_FIRST), random.choice(_LAST)
    city, state, zipc = random.choice(_CITIES)
    return {
        "name": f"{fn} {ln}",
        "company": "N/A",
        "address": f"{random.randint(100, 9899)} {random.choice(_STREETS)}",
        "city": city,
        "state": state,
        "zip": zipc,
        "country": "US",
        "countryCode": "1",
        "phone": f"{random.randint(201, 989)}{random.randint(200, 999)}{random.randint(1000, 9999)}",
    }
