import unittest

from fubot.bot import greet, add, shout


class TestBot(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("Mundo"), "Olá, Mundo!")

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_shout(self):
        self.assertEqual(shout("oi"), "OI!")
        self.assertEqual(shout("Olá"), "OLÁ!")


if __name__ == "__main__":
    unittest.main()
