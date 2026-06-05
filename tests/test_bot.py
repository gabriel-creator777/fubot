import unittest

from fubot.bot import greet, add


class TestBot(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Mundo"), "Olá, Mundo!")

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)


if __name__ == "__main__":
    unittest.main()
