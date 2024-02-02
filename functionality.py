# Checking basic functionality of Pasientza
from Cards import Card, Deck
import copy

# A list with the eight stacks
all_stacks = [[] for _ in range(8)]

def triplet(d:Deck) -> list:
    """Pops the first three cards from the Deck"""
    triple = [] # Save the three first cards
    for _ in range(3):
        card = d.pop()
        triple.append(card)
    return triple

deck = Deck()               # Normal deck
soros = Deck(full = False)  # Create empty deck

# Remove the first 45 cards from the deck to simplify testing
for _ in range(45): card = deck.pop()

print("Deck", deck, "\n")
print("Soros", soros, "\n")

while (not deck.isEmpty()):
    for _  in range(3):
        card = deck.pop()

        if (not isinstance(card, Card)):
            print("End of deck")
            break
        else:
            soros.push(card.rank(), card.suit())
            
    print("Deck", deck)
    print("Soros = ", soros)

    # Take user input.
    # It stops asking user for input in two cases:
    # (1): Soros gets empty
    # (2): User does not want to remove a card from soros
    while (not soros.isEmpty()):
        user_pick = int(input("#: "))

        if 0 <= user_pick < 8:
            all_stacks[user_pick].append(soros.pop())
            print("Soros = ", soros)
            print("Deck", deck)
        else: break

    if (deck.isEmpty()):
        print("Kalimera")
        deck = copy.deepcopy(soros)
        soros.empty()

print(all_stacks)