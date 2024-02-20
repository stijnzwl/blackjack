from random import randint
from colorama import init, Fore, Style
init(autoreset=True)
import sqlite3

def initialize_db(db_name='blackjack_game.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS player_balance
                      (name TEXT PRIMARY KEY, balance INTEGER)''')
    conn.commit()
    conn.close()

def update_player_balance(name, amount, db_name='blackjack_game.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Check if player exists
    cursor.execute("SELECT balance FROM player_balance WHERE name=?", (name,))
    result = cursor.fetchone()
    if result is None:
        # Add new player
        cursor.execute("INSERT INTO player_balance (name, balance) VALUES (?, ?)", (name, amount))
    else:
        # Update existing player's balance
        new_balance = result[0] + amount
        cursor.execute("UPDATE player_balance SET balance=? WHERE name=?", (new_balance, name))
    conn.commit()
    conn.close()
    
def make_bet(name, bet_amount):
    update_player_balance(name, -bet_amount)

def add_winnings(name, winnings_amount):
    update_player_balance(name, winnings_amount)
    
def get_player_balance(name, db_name='blackjack_game.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM player_balance WHERE name=?", (name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

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

def winnings_calculator(bet, player_deck, turn):
    if len(player_deck) == 2 and turn == 1:
        winnings = bet * 2.5
        print(Fore.GREEN + Style.BRIGHT + f"Your winnings: {winnings}")
    else:
        winnings = bet * 2
        print(Fore.GREEN + Style.BRIGHT + f"Your winnings: {winnings}")
    return winnings

deck_instance = DealingCards(blackjack_deck)
start = input(Fore.MAGENTA + Style.BRIGHT + "Welcome to my blackjack game, would you like to play? (yes/no) ").lower()
turn = 1
if start == "yes":
    name = str(input(Fore.WHITE + "Type your name: ")).lower()
    print(Fore.WHITE + f"Your balance: {get_player_balance(name)}")
    balance = float(input(Fore.MAGENTA + Style.BRIGHT + "Add money to balance (0 - XXX): "))
    update_player_balance(name, balance)
    print(Fore.WHITE + f"Your balance: {get_player_balance(name)}")
    bet = float(input(Fore.MAGENTA + Style.BRIGHT + "How much would you like to bet? "))
    make_bet(name, bet)
    print(Fore.MAGENTA + Style.BRIGHT + "Great! You got dealt the following cards:\n")
    player_cards, dealer_cards, modified_deck = deck_instance.first_turn()
    for card in player_cards:
        print(Fore.GREEN + Style.BRIGHT + card[0])
    print("\nThe dealer also deals himself two cards. He shows you one:\n")
    print(Fore.RED + Style.BRIGHT + dealer_cards[0][0])
    
    player_score = calculate_hand_value(player_cards)
    dealer_score = calculate_hand_value(dealer_cards)
        
    if player_score == 21 and dealer_score != 21:
        print(Fore.BLUE + Style.BRIGHT + "\nBlackjack!! congrats!")
        print(Fore.GREEN + Style.BRIGHT + f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(Fore.RED + Style.BRIGHT + f"The dealers final cards were: {dealer_cards[0][0]} and {dealer_cards[1][0]}")
        add_winnings(name, winnings_calculator(bet, player_cards, turn))
        print(f"Your balance is now: {get_player_balance(name)}")
        

    elif player_score == 21 and dealer_score == 21:
        print(Fore.CYAN + Style.BRIGHT + "\nYou have a blackjack! Unfortunately for you the dealer also has a blackjack. Tie!")
        print(Fore.GREEN + Style.BRIGHT + f"\nYour final cards were: {player_cards[0][0]} and {player_cards[1][0]}")
        print(Fore.RED + Style.BRIGHT + f"The dealers final cards were {dealer_cards[0][0]} and {dealer_cards[1][0]}")
        add_winnings(name, bet)
        print(f"Your balance is now: {get_player_balance(name)}")
    else:
        print("\nTime for your next move!\n")

else:
    print("Okay, bye!")

after_first_turn_player = PlayerDecisions(modified_deck, player_cards)
after_first_turn_dealer = PlayerDecisions(modified_deck, dealer_cards)

if player_score != 21:
    while True:
        if player_score == 21:
            break
        answer = input(Fore.MAGENTA + Style.BRIGHT + "\nWhat would you like to do next? (hit / stand / double down / split / surrender / insurance) \n")
        if answer == 'double down' and turn > 1:
            print(Fore.MAGENTA + Style.BRIGHT + "You can only double down on your first action")
        if answer == 'hit':
            turn += 1
            modified_deck, player_cards = after_first_turn_player.hit()
            print(f"\nYou got dealt a {player_cards[-1][0]}\n\nYour cards are now:")
            for card in player_cards:
                print(Fore.GREEN + Style.BRIGHT + card[0])
            player_score = calculate_hand_value(player_cards)

            if len(dealer_cards) == 2 and dealer_score == 21:
                print("\nThe dealer shows you his hole card.")
                for card in dealer_cards:
                    print(Fore.RED + Style.BRIGHT + card[0])
                print(Fore.YELLOW + Style.BRIGHT + "\nDealer has blackjack! Better luck next time.")
                break
    
            if player_score == 21 and dealer_score != 21:
                print("\nYou have 21! now it's the dealers turn: ")
                if dealer_score >= 17:
                    print("The dealer reveals his hole card:\n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    print(Fore.BLUE + Style.BRIGHT + "\nDealer stands, you win!")
                    add_winnings(name, winnings_calculator(bet, player_cards, turn))
                    print(f"Your balance is now: {get_player_balance(name)}")
                    break
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    dealer_score = calculate_hand_value(dealer_cards)
                    print(f"\nThe dealer gets a {dealer_cards[-1][0]}")
                    print("His cards are now: \n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if dealer_score == 21:
                        print(Fore.CYAN + Style.BRIGHT + "The dealer also has 21, tie! Better luck next time.")
                        add_winnings(name, bet)
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score > 21:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer busts. You win!!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score >= 17 and dealer_score < 21:
                        print(Fore.BLUE + Style.BRIGHT + "The dealer stands, you win!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                break

            elif player_score == 21 and dealer_score == 21:
                print(Fore.CYAN + Style.BRIGHT + "\nYou have 21! But the dealer also has 21, tie! :( Better luck next time!")
                break

            elif player_score > 21:
                print(Fore.YELLOW + Style.BRIGHT + "\nBust! Better luck next time.")
                break                

            elif player_score < 21 and dealer_score != 21:
                if len(dealer_cards) == 2:
                    print("\nThe dealer reveals his hole card!")
                print("\nThe dealer has the following cards: ")
                for card in dealer_cards:
                    print(Fore.RED + Style.BRIGHT + card[0])
                if dealer_score >= 17:
                    print("\nThe dealer stands")
                    if player_score > dealer_score:
                        print(Fore.BLUE + Style.BRIGHT + "You win!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now {get_player_balance(name)}")
                        break
                
                elif dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    print(f"\nThe dealer hits, and gets a {dealer_cards[-1][0]}")
                    print("He now has the following cards: \n")
                    dealer_score = calculate_hand_value(dealer_cards)
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if dealer_score == 21:
                        print(Fore.YELLOW + Style.BRIGHT + "\nDealer has 21! Better luck next time.")
                        break
                    elif dealer_score > 21:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer busts, You win!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score < 21 and dealer_score >= 17:
                        print("The dealer stands")
                        if player_score > dealer_score:
                            print(Fore.BLUE + Style.BRIGHT + "You win!")
                            add_winnings(name, winnings_calculator(bet, player_cards, turn))
                            print(f"Your balance is now: {get_player_balance(name)}")
                            break
        if answer == 'stand':
            turn += 1
            print(Fore.WHITE + Style.BRIGHT + "You chose to stand")
            if len(dealer_cards) == 2 and dealer_score == 21:
                print("\nThe dealer shows you his hole card.")
                for card in dealer_cards:
                    print(Fore.RED + Style.BRIGHT + card[0])
                print(Fore.YELLOW + Style.BRIGHT + "\nDealer has blackjack! Better luck next time.")
                break
            
            elif dealer_score != 21:
                print("\nNow it's the dealers turn: ")
                if dealer_score >= 17:
                    print("The dealer reveals his hole card:\n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if player_score > dealer_score:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer stands, you win!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif player_score == dealer_score:
                        print(Fore.CYAN + Style.BRIGHT + "Tie!")
                        add_winnings(name, bet)
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    else:
                        print(Fore.YELLOW + Style.BRIGHT + "The dealer also stands, but has a higher score, you lose!")
                        break
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    dealer_score = calculate_hand_value(dealer_cards)
                    print(f"\nThe dealer gets a {dealer_cards[-1][0]}")
                    print("His cards are now: \n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if dealer_score == 21:
                        print(Fore.YELLOW + Style.BRIGHT + "The dealer has 21! You lose.")
                        break
                    elif dealer_score > 21:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer busts. You win!!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score == player_score:
                        print(Fore.CYAN + Style.BRIGHT + "\nSame score, tie!")
                        add_winnings(name, bet)
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score >= 17 and dealer_score < 21 and player_score > dealer_score:
                        print(Fore.BLUE + Style.BRIGHT + "The dealer stands, you win!")
                        add_winnings(name, winnings_calculator(bet, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score >= 17 and dealer_score < 21 and player_score < dealer_score:
                        print(Fore.YELLOW + Style.BRIGHT + "The dealer stands, you lose!")
                        break
            break
        if answer == 'double down' and turn == 1:
            turn += 1
            make_bet(name, bet)
            modified_deck, player_cards = after_first_turn_player.hit()
            print(f"\nYou got dealt a {player_cards[-1][0]}\n\nYour cards are now:")
            for card in player_cards:
                print(Fore.GREEN + Style.BRIGHT + card[0])
            player_score = calculate_hand_value(player_cards)

            if len(dealer_cards) == 2 and dealer_score == 21:
                print("\nThe dealer shows you his hole card.")
                for card in dealer_cards:
                    print(Fore.RED + Style.BRIGHT + card[0])
                print(Fore.YELLOW + Style.BRIGHT + "\nDealer has blackjack! Better luck next time.")
                break
    
            if player_score == 21 and dealer_score != 21:
                print("\nYou have 21! now it's the dealers turn: ")
                if dealer_score >= 17:
                    print("The dealer reveals his hole card:\n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    print(Fore.BLUE + Style.BRIGHT + "\nDealer stands, you win!")
                    add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                    print(f"Your balance is now: {get_player_balance(name)}")
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    dealer_score = calculate_hand_value(dealer_cards)
                    print(f"\nThe dealer gets a {dealer_cards[-1][0]}")
                    print("His cards are now: \n")
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if dealer_score == 21:
                        print(Fore.CYAN + Style.BRIGHT + "The dealer also has 21, tie! Better luck next time.")
                        add_winnings(name, bet * 2)
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score > 21:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer busts. You win!!")
                        add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score >= 17 and dealer_score < 21:
                        print(Fore.BLUE + Style.BRIGHT + "The dealer stands, you win!")
                        add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                break

            elif player_score == 21 and dealer_score == 21:
                print(Fore.CYAN + Style.BRIGHT + "\nYou have 21! But the dealer also has 21, tie! :( Better luck next time!")
                add_winnings(name, bet * 2)
                print(f"Your balance is now: {get_player_balance(name)}")
                break

            elif player_score > 21:
                print(Fore.YELLOW + Style.BRIGHT + "\nBust! Better luck next time.")
                break                

            elif player_score < 21 and dealer_score != 21:
                if len(dealer_cards) == 2:
                    print("\nThe dealer reveals his hole card!")
                print("\nThe dealer has the following cards: ")
                for card in dealer_cards:
                    print(Fore.RED + Style.BRIGHT + card[0])
                if dealer_score >= 17:
                    print("\nThe dealer stands")
                    if player_score > dealer_score:
                        print(Fore.BLUE + Style.BRIGHT + "You win!")
                        add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif player_score < dealer_score:
                        print(Fore.YELLOW + Style.BRIGHT + "You lose!")
                        break
                    elif player_score == dealer_score:
                        print(Fore.CYAN + Style.BRIGHT + "Tie!")
                        add_winnings(name, bet * 2)
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                while dealer_score < 17:
                    modified_deck, dealer_cards = after_first_turn_dealer.hit()
                    print(f"\nThe dealer hits, and gets a {dealer_cards[-1][0]}")
                    print("He now has the following cards: \n")
                    dealer_score = calculate_hand_value(dealer_cards)
                    for card in dealer_cards:
                        print(Fore.RED + Style.BRIGHT + card[0])
                    if dealer_score == 21:
                        print(Fore.YELLOW + Style.BRIGHT + "\nDealer has 21! Better luck next time.")
                        break
                    elif dealer_score > 21:
                        print(Fore.BLUE + Style.BRIGHT + "\nDealer busts, You win!")
                        add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                        print(f"Your balance is now: {get_player_balance(name)}")
                        break
                    elif dealer_score < 21 and dealer_score >= 17:
                        print("The dealer stands")
                        if player_score > dealer_score:
                            print(Fore.BLUE + Style.BRIGHT + "You win!")
                            add_winnings(name, winnings_calculator(bet * 2, player_cards, turn))
                            print(f"Your balance is now: {get_player_balance(name)}")
                            break
                        elif player_score < dealer_score:
                            print(Fore.YELLOW + Style.BRIGHT + "You lose!")
                            break
                        elif player_score == dealer_score:
                            print(Fore.CYAN + Style.BRIGHT + "Tie!")
                            add_winnings(name, bet * 2)
                            print(f"Your balance is now: {get_player_balance(name)}")
                            break
                break
        