import hashlib
import pandas as pd

import nugflow.interfaces.vault as sut


def test_vault_hash():
    """
    GIVEN a set of business values {'name': ['A', 'B'], 'foo': [1, 2]}
    WHEN I calculate the hkey
    THEN it should return the hash of the ordered, lowered set of business values
    """
    # Arrange
    fixture = pd.DataFrame(data={"name": ["A", "B"], "foo": [1, 2]})
    val1 = hashlib.md5("1|a".encode()).hexdigest()
    val2 = hashlib.md5("2|b".encode()).hexdigest()
    expected = pd.Series([val1, val2], name="foo")
    # Act
    actual = sut.get_vault_hash(fixture, ["name", "foo"])
    # Assert
    pd.testing.assert_series_equal(actual, expected)
