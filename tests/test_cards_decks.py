#----------------------------------
#Michail E. Koutrakis
#Github: https://github.com/mkoutra

from lib.Decks import Deck, SuitDeck
from lib.Card import Card

if __name__ == "__main__":
    d1 = Deck()
    print(d1)
    print(d1.number_of_cards())
    c1 = d1.pop()
    print(c1)
    print(d1)
    d1.shuffle()
    print("\n\n",d1, d1.number_of_cards())
    print(d1.contains(Card('3', 's')))

    sd1 = SuitDeck()

    sd1.push(Card('A', 'd'))
    sd1.push(Card('2', 'd'))
    sd1.push(Card('3', 'd'))
    print(sd1, sd1.number_of_cards())
