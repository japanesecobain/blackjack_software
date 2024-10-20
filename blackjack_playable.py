'''Welcome to Aoi Araki's Black Jack Software'''

import random

def generate_deck():
    '''Generates a standard deck of playing cards ordered by rank'''
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    suits = ["♣", "♦", "♥", "♠"]
    deck = []
    for rank in ranks:
        for suit in suits:
            deck.append(f"{rank}{suit}")
    return deck

def card_value(card):
    rank = card[0]
    if rank in ['J', 'Q', 'K', 'T']:
        return 10
    elif rank == 'A':
        return 11  # Begins by calculating A as 11
    else:
        return int(rank)

def hand_value(hand):
    value = 0
    num_aces = 0
    for card in hand:
        card_val = card_value(card)
        value += card_val
        if card[0] == 'A':
            num_aces += 1
    # Adjust for aces
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1
    return value

def main():
    print('Welcome to a game of Blackjack!')
    print("GOOD LUCK! (don't bet too much)")
    balance = -1
    while balance < 0:
        balance_input = input("Enter your starting balance: ")
        try:
            balance = float(balance_input)
            if balance < 0:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    deck = generate_deck()
    random.shuffle(deck)

    keep_playing = True
    while keep_playing and balance > 0:
        # Get bet amount
        bet = -1
        while bet <= 0 or bet > balance:
            bet_input = input(
                f"Your balance is ${balance:.2f}. How much would you like to bet? "
            )
            try:
                bet = float(bet_input)
                if bet <= 0:
                    print("You must enter a positive value.")
                elif bet > balance:
                    print("You cannot bet more than your current balance.")
            except ValueError:
                print("Invalid input. Please enter a positive number.")

        # Reshuffle the deck if necessary
        if len(deck) < 10:
            print("Reshuffling the deck...")
            deck = generate_deck()
            random.shuffle(deck)

        # Deal initial hands
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]  # Dealer gets two cards

        # Show hands
        print(f"Dealer's Hand: [{dealer_hand[0]}, ?]")
        print(f"Player's Hand: {player_hand} (Value: {hand_value(player_hand)})")

        # Player's turn
        while True:
            if hand_value(player_hand) == 21:
                print("Blackjack! You have 21.")
                break
            elif hand_value(player_hand) > 21:
                print("You have busted!")
                break
            else:
                action = input("Do you wish to 'hit' or 'stand'? ").lower()
                if action == 'hit':
                    player_hand.append(deck.pop())
                    print(
                        f"Player's Hand: {player_hand} "
                        f"(Value: {hand_value(player_hand)})"
                    )
                elif action == 'stand':
                    break
                else:
                    print("Invalid input. Please enter 'hit' or 'stand'.")

        player_total = hand_value(player_hand)

        # Dealer's turn
        if player_total <= 21:
            print(f"Dealer's Hand: {dealer_hand} (Value: {hand_value(dealer_hand)})")
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
                print(
                    f"Dealer hits: {dealer_hand} "
                    f"(Value: {hand_value(dealer_hand)})"
                )
            dealer_total = hand_value(dealer_hand)
            # Determine the outcome
            if dealer_total > 21:
                print("Dealer busts! You win.")
                balance += bet
            elif dealer_total > player_total:
                print("Dealer wins.")
                balance -= bet
            elif dealer_total < player_total:
                print("You win!")
                balance += bet
            else:
                print("It's a tie!")
        else:
            balance -= bet

        print(f"Your balance is now ${balance:.2f}")

        if balance <= 0:
            print("You have run out of money!")
            break

        play_again = input("Do you wish to play again? (yes/no): ").lower()
        if play_again != 'yes':
            keep_playing = False

    print(f"Thank you for playing! Your final balance is ${balance:.2f}")

main()


