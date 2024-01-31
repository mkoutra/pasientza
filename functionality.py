# Checking basic functionality of Pasientza
from Cards import Card, Deck

# A list with the eight stacks
all_stacks = [[] for _ in range(8)]

def triplet(d:Deck) -> list:
    """Pops the first three cards from the Deck"""
    triple = [] # Save the three first cards
    for _ in range(3):
        card = d.pop()
        triple.append(card)
    return triple

deck = Deck()
# TODO soros must be of Deck Type with no cards
# __eq__() method probably

soros:list = []

# Remove the first 45 cards from the deck
for _ in range(45): deck.pop()

print(deck,"\n")

while (not deck.isEmpty()):
    for _  in range(3):
        card = deck.pop()
        if (not isinstance(card, Card)):
            print("End of deck")
            break
        else:
            soros.append(card)
            
    print("Soros = ", soros)
    
    # Take user input
    while (True):
        user_pick = int(input("#: "))
        if (user_pick >= 0 and user_pick < 8):
            all_stacks[user_pick].append(soros.pop())
            print("Soros = ", soros)
        else: break

print(all_stacks)