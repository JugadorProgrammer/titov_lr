import unittest
from operations import multiply


class MultiplyTests(unittest.TestCase):
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)


if __name__ == "__main__":
    unittest.main()
