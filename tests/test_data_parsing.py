import unittest
from model import NsrEnhetTinyApiModel, NsrEnhetApiModel


class TestEmailParsing(unittest.TestCase):
    def setUp(self):
        self.input = {
            "Orgnr": "12345",
            "Navn": "Galtvort"
        }

    def test_empty_email_becomes_none(self):
        self.input.update({"Epost": ""})
        unit = NsrEnhetTinyApiModel.model_validate(self.input)
        self.assertEqual(unit.email, None)

    def test_normal_email(self):
        self.input.update({"Epost": "test@example.com"})
        unit = NsrEnhetTinyApiModel.model_validate(self.input)
        self.assertEqual(unit.email, "test@example.com")

    def test_multiple_emails(self):
        self.input.update({"Epost": "test@example.com;test2@example.com"})
        unit = NsrEnhetTinyApiModel.model_validate(self.input)
        self.assertEqual(unit.email, "test@example.com;test2@example.com")

    def test_whitespace_stripped_from_email(self):
        self.input.update({"Epost": "  test@example.com  "})
        unit = NsrEnhetTinyApiModel.model_validate(self.input)
        self.assertEqual(unit.email, "test@example.com")


class TestCoordinateParsing(unittest.TestCase):
    def setUp(self):
        self.input = {
            "Orgnr": "12345",
            "Navn": "Galtvort",
            "Koordinat": {
                "Breddegrad": 0,
                "Lengdegrad": 0
            }
        }

    def test_zero_coordinates(self):
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0)
        self.assertEqual(unit.coordinate.longitude, 0)

    def test_positive_coordinates(self):
        self.input["Koordinat"]["Breddegrad"] = 61
        self.input["Koordinat"]["Lengdegrad"] = 22
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 61)
        self.assertEqual(unit.coordinate.longitude, 22)

    def test_negative_coordinates(self):
        self.input["Koordinat"]["Breddegrad"] = -61
        self.input["Koordinat"]["Lengdegrad"] = -22
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, -61)
        self.assertEqual(unit.coordinate.longitude, -22)

    def test_both_coordinates_none(self):
        self.input["Koordinat"]["Breddegrad"] = None
        self.input["Koordinat"]["Lengdegrad"] = None
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0)
        self.assertEqual(unit.coordinate.longitude, 0)

    def test_both_coordinates_missing(self):
        self.input["Koordinat"] = {}
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0)
        self.assertEqual(unit.coordinate.longitude, 0)

    def test_lat_missing(self):
        self.input["Koordinat"] = {"Lengdegrad": 10}
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0, "Lat should be zero")
        self.assertEqual(unit.coordinate.longitude, 0, "Lon should be zero")

    def test_lon_missing(self):
        self.input["Koordinat"] = {"Breddegrad": 10}
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0, "Lat should be zero")
        self.assertEqual(unit.coordinate.longitude, 0, "Lon should be zero")

    def test_lat_none(self):
        self.input["Koordinat"]["Breddegrad"] = None
        self.input["Koordinat"]["Lengdegrad"] = 10
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0, "Lat should be zero")
        self.assertEqual(unit.coordinate.longitude, 0, "Lon should be zero")

    def test_lon_none(self):
        self.input["Koordinat"]["Breddegrad"] = 10
        self.input["Koordinat"]["Lengdegrad"] = None
        unit = NsrEnhetApiModel.model_validate(self.input)
        self.assertEqual(unit.coordinate.latitude, 0, "Lat should be zero")
        self.assertEqual(unit.coordinate.longitude, 0, "Lon should be zero")
