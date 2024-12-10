"""Copyright (C) 2024 felipepimentel plc"""


def test_import() -> None:
    """Test that poetflow can be imported."""
    try:
        import poetflow  # noqa: F401

        assert True  # If we get here, import succeeded
    except ImportError as e:
        raise AssertionError("Failed to import poetflow") from e
