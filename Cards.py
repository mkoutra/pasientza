# Classes related to playing cards and deck.
# Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
# Suits: c-clubs (♣), d-diamonds (♦), h-hearts (♥) and s-spades (♠)

import random
import copy
from typing import List

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
        self._set_rank(rank)
        self._set_suit(suit)
        self._set_value()
        self._set_color()
        self._set_symbol()

    # -------------- Setters -------------- 
    def _set_rank(self, rank:str):
        if rank.upper() in Card._allRanks:
            self._rank = rank
        else:
            raise Exception("Invalid card rank.")

    def _set_suit(self, suit:str):
        if suit.lower() in Card._suitToSymbol.keys():
            self._suit = suit
        else: raise Exception("Invalid suit.")

    def _set_value(self):
        figures = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}

        if (self._rank in Card._allRanks[:9]):
            self._value = int(self._rank)
        elif (self._rank in figures):
            self._value = figures[self._rank]
        else:
            raise Exception("Invalid value.")

    def _set_color(self):
        if (self._suit in ['c', 's']):
            self._color = CardColor('black')
        elif (self._suit in ['h', 'd']):
            self._color = CardColor('red')

    def _set_symbol(self):
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
        """ Removes and returns a card from the top of the deck, else None"""
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

    def top(self) -> Card:
        """Returns the top card of the deck, otherwise None"""
        if (self.isEmpty()): return None
        else: return self._deckCards[-1]

    def inverse(self) -> None:
        """Inverse the order of cards."""
        # self._deckCards = self._deckCards[::-1]
        self._deckCards.reverse() 

    def top_cards(self, n:int) -> List[Card]:
        """Returns a list with the first n cards of the deck"""
        if (n < 0):
            raise AttributeError("Argument must be positive.")
        return self._deckCards[:-n-1:-1]
    
    def __str__(self):
        s = ""
        for i in range(len(self._deckCards)):
            if ((i != 0) and (i % 13 == 0)): s += '\n'
            s += str(self._deckCards[i]) + " "
        return s

    def __repr__(self):
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

class SuitDeck(Deck):
    """A specific kind of deck used to store cards only of the same suit."""
    def __init__(self, suit = ""):
        super().__init__(full = False)
        self._set_suit(suit)
        
    def push(self, rank:str, suit:str):
        # Deck is full
        if (self.isFull()):
            raise Exception("SuitDeck is empty")
        
        # Initially empty deck. Insert card only if it is K or A.
        if (self.isEmpty()):
            if (rank.upper() == 'K' or rank.upper() == 'A'):
                self._suit = suit
                self._deckCards.append(Card(rank,  suit))
                self._nCards += 1
                return
            else: raise Exception(f"SuitDeck can't begin with {rank}")
        
        # Wrong suit
        if (self._suit != suit):
            raise Exception("Invalid suit")

        # New card to insert on the deck
        new_card = Card(rank, suit)

        # Insert card only if it is in the correct order
        if (abs(self.top().value() - new_card.value()) == 1):
            self._deckCards.append(new_card)
            self._nCards += 1
        else:
            raise Exception(f"Card {rank, suit} not in correct order.")
            
    def _set_suit(self, suit:str):
        if (suit == "" or suit.lower() in Card._suitToSymbol.keys()):
            self._suit = suit
        else:
            raise AttributeError(f"suit '{suit}' does not exist.")
    
    def isFull(self):
        if (self.nCards() == 13): return True
        return False
    

if __name__ == "__main__":
    # print(10*'-', "Testing", 10*'-')
    # c1 = Card('A', 'h')
    # c2 = Card('3', 'd')

    # print(c1, c2)
    # print("Id = ", c2.id())
    # print("Same cards") if (c1 == c2) else print("Not same cards")
    # print(c1.color(), c1.rank(), c1.suit(), c1.value(), c1.symbol())

    # if (c1.color() == c2.color()): print("Same color\n")
    # else: print("Not same color")

    # print("Initial Deck")
    # deck1 = Deck()
    # print(deck1)

    # print("\nPop the first 51 cards")
    # for _ in range(51): deck1.pop()

    # print(deck1)

    # print("\nPop the last card")
    # deck1.pop()

    # print(deck1)
    
    # if (deck1.isEmpty()): print("Empty", deck1.nCards())
    # else: print("Non empty")
    
    # #deck1.push("4", 's')

    # print("\nRestore")
    # deck1.restore()
    # print(deck1)

    # print("Number of cards", deck1.nCards())
    specific_deck = SuitDeck()
    specific_deck.push('K', 'c')
    specific_deck.push('Q', 'c')
    specific_deck.push('11', 'c')
    print(specific_deck._deckCards)

    print(specific_deck.nCards())
