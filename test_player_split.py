import unittest
from blackjack_with_split import Player, Deck, Hand, Card


#!!To run: run "python -m unittest test_player_split.py" in terminal


class TestPlayerSplit(unittest.TestCase):
    def test_player_can_split(self):
        #create a player and a deck
        player = Player()
        deck = Deck()
        deck.shuffle()

        #simulate a hand where the player has two cards of the same rank
        card1 = Card("Spades", "Queen")
        card2 = Card("Diamonds", "Queen")
        player.hands[0].cards = [card1, card2]

        #attempt to split
        result = player.split(deck)

        #check if the split was successful
        self.assertTrue(result)
        self.assertEqual(len(player.hands), 2)
        self.assertNotEqual(player.hands[0].cards[1], player.hands[1].cards[1])

        #check if the hands contain the correct initial cards
        self.assertEqual(player.hands[0].cards[0], card1)
        self.assertEqual(player.hands[1].cards[0], card2)


if __name__ == "__main__":
    unittest.main()