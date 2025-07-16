import pytest
from vep_mcp.bridge import Bridge


@pytest.fixture
def bridge():
    """Fixture for VEP Bridge."""
    return Bridge()
