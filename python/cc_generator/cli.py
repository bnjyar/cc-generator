"""CLI for cc-generator."""
from __future__ import annotations

import argparse
import json
import sys

from .generator import gen_card, gen_cards, gen_identity, luhn_ok, DEFAULT_BINS


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate Luhn-valid test credit cards")
    ap.add_argument("--count", type=int, default=1, help="how many cards to generate")
    ap.add_argument("--bin", help="specific BIN prefix (e.g. 415464440635)")
    ap.add_argument("--brand", choices=["visa", "unionpay", "mastercard", "amex", "discover"],
                    help="filter by brand")
    ap.add_argument("--length", type=int, help="force card length")
    ap.add_argument("--identity", action="store_true", help="also output a fake identity")
    ap.add_argument("--json", action="store_true", help="output as JSON")
    a = ap.parse_args()

    bins = DEFAULT_BINS
    if a.brand:
        bins = [b for b in bins if b["brand"] == a.brand]
    if a.bin:
        # override with a single custom bin
        spec = {"bin": a.bin, "brand": "custom", "lengths": [a.length or 16], "cvv": 3}
        bins = [spec]

    results = gen_cards(count=a.count, bins=bins)

    for card in results:
        card["luhn"] = luhn_ok(card["number"])

    if a.identity:
        ident = gen_identity()
    else:
        ident = None

    if a.json:
        out = {"cards": results}
        if ident:
            out["identity"] = ident
        print(json.dumps(out, indent=2))
    else:
        for c in results:
            print(f"{c['number']}  {c['exp']}  {c['cvv']}  {c['brand']}  luhn={c['luhn']}")
        if ident:
            print(f"Identity: {ident['name']}, {ident['address']}, {ident['city']} {ident['zip']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
