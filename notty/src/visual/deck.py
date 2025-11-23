"""visual deck."""

import random
from types import ModuleType

import pygame

from notty.dev.artifacts.resources.visuals import deck
from notty.src.consts import (
    ANTI_ALIASING,
    DECK_HEIGHT,
    DECK_POS_X,
    DECK_POS_Y,
    DECK_WIDTH,
)
from notty.src.visual.base import Visual
from notty.src.visual.card import Color, Number, VisualCard


class VisualDeck(Visual):
    """Visual deck."""

    NUM_DUPLICATES = 2

    def draw(self) -> None:
        """Draw the visual element.

        Args:
            screen: The pygame display surface.
        """
        for card in self.cards:
            card.draw()
        super().draw()
        # Cards stay hidden behind the deck - only draw the deck image
        # draw the number of cards in the deck in black
        font = pygame.font.Font(None, 100)
        text = font.render(str(self.size()), ANTI_ALIASING, (0, 0, 0))
        self.screen.blit(text, (self.x + 10, self.y + 10))

    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        """Initialize a visual deck.

        Args:
            x: X coordinate. Always represents the top-left corner.
            y: Y coordinate. Always represents the top-left corner.
            height: Height of the visual element.
            width: Width of the visual element.
            screen: The pygame display surface.
            deck: The deck to visualize.
        """
        self.cards: list[VisualCard] = []
        super().__init__(DECK_POS_X, DECK_POS_Y, DECK_HEIGHT, DECK_WIDTH, screen)
        self._initialize_deck()

    def _initialize_deck(self) -> None:
        """Create all 90 cards (2 of each color-number combination)."""
        self.cards = []
        for color in Color.get_all_colors():
            for number in Number.get_all_numbers():
                for _ in range(self.NUM_DUPLICATES):
                    self.add_card(
                        VisualCard(color, number, DECK_POS_X, DECK_POS_Y, self.screen)
                    )

    def get_png_name(self) -> str:
        """Get the png for the visual element."""
        return "deck"

    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
        return deck

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def draw_card(self) -> VisualCard:
        """Draw the top card from the deck.

        Returns:
            The top card, or raises ValueError if deck is empty.
        """
        if not self.cards:
            msg = "Cannot draw from an empty deck"
            raise ValueError(msg)
        return self.cards.pop()

    def draw_cards(self, count: int) -> list[VisualCard]:
        """Draw multiple cards from the deck.

        Args:
            count: Number of cards to draw.

        Returns:
            List of drawn cards (may be fewer than requested if deck runs out).
        """
        drawn_cards: list[VisualCard] = []
        for _ in range(count):
            if self.is_empty():
                break
            card = self.draw_card()
            drawn_cards.append(card)
        return drawn_cards

    def add_cards(self, cards: list[VisualCard]) -> None:
        """Add cards back to the deck (used when discarding).

        Args:
            cards: List of cards to add back to the deck.
        """
        for card in cards:
            self.add_card(card)

    def add_card(self, card: VisualCard) -> None:
        """Add a single card back to the deck (used when discarding).

        Args:
            card: VisualCard to add back to the deck.
        """
        self.cards.append(card)
        # move the card to the middle of the deck
        x, y = self.get_center()
        card.move(x, y)
        self.shuffle()

    def is_empty(self) -> bool:
        """Check if the deck is empty.

        Returns:
            True if the deck has no cards, False otherwise.
        """
        return len(self.cards) == 0

    def size(self) -> int:
        """Get the number of cards in the deck.

        Returns:
            Number of cards currently in the deck.
        """
        return len(self.cards)

    def __len__(self) -> int:
        """Return the number of cards in the deck."""
        return len(self.cards)
