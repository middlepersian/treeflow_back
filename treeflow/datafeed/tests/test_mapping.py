import pytest
from treeflow.datafeed.management.commands.map_images import map_folio_to_page


@pytest.mark.django_db
def test_map_folio_to_page():
    """Test map_folio_to_page."""
    csv_file = 'treeflow/datafeed/tests/data/L19_folio_page.csv'
    map_folio_to_page(csv_file, 'L19')
