import random

#Card Class: define card ranks and suits
class Card:
    #represents a single card, defined by its suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    #returns a readable string representation of the card
    def __repr__(self):
        return f'{self.rank} of {self.suit}'
    
    #returns the rank of the card
    def return_rank(self):
        return self.rank


#Deck Class: set up the deck, shuffle it, and handle card draws
class Deck:
    #initialises the deck by creating a full set of 52 cards and then shuffling them
    def __init__(self, num_decks=1):
        self.cards = []
        for _ in range(num_decks):
            for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
                for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']:
                    self.cards.append(Card(suit, rank))
        self.shuffle()

    #shuffles the deck to randomise the order of the cards
    def shuffle(self):
        random.shuffle(self.cards)

    #draws the top card from the deck and returns it
    def draw_card(self):
        if not self.cards:
            #reinitialises the deck and shuffles again if out of cards
            self.__init__()  
            print("Deck was empty, reshuffled.")
        return self.cards.pop()

    #returns a string representation showing the number of cards left in the deck
    def __repr__(self):
        return f'Deck of {len(self.cards)} cards'
    
    
#Player Class: Blackjack player
class Player:
    
    #defines the player with an empty hand, score and bust status
    def __init__(self):
        self.hand = []
        self.total_score = 0
        self.bust = False

    #draws a card from the deck, adds it to the player's hand, and updates the score
    def draw_card(self, deck):
        card = deck.draw_card()
        self.hand.append(card)
        self.calculate_score()
        return card

    #calculates the score of the player's hand and adjusting the Aces as needed (1 or 11)
    def calculate_score(self):
        aces = 0
        self.total_score = 0
        
        for card in self.hand:
            if card.rank == 'Ace':
                aces += 1
                #ace is worth 11
                self.total_score += 11  
            elif card.rank in ['Jack', 'Queen', 'King']:
                #face cards are worth 10
                self.total_score += 10  
            else:
                #numeric cards are worth their number
                self.total_score += int(card.rank)          
        #adjust score if it's over 21 while there are Aces in hand
        while self.total_score > 21 and aces:
            #ace is worth 1 instead of 11
            self.total_score -= 10
            aces -= 1      
        self.bust = self.total_score > 21

    #returns a string representation of the player's hand
    def display_hand(self):
        return ', '.join(str(card) for card in self.hand)


    #resets the player's hand and score for a new round
    def reset_hand(self):
        self.hand.clear()
        self.total_score = 0
        self.bust = False


#Dealer Class: Blackjack dealer
class Dealer(Player):
    
    #returns the dealer's visible card
    def show_uphand(self):
        return self.hand[0] if self.hand else None

    #dealer draws cards until the score is at least 17
    def take_turn(self, deck):
        while self.total_score < 17:
            self.draw_card(deck)
        return self.hand
    

class Game:
    #initialize the game with a new deck, player and dealer
    def __init__(self, strategy, num_decks=1):
        self.deck = Deck(num_decks)
        self.player = Player()
        self.dealer = Dealer()
        self.strategy = strategy

    #deal two cards each to the player and the dealer
    def deal_cards(self):
        self.player.draw_card(self.deck)
        self.player.draw_card(self.deck)
        self.dealer.draw_card(self.deck)
        self.dealer.draw_card(self.deck)

    #display the player's hand and the dealer's initial card
    def show_hands(self):
        print(f"Player's hand: {self.player.display_hand()} - Score: {self.player.total_score}")
        print(f"Dealer's initial card: {self.dealer.show_initial_card()}")


    #player actions
    def player_turn(self):
        while not self.player.bust:
            print(f"Player's hand: {self.player.display_hand()} - Score: {self.player.total_score}")
            
            #display the dealer's visible card to use in the strategy function
            dealer_card = self.dealer.show_initial_card()
            print(f"Dealer's visible card: {dealer_card}")
            
            #option for decision based on whether a strategy is provided
            if self.strategy:
                action = self.strategy(self.dealer.total_score,self.player.total_score)
                print(f"Strategy recommends to '{action}'.")
            else:
                action = str(input("Choose action: Hit (h) or Stand (s): "))
                action=action.lower()

            #execute the chosen action
            if action == 'hit':
                self.player.draw_card(self.deck)
                if self.player.bust:
                    print("Player busts!")
                    break
            elif action == 'stand':
                print("Player stands.")
                break
            else:
                print("Invalid action. Please enter 'h' to hit or 's' to stand.")


    #dealer draws cards until their score is 17 or higher
    def dealer_turn(self):
        while self.dealer.total_score < 17:
            self.dealer.draw_card(self.deck)
        print(f"Dealer's hand: {self.dealer.display_hand()} - Score: {self.dealer.total_score}")
        if self.dealer.bust:
            print("Dealer busts!")
            Dealer.dealer_busted(self.dealer)



    #determine the winner based on the final scores
    def determine_winner(self):
        if self.player.bust:
            return "Dealer wins!"
        elif self.dealer.bust:
            return "Player wins!"
        elif self.player.total_score > self.dealer.total_score:
            return "Player wins!"
        elif self.player.total_score < self.dealer.total_score:
            return "Dealer wins!"
        else:
            return "It's a tie!"
        

    #play a round of the game
    def play_round(self):
        #refresh the deck each round
        self.deck = Deck()  
        self.player.reset_hand()
        self.dealer.reset_hand()
        self.deal_cards()
        self.show_hands()
        self.player_turn()
        if not self.player.bust:
            self.dealer_turn()
        print(self.determine_winner())
        if self.determine_winner() == "Player wins!":
            return "wins"
        elif self.determine_winner() == "Dealer wins!":
            return "losses"
        else:
            return "ties" 
        


#run a simulation of the game with a given strategy, number of trials and number of decks
def run_simulation(strategy, num_trials=10000, num_decks=1):
    #dictionary to keep track of wins, losses, ties and scores
    results = {'wins': 0, 'losses': 0, 'ties': 0, 'player_scores': [], 'dealer_scores': []}
    for _ in range(num_trials):
        #create a new game instance with the specified strategy and number of decks
        game = Game(strategy, num_decks)
        print(f"--------------Running simulation with {num_decks} decks.--------------")
        #store the result of the round
        result = game.play_round()
        results[result] += 1
        #add player's and dealer's total scores to the results dictionary
        results['player_scores'].append(game.player.total_score)
        results['dealer_scores'].append(game.dealer.total_score)
    return results