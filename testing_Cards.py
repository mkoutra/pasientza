import Cards
import copy

import random

a = [1,2,3]

a.reverse()

print(a)
random.seed(100)

deck1 = Cards.Deck()
print(deck1)

deck1.inverse()

print("Inversed Deck:\n", deck1)

# c1 = Cards.Card('10', 'c')
# c2 = Cards.Card('9', 'd')

# if (c1 == c2): print("c1 == c2")
# else: print("c1 != c2")

# print("-"*10,"\n", c1, c2)

# c1 = c2 # Assignment
# c1.set_rank('A')
# print("After assignment", c1, c2) # (A♦) (A♦)

# c1 = Cards.Card('10', 'c')
# c2 = Cards.Card('9', 'd')

# print("-"*10,"\n", c1, c2)

# c1 = copy.copy(c2)
# c1.set_rank('A')
# print("After c1 = copy.copy(c2)", c1, c2)

# deck1 = Cards.Deck()
# deck2 = Cards.Deck(full = False)
# deck2.push('8', 'c')

# print("Deck 1: ", deck1)
# print("Deck 2: ", deck2)

# deck1 = copy.deepcopy(deck2)

# deck2.push('A', 's')
# deck2.push('K', 's')

# deck1.push('3', 's')

# print("Deck 1: ", deck1)
# print("Deck 2: ", deck2)
