import unittest
import blackjack3


class MyTestCase(unittest.TestCase):

    def test_score(self):
        ret = blackjack3.Hand([3, 12])
        self.assertEqual(ret.score(), (13, 0))

    def test_add_card(self):
        ret = blackjack3.Hand()
        ret.add_card()
        self.assertEqual(len(ret.cards), 1)

    def test_is_blackjack(self):
        ret = blackjack3.Hand([1, 12])
        self.assertTrue(ret.is_blackjack())

    def test_is_blackjack_false(self):
        ret = blackjack3.Hand([13, 8])
        self.assertFalse(ret.is_blackjack())

    def test_is_bust(self):
        ret = blackjack3.Hand([7, 5, 13])
        self.assertTrue(ret.is_bust())

    def test_is_bust_false(self):
        ret = blackjack3.Hand([7, 5])
        self.assertFalse(ret.is_bust())

    def test_stand_soft(self):
        ret = blackjack3.Strategy(16, True).stand(blackjack3.Hand([1, 7]))
        self.assertTrue(ret[0])

    def test_stand_hard(self):
        ret = blackjack3.Strategy(16, False).stand(blackjack3.Hand([1, 7]))
        self.assertFalse(ret[0])

    def test_play_hand(self):
        ret = blackjack3.Strategy(13, True).play()
        self.assertTrue(ret.score()[0] >= 13)

if __name__ == '__main__':
    unittest.main()
