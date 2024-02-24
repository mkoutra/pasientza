"""Pasientza main function"""

from lib.Decks import Deck
from lib.GameWindow import GameWindow

def main():
    """Main function."""
    deck = Deck()
    window = GameWindow(deck)
    window.draw()

if __name__ == "__main__":
    main()
