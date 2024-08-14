import unittest
from blackjack_with_split import Player, Deck, Hand, Card


#!!To run: run "python -m unittest test_player_split.py" in terminal


class TestPlayerSplitFunction(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()
        self.player = Player()

    def test_split_valid_pair(self):
        #simulate a pair of 8s
        self.player.hands[0].cards = [Card("Hearts", "8"), Card("Spades", "8")]
        self.assertTrue(self.player.split(self.deck, "10"))
        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(self.player.hands[0].cards[0].rank, "8")
        self.assertEqual(self.player.hands[1].cards[0].rank, "8")

    def test_split_invalid_pair(self):
        #simulate a non-pair hand
        self.player.hands[0].cards = [Card("Hearts", "8"), Card("Spades", "7")]
        self.assertFalse(self.player.split(self.deck, "10"))
        self.assertEqual(len(self.player.hands), 1)

    def test_split_already_split(self):
        #simulate already split hands
        self.player.hands = [Hand(), Hand()]
        self.player.hands[0].cards = [Card("Hearts", "8"), Card("Spades", "3")]
        self.player.hands[1].cards = [Card("Hearts", "8"), Card("Spades", "3")]
        self.assertFalse(self.player.split(self.deck, "10"))
        self.assertEqual(len(self.player.hands), 2)

    def test_split_ace_pair(self):
        #simulate a pair of Aces
        self.player.hands[0].cards = [Card("Hearts", "Ace"), Card("Spades", "Ace")]
        self.assertTrue(self.player.split(self.deck, "10"))
        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(self.player.hands[0].cards[0].rank, "Ace")
        self.assertEqual(self.player.hands[1].cards[0].rank, "Ace")

    def test_split_draw_card(self):
        #simulate a pair of 9s and ensure new cards are drawn after split
        self.player.hands[0].cards = [Card("Hearts", "9"), Card("Spades", "9")]
        initial_deck_count = len(self.deck.cards)
        self.assertTrue(self.player.split(self.deck, "10"))
        self.assertEqual(len(self.player.hands), 2)
        self.assertEqual(
            len(self.deck.cards), initial_deck_count - 2
        )  #two cards should be drawn


if __name__ == "__main__":
    unittest.main()