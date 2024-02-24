"""This file contains the Deck class used to represent a normal
52 playing card deck. Also, it contains a class SuitDeck inherited
by Deck that is used to represent the eight, initially empty stacks
used to store the cards removed from Deck and 'soros'.
"""

import copy
import random
from typing import List

from .Card import Card

class Deck:
    """ A regular deck of playing cards."""

    _suitToSymbol = {'c': '♣', 'd': '♦', 'h': '♥', 's': '♠'}
    _allRanks = [str(i) for i in range(2, 11)] + ['J', 'Q', 'K', 'A']

    def __init__(self, full = True, deck_size = 52):
        """full: optional, If True the deck contains deck_size cards"""
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