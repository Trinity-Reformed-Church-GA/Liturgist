"""Tests for liturgist.core module."""

import tempfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from liturgist.core import (
    get_scripture_text,
    load_template_from_file,
    next_sunday,
    process_schedule_data,
    read_schedule,
)


def test_next_sunday():
    """Test next_sunday function returns a date."""
    result = next_sunday()
    assert isinstance(result, type(datetime.now().date()))


def test_read_schedule_csv():
    """Test reading a CSV schedule file."""
    # Create a temporary CSV file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("Header Row\n")
        f.write("Date,Hymn 1,Scripture\n")
        f.write("2024-02-18,Hymn 290,Acts 2:34-35\n")
        temp_path = f.name

    try:
        df = read_schedule(temp_path)
        assert isinstance(df, pd.DataFrame)
        assert "Date" in df.columns
        assert "Hymn 1" in df.columns
        assert "Scripture" in df.columns
    finally:
        Path(temp_path).unlink()


def test_read_schedule_unsupported():
    """Test reading an unsupported file format raises ValueError."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="Unexpected schedule file type"):
            read_schedule(temp_path)
    finally:
        Path(temp_path).unlink()


def test_load_template_from_file():
    """Test loading a template file."""
    template_content = "Hello {{name}}!"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(template_content)
        temp_path = f.name

    try:
        template = load_template_from_file(temp_path)
        result = template({"name": "World"})
        assert result == "Hello World!"
    finally:
        Path(temp_path).unlink()


def test_get_scripture_text():
    """Test scripture text extraction."""
    # This is a basic test - the function is complex and would need more extensive testing
    bible_data = {"books": []}

    result = get_scripture_text(bible_data, "John 3:16")
    # With no books, should return empty string
    assert result == ""


def test_process_schedule_data():
    """Test processing schedule data for a date."""
    # Create test schedule DataFrame
    data = {
        "Date": ["2024-02-18"],
        "Hymn 1": ["Hymn 290 - Hallelujah, Praise Jehovah"],
        "Scripture": ["Acts 2:34-35"],
        "Question": ["Q50. What is required in the second commandment?"],
        "Answer": [
            "A. The second commandment requireth the receiving, observing, and keeping pure and entire, all such religious worship and ordinances as God hath appointed in his Word."
        ],
    }
    schedule = pd.DataFrame(data)

    date = pd.to_datetime("2024-02-18").date()
    result = process_schedule_data(schedule, date)

    assert result["DATE"] == "2024-02-18"
    assert result["FORMATTED_DATE"] == "Sunday, February 18, 2024"
    assert result["HYMNS"] == "Hymn 290 - Hallelujah, Praise Jehovah"
    assert result["SCRIPTURE"] == "Acts 2:34-35"
    assert (
        result["CATECHISM_QUESTION"]
        == "Q50. What is required in the second commandment?"
    )
    assert (
        result["CATECHISM_ANSWER"]
        == "A. The second commandment requireth the receiving, observing, and keeping pure and entire, all such religious worship and ordinances as God hath appointed in his Word."
    )


def test_process_schedule_data_date_not_found():
    """Test processing schedule data with date not in schedule."""
    data = {
        "Date": [pd.to_datetime("2024-02-18").date()],
        "Hymn 1": ["Hymn 290"],
    }
    schedule = pd.DataFrame(data)

    date = pd.to_datetime("2024-02-25").date()

    with pytest.raises(ValueError, match="Date .* was not found in the schedule"):
        process_schedule_data(schedule, date)
