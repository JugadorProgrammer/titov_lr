import unittest
from operations import modulo


class ModuloTests(unittest.TestCase):
    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)


if __name__ == "__main__":
    unittest.main()
