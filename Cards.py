# Classes related to the card and deck
# Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
# Suits: c-clubs (♣), d-diamonds (♦), h-hearts (♥) and s-spades (♠)

class CardColor:
    """Card Color"""

    def __init__(self, c):
        if (c.lower() == 'r' or c.lower() == "red"):   self._color = 0
        elif (c.lower() == 'b' or c.lower() == "black"): self._color = 1
        else: raise Exception("Invalid CardColor.")
    
    def __eq__(self, other):
        if isinstance(other, CardColor):
            return self._color == other._color
        else: raise Exception("Invalid comparison.")
    
    def __str__(self):
        if (self._color == 0): return "Red"
        elif (self._color == 1): return "Black"
        else: raise Exception("Invalid color")
    

class Card:
    """Card representation"""
    _suitToSymbol = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    _possible_ranks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

    def __init__(self, rank:str, suit:str):
        self.set_rank(rank)
        self.set_suit(suit)
        self.set_value()
        self.set_color()
        self.set_symbol()

    # -------------- Setters -------------- 
    def set_rank(self, rank:str):
        if rank.upper() in Card._possible_ranks:
            self._rank = rank
        else:
            raise Exception("Invalid card rank.")

    def set_suit(self, suit:str):
        if suit.lower() in Card._suitToSymbol.keys():
            self._suit = suit
        else: raise Exception("Invalid suit.")

    def set_value(self):
        if self._rank in "JQK":
            self._value = 10
        elif (self._rank == 'A'):
            self._value = 1
        elif (self._rank in Card._possible_ranks[:9]):
            self._value = int(self._rank)
        else:
            raise Exception("Invalid value.")

    def set_color(self):
        if (self._suit in ['c', 's']):
            self._color = CardColor('black')
        elif (self._suit in ['h', 'd']):
            self._color = CardColor('red')

    def set_symbol(self):
        if (self._suit in Card._suitToSymbol.keys()):
            self._symbol = Card._suitToSymbol[self._suit]
        else: raise Exception("Invalid symbol.")

    # -------------- Getters --------------
    def rank(self)->str: return self._rank
    def suit(self)->str: return self._suit
    def color(self)->CardColor: return self._color
    def value(self)->int: return self._value
    def symbol(self)->str: return self._symbol

    def __str__(self) -> str:
        return '|' + self.rank() + "" + self.symbol() + '|'

    def __eq__(self, other):
        if isinstance(other, Card):
            return (self.rank() == other.rank() and self.suit() == self.suit())
        else: raise Exception("Invalid Card comparison.")

if __name__ == "__main__":
    c1 = Card('A', 'h')
    c2 = Card('3', 'd')

    print(c1, c2)

    print("Same cards") if (c1 == c2) else print("Not same cards")
    print(c1.color(), c1.rank(), c1.suit(), c1.value(), c1.symbol())

    if (c1.color() == c2.color()): print("Same color\n")
    else: print("Not same color")