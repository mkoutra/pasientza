# Checking basic functionality of Pasientza game
from lib.Card import Card
from lib.Decks import Deck, SuitDeck
import copy

N_SUIT_DECKS = 8

suit_decks = [SuitDeck() for _ in range(N_SUIT_DECKS)]

def print_suit_decks_top():
    print('-' * 50)
    for i in range(N_SUIT_DECKS):
        print(i,suit_decks[i].top(), end =" ")

deck = Deck()               # Normal deck
soros = Deck(full = False)  # Create empty deck

# Remove the first 45 cards from the deck to simplify testing
# for _ in range(45): card = deck.pop()

print("Deck", deck, "\n")
print("Soros", soros, "\n")

while not deck.is_empty():
    for _  in range(3):
        card = deck.pop()

        if not isinstance(card, Card):
            print("End of deck")
            break
        soros.push(card)
            
    # print("Deck", deck)
    print("Soros = ", soros)
    print_suit_decks_top()

    # Take user input.
    # It stops asking user for input in two cases:
    # (1): Soros gets empty
    # (2): User does not want to remove a card from soros
    while (not soros.is_empty()):
        user_pick = int(input("\nSuitDeck # to insert top of deck: "))

        if 0 <= user_pick < 8:
            try:
                # Card moving from soros to a suitDeck
                moving_card = soros.pop()
                suit_decks[user_pick].push(moving_card)
                print("Soros = ", soros)
                print_suit_decks_top()
            except:
                # Move card back to soros
                print("Error occurred")
                soros.push(moving_card)
                print("Soros = ", soros)
                print_suit_decks_top()
        else: # User's pick was invalid
            break

    if deck.is_empty():
        print("Deck got empty, start again")
        soros.inverse()
        deck = copy.deepcopy(soros)
        soros.make_empty()       # Remove all cards from soros

print("SuitDecks:\n", suit_decks)