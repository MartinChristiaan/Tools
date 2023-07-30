"""CHANGEME: These are shared resources for all of your tests.

Docs: https://docs.pytest.org/en/6.2.x/fixture.html
"""
import pytest


@pytest.fixture
def shared_resource() -> int:
    """Some resource which can easily be used in multiple different tests. Called a `fixture`

    For more info see: https://docs.pytest.org/en/7.1.x/explanation/fixtures.html
    """
    # Some code
    x = 1

    return x
