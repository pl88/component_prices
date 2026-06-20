from decimal import Decimal

import pytest

from scraper.scraper import parse_price_pln


def test_parse_price_pln_from_selector() -> None:
    html = """
    <html>
      <body>
        <span data-name="ProductPrice">2 199,99 zł</span>
      </body>
    </html>
    """
    assert parse_price_pln(html) == Decimal("2199.99")


def test_parse_price_pln_raises_when_missing() -> None:
    with pytest.raises(ValueError):
        parse_price_pln("<html><body>No price here</body></html>")
