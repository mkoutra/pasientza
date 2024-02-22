# Classes related to playing cards and deck.
# Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
# Suits: c-clubs (♣), d-diamonds (♦), h-hearts (♥) and s-spades (♠)

import copy
import random
from typing import List

class CardColor:
    """Color of a playing card. We assume that the two colors
    are red and black.
    """

    def __init__(self, c:str):
        self._c = c.lower()
        color_mapping = {'r': 0, "red": 0, 'b': 1, "black": 1}
        if self._c in color_mapping:
            self._color = color_mapping[self._c]
        else:
            raise Exception("Invalid CardColor.")

    def __eq__(self, other):
        if isinstance(other, CardColor):
            return self._color == other._color
        raise TypeError("Invalid comparison.")

    def _ne__(self, other):
        return not self == other

    def __str__(self):
        if self._color == 1:
            return "Black"
        if self._color == 0:
            return "Red"

    def __copy__(self):
        return CardColor(self._c)

    def __del__(self):
        del self._c
        del self._color


class Card:
    """Representation of a playing card."""
    _suitToSymbol = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    _allRanks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

    def __init__(self, rank:str, suit:str):
        self._set_rank(rank)
        self._set_suit(suit)
        self._set_value()
        self._set_color()
        self._set_symbol()

    def _set_rank(self, rank:str):
        if rank.upper() in Card._allRanks:
            self._rank = rank
        else:
            raise Exception("Invalid card rank.")

    def _set_suit(self, suit:str):
        if suit.lower() in Card._suitToSymbol:
            self._suit = suit
        else: raise Exception("Invalid suit.")

    def _set_value(self):
        figures = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}

        if self._rank in Card._allRanks[:9]:
            self._value = int(self._rank)
        elif self._rank in figures:
            self._value = figures[self._rank]
        else:
            raise Exception("Rank given is invalid.")

    def _set_color(self):
        _suit_to_color_mapping = {'c': 'b', 's': 'b', 'h': 'r', 'd': 'r'}

        if self._suit in _suit_to_color_mapping:
            self._color = CardColor(_suit_to_color_mapping[self._suit])
        else:
            raise Exception("Suit given has not a matching color.")

    def _set_symbol(self):
        if self._suit in Card._suitToSymbol:
            self._symbol = Card._suitToSymbol[self._suit]
        else:
            raise Exception("Suit given has not a matching symbol.")

    def rank(self) -> str:
        """Returns the rank of the card as a string, e.g. '4'."""
        return self._rank

    def suit(self) -> str:
        """Returns the suit of the card as a string.
        The possible outcomes are: 'c', 's', 'h' or 'd'
        """
        return self._suit

    def color(self) -> CardColor:
        """Returns the card color of the playing card."""
        return self._color

    def value(self) -> int:
        """Returns the value of the playing card.
        The value of the card is equal to its numerical value.
        For cards with figures: A -> 1, J -> 11, Q -> 12 and K -> 13.
        """
        return self._value

    def symbol(self) -> str:
        """Returns the symbol of the playing card (♣, ♦, ♥ or ♠)."""
        return self._symbol

    def id(self) -> str:
        """Returns card's id, concatenation of rank and suit.
        For example: Card('4','h').id() -> 4h.
        """
        return self._rank + self._suit

    def __str__(self) -> str:
        return '(' + self.rank() + "" + self.symbol() + ')'

    def __repr__(self) -> str:
        return self._rank + self._suit

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.rank() == other.rank() and self.suit() == other.suit()
        raise TypeError("Invalid comparison: Can only compare Card objects.")

    def __ne__(self, other):
        return not self == other

    def __copy__(self):
        return Card(self.rank(), self.suit())

    def __del__(self):
        del self._rank
        del self._suit
        del self._color
        del self._value
        del self._symbol


