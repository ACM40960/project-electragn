import random

#Define the Card and Deck Classes


#Card Class: Define card ranks and suits
class Card:
    """ Represents a single card, defined by its rank and suit. """
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        """ Returns a human-readable string representation of the card. """
        return f'{self.rank} of {self.suit}'


#Deck Class: Set up the deck, shuffle it, and handle card draws
class Deck:
    """ Represents a deck of cards to be used in a game of Blackjack. """
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        """ Initialise the deck by creating a full set of 52 cards and then shuffling them. """
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def shuffle(self):
        """ Shuffles the cards in the deck to randomise their order. """
        random.shuffle(self.cards)

    def draw_card(self):
        """ Draws the top card from the deck and returns it. """
        if not self.cards:
            #reinitialize the deck and shuffle again if out of cards
            self.__init__()  
            print("The deck was empty. Reshuffled.")
        return self.cards.pop()

    def __repr__(self):
        """ Returns a string representation showing the number of cards left in the deck. """
        return f'Deck of {len(self.cards)} cards'
    
    