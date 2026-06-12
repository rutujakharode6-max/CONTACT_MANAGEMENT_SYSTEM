import unittest
from contacts_manager import validate_phone, validate_email, validate_name

class TestContactManager(unittest.TestCase):
    def test_validate_name(self):
        self.assertTrue(validate_name("John Doe"))
        self.assertFalse(validate_name("John123"))
        self.assertFalse(validate_name(""))

    def test_validate_phone(self):
        self.assertTrue(validate_phone("1234567890"))
        self.assertFalse(validate_phone("12345"))
        self.assertFalse(validate_phone("abcdefghij"))

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("testexample.com"))

if __name__ == '__main__':
    unittest.main()
