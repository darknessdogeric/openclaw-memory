"""Tests for the text cleaning module."""

import pytest

from cleaner import (
    _collapse_whitespace,
    _expand_abbreviations,
    _normalize_typography,
    _rejoin_hyphenated_words,
    _remove_page_numbers,
    _remove_urls_and_refs,
    clean_text,
)
from models import Page


class TestRemovePageNumbers:
    def test_removes_standalone_number(self):
        text = "Some text.\n42\nMore text."
        result = _remove_page_numbers(text)
        assert "42" not in result
        assert "Some text." in result
        assert "More text." in result

    def test_removes_number_with_dashes(self):
        text = "Some text.\n- 42 -\nMore text."
        result = _remove_page_numbers(text)
        assert "42" not in result

    def test_keeps_numbers_in_context(self):
        text = "There are 42 cats in the garden."
        result = _remove_page_numbers(text)
        assert "42" in result

    def test_removes_single_digit(self):
        text = "Line before.\n5\nLine after."
        result = _remove_page_numbers(text)
        assert "\n5\n" not in result

    def test_keeps_five_digit_numbers(self):
        text = "Code: 12345"
        result = _remove_page_numbers(text)
        assert "12345" in result


class TestRejoinHyphenatedWords:
    def test_basic_hyphenation(self):
        text = "transfor-\nmación del texto"
        result = _rejoin_hyphenated_words(text)
        assert result == "transformación del texto"

    def test_preserves_real_hyphens(self):
        text = "well-known\nfact"
        result = _rejoin_hyphenated_words(text)
        assert "wellknown" in result or "well-known" in result

    def test_no_join_uppercase(self):
        text = "some-\nAmazing word"
        result = _rejoin_hyphenated_words(text)
        assert "-" in result

    def test_spanish_characters(self):
        text = "comuni-\ncación efectiva"
        result = _rejoin_hyphenated_words(text)
        assert "comunicación" in result


class TestNormalizeTypography:
    def test_curly_quotes_to_straight(self):
        text = "\u201cHello\u201d"
        result = _normalize_typography(text)
        assert result == '"Hello"'

    def test_single_curly_quotes(self):
        text = "\u2018word\u2019"
        result = _normalize_typography(text)
        assert result == "'word'"

    def test_em_dash_to_comma(self):
        text = "word\u2014another"
        result = _normalize_typography(text)
        assert result == "word, another"

    def test_en_dash_to_comma(self):
        text = "word\u2013another"
        result = _normalize_typography(text)
        assert result == "word, another"

    def test_ellipsis(self):
        text = "wait\u2026"
        result = _normalize_typography(text)
        assert result == "wait..."

    def test_guillemets(self):
        text = "\u00abcita\u00bb"
        result = _normalize_typography(text)
        assert result == '"cita"'

    def test_non_breaking_space(self):
        text = "hello\u00a0world"
        result = _normalize_typography(text)
        assert result == "hello world"


class TestExpandAbbreviations:
    def test_spanish_abbreviations(self):
        text = "Ver pág. 42 para el nº de referencia."
        result = _expand_abbreviations(text, "es")
        assert "página" in result
        assert "número" in result

    def test_spanish_titles(self):
        text = "El Sr. García y la Dra. López."
        result = _expand_abbreviations(text, "es")
        assert "Señor" in result
        assert "Doctora" in result

    def test_english_abbreviations(self):
        text = "Dr. Smith and Prof. Jones, etc."
        result = _expand_abbreviations(text, "en")
        assert "Doctor" in result
        assert "Professor" in result
        assert "etcetera" in result

    def test_unknown_language_no_crash(self):
        text = "Some text."
        result = _expand_abbreviations(text, "fr")
        assert result == text


class TestRemoveUrlsAndRefs:
    def test_removes_http_url(self):
        text = "Visit https://example.com/page for more info."
        result = _remove_urls_and_refs(text)
        assert "https://example.com" not in result
        assert "Visit" in result

    def test_removes_www_url(self):
        text = "Go to www.example.com for details."
        result = _remove_urls_and_refs(text)
        assert "www.example.com" not in result

    def test_removes_numeric_citations(self):
        text = "As shown in previous work [1] and [2, 3]."
        result = _remove_urls_and_refs(text)
        assert "[1]" not in result
        assert "[2, 3]" not in result

    def test_removes_author_year_citations(self):
        text = "According to (Smith, 2020) and (García et al., 2019)."
        result = _remove_urls_and_refs(text)
        assert "(Smith, 2020)" not in result
        assert "(García et al., 2019)" not in result


class TestCollapseWhitespace:
    def test_multiple_spaces(self):
        text = "hello    world"
        result = _collapse_whitespace(text)
        assert result == "hello world"

    def test_multiple_newlines(self):
        text = "para1\n\n\n\n\npara2"
        result = _collapse_whitespace(text)
        assert result == "para1\n\npara2"

    def test_preserves_double_newline(self):
        text = "para1\n\npara2"
        result = _collapse_whitespace(text)
        assert result == "para1\n\npara2"


class TestCleanTextIntegration:
    def test_full_cleaning_pipeline(self):
        pages = [
            Page(number=1, text="Header Line\n\nSome content on page one.\n\n1"),
            Page(number=2, text="Header Line\n\nMore content on page two.\n\n2"),
            Page(number=3, text="Header Line\n\nFinal content on page three.\n\n3"),
            Page(number=4, text="Header Line\n\nExtra content here.\n\n4"),
        ]
        result = clean_text(pages, language="es")
        for page in result:
            lines = page.text.split("\n")
            for line in lines:
                stripped = line.strip()
                assert not (stripped.isdigit() and len(stripped) <= 4), (
                    f"Page number not removed: '{stripped}'"
                )

    def test_empty_pages_filtered(self):
        pages = [
            Page(number=1, text="Real content here."),
            Page(number=2, text="   \n\n   "),
        ]
        result = clean_text(pages, language="es")
        assert len(result) >= 1
        assert any("Real content" in p.text for p in result)

    def test_preserves_urls_when_flag_off(self):
        pages = [Page(number=1, text="Visit https://example.com for info.")]
        result = clean_text(pages, language="es", remove_urls=False)
        assert "https://example.com" in result[0].text
