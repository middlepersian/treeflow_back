import pytest
from mpcd.corpus.models import Line
from mpcd.corpus.tests.factories import LineFactory


@pytest.mark.django_db
def test_line_factory():
    line = LineFactory()
    assert isinstance(line, Line)
    assert line.folio is not None
    assert line.number is not None
    assert line.number_in_text is not None
    assert line.previous is not None
    assert line.identifier is not None
    previous_line = line.previous
    assert isinstance(previous_line, Line)