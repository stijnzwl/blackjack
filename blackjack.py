from random import randint

blackjack_deck = [
    ("2 of Hearts", 2), ("3 of Hearts", 3), ("4 of Hearts", 4), ("5 of Hearts", 5),
    ("6 of Hearts", 6), ("7 of Hearts", 7), ("8 of Hearts", 8), ("9 of Hearts", 9), ("10 of Hearts", 10),
    ("Jack of Hearts", 10), ("Queen of Hearts", 10), ("King of Hearts", 10), ("Ace of Hearts", 11),

    ("2 of Diamonds", 2), ("3 of Diamonds", 3), ("4 of Diamonds", 4), ("5 of Diamonds", 5),
    ("6 of Diamonds", 6), ("7 of Diamonds", 7), ("8 of Diamonds", 8), ("9 of Diamonds", 9), ("10 of Diamonds", 10),
    ("Jack of Diamonds", 10), ("Queen of Diamonds", 10), ("King of Diamonds", 10), ("Ace of Diamonds", 11),

    ("2 of Clubs", 2), ("3 of Clubs", 3), ("4 of Clubs", 4), ("5 of Clubs", 5),
    ("6 of Clubs", 6), ("7 of Clubs", 7), ("8 of Clubs", 8), ("9 of Clubs", 9), ("10 of Clubs", 10),
    ("Jack of Clubs", 10), ("Queen of Clubs", 10), ("King of Clubs", 10), ("Ace of Clubs", 11),

    ("2 of Spades", 2), ("3 of Spades", 3), ("4 of Spades", 4), ("5 of Spades", 5),
    ("6 of Spades", 6), ("7 of Spades", 7), ("8 of Spades", 8), ("9 of Spades", 9), ("10 of Spades", 10),
    ("Jack of Spades", 10), ("Queen of Spades", 10), ("King of Spades", 10), ("Ace of Spades", 11),
]




class DealingCards:
    def __init__(self, deck):
        self.deck = deck
    def first_turn(self):
        player_cards = []
        dealer_cards = []
        while True:
            player_cards.append(self.deck.pop(randint(0, len(self.deck) - 1)))
            dealer_cards.append(self.deck.pop(randint(0, len(self.deck) - 1)))
            if len(player_cards) == 2 and len(dealer_cards) == 2:
                break
        return player_cards, dealer_cards

class PlayerDecisions:
    def __init__(self, deck):
        self.deck = deck

    def hit(self):
        pass


deck_instance = DealingCards(blackjack_deck)
start = "yes"   # input("Welcome to my blackjack game, would you like to play? (yes/no) ")
if start == "yes":
    print("Great! You got dealt the following cards:\n")
    player_cards, dealer_cards = deck_instance.first_turn()
    for card in player_cards:
        print(card[0])
    print("\nThe dealer also deals himself two cards. He shows you one:\n")
    print(dealer_cards[0][0])

    player_score = 0
    dealer_score = 0
    for card in player_cards:
        player_score += card[1]
    for card in dealer_cards:
        dealer_score += card[1]
        
    if player_score == 21 and dealer_score != 21:
        print("\nCongrats!! you already won you lucky fuck")
        print(f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(f"The dealers cards were: {dealer_cards[0][0]} and {dealer_cards[1][0]}")
    elif player_score == 21 and dealer_score == 21:
        print("\nYou have a blackjack! Unfortunately for you the dealer also has a blackjack. Tie!")
        print(f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(f"The dealers cards were {dealer_cards[0][0]} and {dealer_cards[1][0]}")
    else:
        print("\nTime for your next move!")

else:
    print("So fuck off cunt")