"""CHANGEME: These are example tests, change them as you see fit.

Docs: https://docs.pytest.org/en/6.2.x/getting-started.html
"""


def test_rename_me():
    """An example

    For more info see: https://docs.pytest.org/en/7.1.x/
    """
    # Some unit of code
    x = 1

    # Some test using asserts
    assert x == 1, "X should be 1 because ..."  # Add explanation to your assert!


def test_shared_resouce(shared_resource):
    """Demonstrates how to use a shared resource, defined in `conftest.py`

    Args:
        shared_resource: This is a shared resource providing ...
    """
    # Some unit of code (using the shared resource)
    x = shared_resource

    # Some test using asserts
    assert x == 1, "X should be 1 because ..."  # Add explanation to your assert!
