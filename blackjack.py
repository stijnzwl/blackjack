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

aces = ["Ace of Hearts", "Ace of Diamonds", "Ace of Clubs", "Ace of Spades"]
balance = 50


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
        return player_cards, dealer_cards, self.deck

class PlayerDecisions:
    def __init__(self, deck, person_deck):
        self.deck = deck
        self.person_deck = person_deck

    def hit(self):
        self.person_deck.append(self.deck.pop(randint(0, len(self.deck) - 1)))
        return self.deck, self.person_deck
        
def calculate_hand_value(hand):
    total = 0
    ace_count = 0
    for card in hand:
        value, is_ace = card[1], card[0] in aces
        total += value
        if is_ace:
            ace_count += 1
    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1
    return total

def winnings_calculator(bet, player_deck, balance):
    if len(player_deck) == 2:
        winnings = bet * 2.5
        balance += winnings
        print(f"Your winnings: {winnings}")
        print(f"Your balance: {balance}")
    else:
        winnings = bet * 2
        balance += winnings
        print(f"Your winnings: {winnings}")
        print(f"Your balance: {balance}")
    return balance

deck_instance = DealingCards(blackjack_deck)
start = input("Welcome to my blackjack game, would you like to play? (yes/no) ")
if start == "yes":
    bet = float(input("How much would you like to bet? "))
    balance -= bet
    print("Great! You got dealt the following cards:\n")
    player_cards, dealer_cards, modified_deck = deck_instance.first_turn()
    for card in player_cards:
        print(card[0])
    print("\nThe dealer also deals himself two cards. He shows you one:\n")
    print(dealer_cards[0][0])
    
    player_score = calculate_hand_value(player_cards)
    dealer_score = calculate_hand_value(dealer_cards)
        
    if player_score == 21 and dealer_score != 21:
        print("\nBlackjack!! congrats!")
        print(f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(f"The dealers final cards were: {dealer_cards[0][0]} and {dealer_cards[1][0]}")
        winnings_calculator(bet, player_cards, balance)
        

    elif player_score == 21 and dealer_score == 21:
        print("\nYou have a blackjack! Unfortunately for you the dealer also has a blackjack. Tie!")
        print(f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(f"The dealers final cards were {dealer_cards[0][0]} and {dealer_cards[1][0]}")
        balance += bet
    else:
        print("\nTime for your next move!\n")

else:
    print("So fuck off cunt")

after_first_turn_player = PlayerDecisions(modified_deck, player_cards)
after_first_turn_dealer = PlayerDecisions(modified_deck, dealer_cards)

if player_score != 21:
    while True:
        if player_score == 21:
            break
        answer = input("\nWhat would you like to do next? (hit / stand / double down / split / surrender / insurance) \n")
        if answer == 'hit':
            modified_deck, player_cards = after_first_turn_player.hit()
            print(f"\nYou got dealt a {player_cards[-1][0]}\n\nYour cards are now:")
            for card in player_cards:
                print(card[0])
            player_score = calculate_hand_value(player_cards)

            if len(dealer_cards) == 2 and dealer_score == 21:
                print("\nThe dealer shows you his hole card.")
                for card in dealer_cards:
                    print(card[0])
                print("\nDealer has blackjack! Better luck next time.")
                break
            
            if player_score == 21 and dealer_score != 21:
                print("\nYou have 21! now it's the dealers turn: ")
                if dealer_score >= 17:
                    print("The dealer reveals his hole card:\n")
                    for card in dealer_cards:
                        print(card[0])
                    print("\nDealer stands, you win!")
                    winnings_calculator(bet, player_cards, balance)
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    dealer_score = calculate_hand_value(dealer_cards)
                    print(f"\nThe dealer gets a {dealer_cards[-1][0]}")
                    print("His cards are now: \n")
                    for card in dealer_cards:
                        print(card[0])
                    if dealer_score == 21:
                        print("The dealer also has 21, tie! Better luck next time.")
                        balance += bet
                        break
                    elif dealer_score > 21:
                        print("\nDealer busts. You win!!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                    elif dealer_score >= 17 and dealer_score < 21:
                        print("The dealer stands, you win!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                break

            elif player_score == 21 and dealer_score == 21:
                print("\nYou have 21! But the dealer also has 21, tie! :( Better luck next time!")
                balance += bet
                break

            elif player_score > 21:
                print("\nBust! Better luck next time.")
                break                

            elif player_score < 21 and dealer_score != 21:
                if len(dealer_cards) == 2:
                    print("\nThe dealer reveals his hole card!")
                print("\nThe dealer has the following cards: ")
                for card in dealer_cards:
                    print(card[0])
                if dealer_score >= 17:
                    print("\nThe dealer stands")
                    if player_score > dealer_score:
                        print("You win!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                
                elif dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    print(f"\nThe dealer hits, and gets a {dealer_cards[-1][0]}")
                    print("He now has the following cards: \n")
                    dealer_score = calculate_hand_value(dealer_cards)
                    for card in dealer_cards:
                        print(card[0])
                    if dealer_score == 21:
                        print("\nDealer has 21! Better luck next time.")
                        break
                    elif dealer_score > 21:
                        print("\nDealer busts, You win!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                    elif dealer_score < 21 and dealer_score >= 17:
                        print("The dealer stands")
                        if player_score > dealer_score:
                            print("You win!")
                            winnings_calculator(bet, player_cards, balance)
                            break
        if answer == 'stand':
            print("You chose to stand")
            if len(dealer_cards) == 2 and dealer_score == 21:
                print("\nThe dealer shows you his hole card.")
                for card in dealer_cards:
                    print(card[0])
                print("\nDealer has blackjack! Better luck next time.")
                break
            
            elif dealer_score != 21:
                print("\nNow it's the dealers turn: ")
                if dealer_score >= 17:
                    print("The dealer reveals his hole card:\n")
                    for card in dealer_cards:
                        print(card[0])
                    if player_score > dealer_score:
                        print("\nDealer stands, you win!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                    elif player_score == dealer_score:
                        print("Tie!")
                        balance += bet
                        break
                    else:
                        print("The dealer also stands, but has a higher score, you lose!")
                        break
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    dealer_score = calculate_hand_value(dealer_cards)
                    print(f"\nThe dealer gets a {dealer_cards[-1][0]}")
                    print("His cards are now: \n")
                    for card in dealer_cards:
                        print(card[0])
                    if dealer_score == 21:
                        print("The dealer has 21! You lose.")
                        break
                    elif dealer_score > 21:
                        print("\nDealer busts. You win!!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                    elif dealer_score == player_score:
                        print("\nSame score, tie!")
                        balance += bet
                        break
                    elif dealer_score >= 17 and dealer_score < 21 and player_score > dealer_score:
                        print("The dealer stands, you win!")
                        winnings_calculator(bet, player_cards, balance)
                        break
                    elif dealer_score >= 17 and dealer_score < 21 and player_score < dealer_score:
                        print("The dealer stands, you lose!")
        
    

