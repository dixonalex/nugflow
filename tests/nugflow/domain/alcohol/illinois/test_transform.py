from nugflow.domain.alcohol.illinois.transform import transform, split_address


class TestAlcoholIllinoisTransform:
    def test_smoke_test(self, path_to_illinois_extract: str):
        """
        GIVEN a test file
        WHEN I transform it
        THEN it should process without fail
        """
        print(path_to_illinois_extract)
        out = transform(path_to_illinois_extract, "2019-11-06")
        assert len(out) > 0

    def test_simple_address(self):
        """
        GIVEN an address string
        WHEN I split it
        THEN there should be a street_address, city, state, zip value
        """
        # Arrange
        addr = "217 FRONT ST\n\nMCHENRY IL, 60050550"
        # Act
        sa, city, state, _zip = split_address(addr)
        # Assert
        assert sa == "217 FRONT ST"
        assert city == "MCHENRY"
        assert state == "IL"
        assert _zip == "60050550"

    def test_address_with_single_newline(self):
        """
        GIVEN an address string
        WHEN I split it
        THEN there should be a street_address, city, state, zip value
        """
        # Arrange
        addr = "217 FRONT ST\nMCHENRY IL, 60050550"
        # Act
        sa, city, state, _zip = split_address(addr)
        # Assert
        assert sa == "217 FRONT ST"
        assert city == "MCHENRY"
        assert state == "IL"
        assert _zip == "60050550"

    def test_multiline_address(self):
        """
        GIVEN an address string with a second line
        WHEN I split it
        THEN there should be a street_address, city, state, zip value
        """
        # Arrange
        addr = "217 FRONT ST\n\nSUITE 135\n\nMCHENRY IL, 60050550"
        # Act
        sa, city, state, _zip = split_address(addr)
        # Assert
        assert sa == "217 FRONT ST SUITE 135"
        assert city == "MCHENRY"
        assert state == "IL"
        assert _zip == "60050550"

    def test_address_with_space_in_city_name(self):
        """
        GIVEN an address string with a space in the city name
        WHEN I split it
        THEN there should be a street_address, city, state, zip value
        """
        # Arrange
        addr = "1051 HIGHLAND GROVE DR\n\nBUFFALO GROVE IL, 600897026"
        # Act
        sa, city, state, _zip = split_address(addr)
        # Assert
        assert sa == "1051 HIGHLAND GROVE DR"
        assert city == "BUFFALO GROVE"
        assert state == "IL"
        assert _zip == "600897026"
