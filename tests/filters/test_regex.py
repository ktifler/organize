from organize.utils import Path
from organize.filters import Regex


TESTDATA = [
    (Path("~/Invoices/RG123456123456-sig.pdf"), True, "123456123456"),
    (Path("~/Invoices/RG002312321542-sig.pdf"), True, "002312321542"),
    (Path("~/Invoices/RG002312321542.pdf"), False, None),
]


def test_regex_backslash():
    regex = Regex(r"^\.pdf$")
    assert regex.matches(Path(".pdf"))
    assert not regex.matches(Path("+pdf"))
    assert not regex.matches(Path("/pdf"))
    assert not regex.matches(Path(r"\pdf"))


def test_regex_basic():
    regex = Regex(r"^RG(\d{12})-sig\.pdf$")
    for path, match, _ in TESTDATA:
        assert regex.matches(path) == match


def test_regex_return():
    regex = Regex(r"^RG(?P<the_number>\d{12})-sig\.pdf$")
    for path, valid, result in TESTDATA:
        if valid:
            attrs = regex.parse(path)
            assert attrs["regex"].the_number == result


def test_regex_umlaut():
    regex = Regex(r"^Erträgnisaufstellung-(?P<year>\d*)\.pdf")
    doc = Path("~/Documents/Erträgnisaufstellung-1998.pdf")
    assert regex.matches(doc)
    attrs = regex.parse(doc)
    assert attrs["regex"].year == "1998"