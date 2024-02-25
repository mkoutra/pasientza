"""Pasientza main function
----------------------------------
Michail E. Koutrakis
Github: https://github.com/mkoutra
"""

from lib.Decks import Deck
from lib.GameWindow import GameWindow

def main():
    """Main function."""
    deck = Deck()
    window = GameWindow(deck)
    window.draw()

if __name__ == "__main__":
    main()
