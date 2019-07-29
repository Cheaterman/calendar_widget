import pytest


def test_flower():
    from kivy.garden.calendar_widget import Calendar
    calendar = Calendar()
    assert calendar is not None