class Deck:
    """ A regular deck of 52 playing cards """

    _suitToSymbol = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    _allRanks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

    def __init__(self, full = True, deck_size = 52):
        """full: optional, True if deck contains 52 cards"""
        self._deck_cards:List[Card] = []    # Cards on the deck.
        self._removed_cards:List[Card] = [] # Cards no longer on the deck
        self._number_of_cards = 0           # Number of cards on the deck
        self._deck_size = deck_size         # Number of cards on a full deck

        if full:
            self.fill_normal_deck()     # Fill deck with the 52 cards
            self.shuffle()              # Shuffle deck

    def deck_size(self):
        """Returns the number of cards contained on a full deck."""
        return self._deck_size

    def contains(self, card: Card) -> bool:
        """Returns True if the card with the rank and the suit
        given is inside the deck.
        """
        for deck_card in self._deck_cards:
            if (deck_card.rank() == card.rank() and
                    deck_card.suit() == card.suit()):
                return True
        return False

    def push(self, card: Card) -> None:
        """ Place a playing card with the rank and the suit given
        at the top of the deck.
        """
        # NOTE: Top card is placed in position -1 inside lists.

        if self.contains(card):
            raise Exception(f"Card {card} is already inside the deck.")

        if self._number_of_cards < self._deck_size:
            self._deck_cards.append(card)
            self._number_of_cards += 1
        else:
            raise Exception(f"Cannot push {card}. Deck is full.")

    def pop(self) -> Card:
        """Removes and returns a card from the top of the deck,
        else None.
        """
        # NOTE: Top card is placed in position -1 inside lists.

        if self._deck_cards:
            popped_card = self._deck_cards.pop()
            self._removed_cards.append(popped_card)
            self._number_of_cards -= 1
            return popped_card

        return None

    def shuffle(self) -> None:
        """ Shuffle the cards on the deck."""
        if self._number_of_cards > 0:
            random.shuffle(self._deck_cards)

    def fill_normal_deck(self) -> None:
        """Fill the deck with the number of cards specified
        on initialization.
        """
        for suit in Deck._suitToSymbol:
            for rank in Deck._allRanks:
                self.push(Card(rank, suit))

    def make_empty(self) -> None:
        """Remove all cards from deck"""
        self._deck_cards.clear()
        self._removed_cards.clear()
        self._number_of_cards = 0

    def restore(self) -> None:
        """Bring deck back to its original condition with 52 cards."""
        if (self._number_of_cards
                + len(self._removed_cards) != self._deck_size):
            raise Exception("Can't go back to original deck.")

        self._number_of_cards = self._deck_size
        self._deck_cards += self._removed_cards[::-1]
        self._removed_cards.clear()

    def is_empty(self) -> bool:
        """Checks if the deck is empty."""
        return self._number_of_cards == 0

    def is_full(self) -> bool:
        """Checks if the deck is full."""
        return self._number_of_cards == self._deck_size

    def number_of_cards(self) -> int:
        """Returns the number of playing cards inside the deck."""
        return self._number_of_cards

    def top(self) -> Card:
        """Returns the top card of the deck, otherwise None"""
        if self.is_empty():
            return None
        return self._deck_cards[-1]

    def inverse(self) -> None:
        """Inverse the order of the cards on the deck."""
        self._deck_cards.reverse()

    def top_cards(self, n:int) -> List[Card]:
        """Returns a list with the first n cards of the deck.
        The first element of the list is the top card.
        """
        if n < 0:
            raise AttributeError("Argument must be positive.")
        return self._deck_cards[:-n-1:-1]

    def __str__(self):
        s = ""
        for i, deck_card in enumerate(self._deck_cards):
            if ((i != 0) and (i % 13 == 0)):
                s += '\n'
            s += str(deck_card) + " "
        return s

    def __repr__(self):
        s = ""
        for i, deck_card in enumerate(self._deck_cards):
            if ((i != 0) and (i % 13 == 0)):
                s += '\n'
            s += str(deck_card) + " "
        return s

    def __getitem__(self, x:int) -> List[Card]:
        if 0 <= x < self._number_of_cards or isinstance(x, slice):
            return self._deck_cards[x]
        return None

    def __copy__(self):
        copy_instance = Deck(full = False)
        copy_instance._deck_cards = self._deck_cards.copy()
        copy_instance._removed_cards = self._removed_cards.copy()
        copy_instance._number_of_cards = self._number_of_cards
        return copy_instance

    def __deepcopy__(self, memo):
        copy_instance = Deck(full = False)
        copy_instance._deck_cards = copy.deepcopy(self._deck_cards)
        copy_instance._removed_cards = copy.deepcopy(self._removed_cards)
        copy_instance._number_of_cards = self._number_of_cards
        return copy_instance

    def __del__(self):
        self._deck_cards.clear()
        self._removed_cards.clear()
        del self._deck_cards
        del self._removed_cards
        del self._number_of_cards


class SuitDeck(Deck):
    """A specific kind of deck used to store cards of the same suit."""

    def __init__(self, suit = ""):
        super().__init__(full = False, deck_size = 13)
        self._deck_suit = suit
        self._set_deck_suit(suit)

    def _set_deck_suit(self, suit:str):
        if (suit == "" or suit.lower() in Deck._suitToSymbol):
            self._deck_suit = suit
        else:
            raise AttributeError(f"Suit '{suit}' does not exist.")

    def deck_suit(self) -> str:
        """Returns the suit of the suitDeck"""
        return self._deck_suit

    def push(self, card: Card) -> None:
        # Deck is full
        if self.is_full():
            raise Exception("SuitDeck is full.")

        # If SuitDeck is empty allow only K or A to be inserted.
        if self.is_empty():
            if card.rank().upper() not in "KA":
                raise Exception(f"SuitDeck can't start with {card.rank()}.")

            self._deck_suit = card.suit()
            self._deck_cards.append(card)
            self._number_of_cards += 1
        else:
            if self._deck_suit != card.suit():
                raise Exception("Card's suit does not match deck's suit.")

            # Insert card only if it is in the correct order
            if abs(self.top().value() - card.value()) != 1:
                raise Exception(f"Card {card} is not in correct order.")

            self._deck_cards.append(card)
            self._number_of_cards += 1

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
