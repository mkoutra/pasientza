""" This file contains the class used to represent playing cards
and playing card colors.

----------------------------------
Michail E. Koutrakis
Github: https://github.com/mkoutra
"""

class CardColor:
    """Color of a playing card. We assume that the two colors
    are red and black. General information about playing cards:
    Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
    Suits: c-clubs (♣), d-diamonds (♦), h-hearts (♥) and s-spades (♠)
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
        return None

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
