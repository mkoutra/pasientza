# "Pasientza" (Solitaire) card game
Pasientza is a simple solo card game requiring a standard deck of 52 cards.

## Installation
Python version 3.0+
## Pasientza Game rules

### Objective
Successfully place all the cards from the deck onto the eight stacks following the order A->2->3->...->K or K->Q->J->...->A and the same suit.

### Setup
- Use a standard 52-card deck.
- Create eight empty stacks for organizing the cards and an empty stack to keep the cards removed from deck, called "soros".

### Gameplay
1. Remove three cards from the deck and place them face up on the "soros".
2. If the top card of "soros" is "A" or "K," place it on one of the eight empty stacks. Execute step 2 again.
3. If the top card of "soros" has both the following properties:
   -  Its value is one larger or smaller than the top card of any of the eight stacks.
   -  It has the same suit as that specific top card
  
    Place the top card of "soros" on the top of that matching stack and go back to step 2.
4. If the top card of "soros" does not fit the criteria in step 2 or 3, go back to step 1.
5. If the deck becomes empty, reverse the "soros" and create a new deck from it. Go to step 1.
6. If both the deck and "soros" are empty, you have won the game.
7. If you keep drawing cards, and nothing changes, start a new game.

![alt text](Pasientza_image.png)