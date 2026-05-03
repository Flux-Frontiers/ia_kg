"""Pytest suite for scripts/download_ia.py text-processing functions."""

import textwrap

from download_ia import _is_heading, clean_ocr, slugify, text_to_markdown


def test_slugify() -> None:
    assert slugify("Audels Electricians Guide Vol. 1") == "audels_electricians_guide_vol_1"
    assert slugify("  Spaces & Symbols!  ") == "spaces_symbols"


def test_ligatures() -> None:
    cases = [
        ("ﬃefficiency", "ffiefficiency"),
        ("ﬁlament", "filament"),
        ("ﬂoor", "floor"),
    ]
    for raw, expected in cases:
        assert expected in clean_ocr(raw), f"Expected {expected!r} in clean_ocr({raw!r})"


def test_smart_quotes() -> None:
    result = clean_ocr("‘quoted’")
    assert "‘" not in result and "’" not in result
    assert "'quoted'" in result

    result2 = clean_ocr("“double”")
    assert "“" not in result2 and "”" not in result2
    assert '"double"' in result2


def test_hyphen_join() -> None:
    assert "electromagnetic" in clean_ocr("electro-\nmagnetic field")
    assert "magnetism" in clean_ocr("mag-\nnetism in the core")


def test_page_numbers() -> None:
    result = clean_ocr("Text.\n\n42\n\nMore text.\n\n1234\n\nEnd.")
    for num in ["42", "1234"]:
        assert f"\n{num}\n" not in result, f"Bare page number {num!r} not removed"
    assert "Text." in result and "More text." in result


def test_index_strip() -> None:
    body = "\n".join(f"Sentence {i} about electricity and circuits." for i in range(200))
    index = "\nINDEX\n\nAlternating current, 12, 45\nDirect current, 8, 22\n"
    result = clean_ocr(body + index)
    assert "Alternating current, 12" not in result
    assert "Sentence 0" in result
    assert "Sentence 199" in result


def test_running_headers() -> None:
    header = "AUDELS ELECTRICIANS GUIDE"
    body = "\n".join(
        header + "\n" + f"Unique text about topic {i} in electrical engineering." for i in range(50)
    )
    result = clean_ocr(body)
    occurrences = sum(1 for ln in result.split("\n") if ln.strip() == header)
    assert occurrences == 0, f"Running header appeared {occurrences} times after cleaning"


def test_heading_detection() -> None:
    expected = [
        ("CHAPTER I", 2),
        ("CHAPTER XIV", 2),
        ("CHAPTER 3. Alternating Current", 2),
        ("PART ONE", 2),
        ("PART II - WIRING METHODS", 2),
        ("SECTION 4", 2),
        ("DIVISION III", 2),
        ("DIRECT CURRENTS", 3),
        ("OHM'S LAW AND ITS APPLICATIONS", 3),
        ("MAGNETISM AND ELECTRICITY", 3),
        ("Ques. What is an electric current?", 4),
        ("Ques. How does a transformer work in practice?", 4),
    ]
    for line, level in expected:
        result = _is_heading(line)
        assert result is not None, f"Expected heading, got None: {line!r}"
        assert result[0] == level, f"{line!r}: expected h{level}, got h{result[0]}"

    not_headings = [
        "The current flows through the wire.",
        "Ans. The voltage is the potential difference.",
        "a",
        "42",
        "This is a long sentence that should not be treated as a heading.",
        "it starts lowercase",
    ]
    for line in not_headings:
        assert _is_heading(line) is None, f"False positive heading: {line!r}"


def test_markdown_conversion() -> None:
    sample = textwrap.dedent("""
        CONTENTS
        Chapter I - Direct Currents....... 1
        Chapter II - Alternating Currents.. 45

        CHAPTER I

        DIRECT CURRENTS

        Ques. What is an electric current?

        Ans. An electric current is a flow of electrons through a conductor.
        The direction of flow determines the polarity.

        CHAPTER II

        ALTERNATING CURRENTS

        Ques. How does alternating current differ from direct current?

        Ans. Alternating current periodically reverses direction, while
        direct current flows continuously in one direction.
    """).strip()

    meta = {
        "title": "Audels Electricians and Plumbers Guide",
        "author": "Edwin P. Anderson",
        "publisher": "Theo. Audel and Co.",
        "date": "1928",
        "series": "Audels Electricians and Plumbers Guide",
        "volume": "1",
    }
    md = text_to_markdown(sample, meta)

    expected_present = {
        "title h1": "# Audels Electricians and Plumbers Guide",
        "CHAPTER I h2": "## CHAPTER I",
        "CHAPTER II h2": "## CHAPTER II",
        "DIRECT CURRENTS h3": "### DIRECT CURRENTS",
        "ALTERNATING h3": "### ALTERNATING CURRENTS",
        "first Ques h4": "#### Ques. What is an electric current?",
        "answer body text": "Ans. An electric current is a flow",
        "publisher front matter": "*Theo. Audel and Co., 1928*",
        "series front matter": "*Audels Electricians and Plumbers Guide, Vol. 1*",
    }
    for label, text in expected_present.items():
        assert text in md, f"Missing {label!r}: {text!r}"

    for toc_entry in [
        "Chapter I - Direct Currents....... 1",
        "Chapter II - Alternating Currents.. 45",
    ]:
        assert toc_entry not in md, f"TOC entry not stripped: {toc_entry!r}"
