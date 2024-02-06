# Classes related to the card and deck
# Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
# Suits: c-clubs (♣), d-diamonds (♦), h-hearts (♥) and s-spades (♠)

import random
import copy         

class CardColor:
    """Card Color"""

    def __init__(self, c:str):
        self.c = c.lower()
        if (self.c == 'r' or self.c == "red"):   self._color = 0
        elif (self.c == 'b' or self.c == "black"): self._color = 1
        else: raise Exception("Invalid CardColor.")
    
    def __eq__(self, other):
        if isinstance(other, CardColor):
            return self._color == other._color
        else: raise TypeError("Invalid comparison.")
    
    def __str__(self):
        if (self._color == 0): return "Red"
        elif (self._color == 1): return "Black"
        else: raise Exception("Invalid color")
    
    def __copy__(self):
        return CardColor(self.c) 
    

class Card:
    """Card representation"""
    _suitToSymbol = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    _allRanks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

    def __init__(self, rank:str, suit:str):
        self.set_rank(rank)
        self.set_suit(suit)
        self.set_value()
        self.set_color()
        self.set_symbol()

    # -------------- Setters -------------- 
    def set_rank(self, rank:str):
        if rank.upper() in Card._allRanks:
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
        elif (self._rank in Card._allRanks[:9]):
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

    def id(self)->str: return f"{self._rank}{self._suit}"

    def __str__(self) -> str:
        return '(' + self.rank() + "" + self.symbol() + ')'

    def __repr__(self) -> str:
        return self.id()

    def __eq__(self, other):
        if isinstance(other, Card):
            return ((self.rank() == other.rank()) and (self.suit() == other.suit()))
        else: raise Exception("Invalid Card comparison.")
    
    def __copy__(self):
        return Card(self.rank(), self.suit())


class Deck:
    """ A regular card deck of 52 cards """
    
    def __init__(self, full = True):
        """full: optional, True if deck contains 52 cards"""
        self._deckCards:list = []       # Cards on the deck
        self._removedCards:list = []    # Cards no longer on the deck
        self._nCards = 0                # Number of cards on the deck
        
        if (full):
            self.fill()                 # Fill deck with the 52 cards
            self.shuffle()              # Shuffle deck
        
    def contains(self, rank, suit) -> bool:
        """
        Returns true if card with rank rank and suit suit is inside the deck
        """
        for card in self._deckCards:
            if (card.rank() == rank and card.suit() == suit):
                return True
        return False
    
    def push(self, rank:str, suit:str) -> None:
        """ Place a card at the top of the deck. """
        
        if (self._nCards < 52 and self.contains(rank, suit) == False):
            self._deckCards.append(Card(rank,  suit))
            self._nCards += 1
        else:
            raise Exception(f"Card {rank, suit} already inside deck.")

    def pop(self) -> Card:
        """ Removes and returns a card from the top of the deck. """
        if self._deckCards: # Checks if deck has cards
            popped_card = self._deckCards.pop()
            self._removedCards.append(popped_card)
            self._nCards -= 1
            return popped_card

        return None

    def shuffle(self):
        """ Shuffle the deck cards. """
        if (self._nCards > 0):
            random.shuffle(self._deckCards)

    def fill(self):
        """Fill a deck with 52 cards"""
        for suit in Card._suitToSymbol.keys():
            for rank in Card._allRanks:
                self.push(rank, suit)

    def empty(self):
        """Remove all cards from deck"""
        self._deckCards = []
        self._removedCards = []
        self._nCards = 0

    def restore(self):
        """Bring deck back to its original condition with 52 cards."""
        if (len(self._deckCards) + len(self._removedCards) != 52):
            raise Exception("Can't go back to original deck.")
        else:
            self._nCards = len(self._deckCards) + len(self._removedCards)
            self._deckCards += self._removedCards[::-1]
            self._removedCards.clear()

    def isEmpty(self)->bool:
        """Checks if the deck is empty."""
        if (self._nCards == 0): return True
        return False

    def nCards(self):
        """Returns the number of cards inside the deck."""
        return self._nCards

    def __str__(self):
        s = ""
        for i in range(len(self._deckCards)):
            if ((i != 0) and (i % 13 == 0)): s += '\n'
            s += str(self._deckCards[i]) + " "
        return s

    def __getitem__(self, x:int) -> Card:
        if isinstance(x, slice) or (x >= 0 and x < self._nCards):
            return self._deckCards[x]
    
    def __copy__(self):
        copy_instance = Deck(full = False)
        copy_instance._deckCards = self._deckCards.copy()
        copy_instance._removedCards = self._removedCards.copy()
        copy_instance._nCards = self._nCards
        return copy_instance
    
    def __deepcopy__(self, memo):
        copy_instance = Deck(full = False)
        copy_instance._deckCards = copy.deepcopy(self._deckCards)
        copy_instance._removedCards = copy.deepcopy(self._removedCards)
        copy_instance._nCards = self._nCards
        return copy_instance


if __name__ == "__main__":
    print(10*'-', "Testing", 10*'-')
    c1 = Card('A', 'h')
    c2 = Card('3', 'd')

    print(c1, c2)
    print("Id = ", c2.id())
    print("Same cards") if (c1 == c2) else print("Not same cards")
    print(c1.color(), c1.rank(), c1.suit(), c1.value(), c1.symbol())

    if (c1.color() == c2.color()): print("Same color\n")
    else: print("Not same color")

    print("Initial Deck")
    deck1 = Deck()
    print(deck1)

    print("\nPop the first 51 cards")
    for _ in range(51): deck1.pop()

    print(deck1)

    print("\nPop the last card")
    deck1.pop()

    print(deck1)
    
    if (deck1.isEmpty()): print("Empty", deck1.nCards())
    else: print("Non empty")
    
    #deck1.push("4", 's')

    print("\nRestore")
    deck1.restore()
    print(deck1)

    print("Number of cards", deck1.nCards())
