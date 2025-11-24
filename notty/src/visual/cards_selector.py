"""Cards selector dialog for choosing multiple cards to discard as a group."""

from collections.abc import Callable
from typing import TYPE_CHECKING

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH
from notty.src.visual.base_selector import BaseSelector, SelectableButton

if TYPE_CHECKING:
    from notty.src.visual.card import VisualCard


class MultiCardButton(SelectableButton["VisualCard"]):
    """Represents a clickable card button that can be selected/deselected."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        card: "VisualCard",
        card_image: pygame.Surface,
    ) -> None:
        """Initialize a multi-card button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            card: The card this button represents.
            card_image: The image of the card.
        """
        super().__init__(
            x, y, width, height, card, card_image, enabled=True, selectable=True
        )
        self.card = card
        self.card_image = card_image

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        # Determine border color based on state
        if self.selected:
            border_color = (50, 255, 50)  # Green for selected
            border_width = 6
        elif self.hovered:
            border_color = (100, 200, 255)  # Light blue for hover
            border_width = 5
        else:
            border_color = (255, 255, 255)  # White
            border_width = 3

        # Draw border
        border_padding = 5
        pygame.draw.rect(
            screen,
            border_color,
            (
                self.x - border_padding,
                self.y - border_padding,
                self.width + 2 * border_padding,
                self.height + 2 * border_padding,
            ),
            border_width,
        )

        # Draw card image
        screen.blit(self.card_image, (self.x, self.y))

        # Draw checkmark if selected
        if self.selected:
            # Draw a semi-transparent green overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((50, 255, 50, 80))
            screen.blit(overlay, (self.x, self.y))

            # Draw checkmark - scale font size based on card height
            font_size = int(self.height * 0.53)  # 53% of card height
            font = pygame.font.Font(None, font_size)
            checkmark = font.render("✓", ANTI_ALIASING, (255, 255, 255))
            checkmark_rect = checkmark.get_rect(
                center=(self.x + self.width // 2, self.y + self.height // 2)
            )
            screen.blit(checkmark, checkmark_rect)


class SubmitButton:
    """Represents a submit button."""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        """Initialize a submit button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hovered = False
        self.enabled = False

    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if the button was clicked.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.

        Returns:
            True if the button was clicked and is enabled.
        """
        if not self.enabled:
            return False
        return (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def update_hover(self, mouse_x: int, mouse_y: int) -> None:
        """Update hover state based on mouse position.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.
        """
        self.hovered = (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        # Determine button color based on state
        if not self.enabled:
            bg_color = (100, 100, 100)  # Gray for disabled
            text_color = (150, 150, 150)  # Light gray text
            border_color = (80, 80, 80)
        elif self.hovered:
            bg_color = (100, 200, 255)  # Light blue for hover
            text_color = (0, 0, 0)  # Black text
            border_color = (50, 150, 255)
        else:
            bg_color = (50, 150, 50)  # Green for enabled
            text_color = (255, 255, 255)  # White text
            border_color = (30, 100, 30)

        # Draw button background
        pygame.draw.rect(screen, bg_color, (self.x, self.y, self.width, self.height))

        # Draw button border
        pygame.draw.rect(
            screen, border_color, (self.x, self.y, self.width, self.height), 3
        )

        # Draw button text - scale font size based on button height
        font_size = int(self.height * 0.72)  # 72% of button height
        font = pygame.font.Font(None, font_size)
        text_surface = font.render("Submit", ANTI_ALIASING, text_color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )
        screen.blit(text_surface, text_rect)


class CardsSelector(BaseSelector["VisualCard"]):
    """Dialog for selecting multiple cards to discard as a group."""

    def __init__(
        self,
        screen: pygame.Surface,
        available_cards: list["VisualCard"],
        validation_func: Callable[[list["VisualCard"]], bool],
    ) -> None:
        """Initialize the cards selector.

        Args:
            screen: The pygame display surface.
            available_cards: List of cards that can be selected.
            validation_func: Function to validate if selected cards form a valid group.
        """
        self.submit_button: SubmitButton | None = None
        super().__init__(
            screen,
            title="Choose cards to discard as a group",
            items=available_cards,
            max_selections=len(available_cards),  # Can select all cards
            validation_func=validation_func,
        )

    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        card_width = int(APP_WIDTH * 0.05)  # 5% of screen width
        card_height = int(APP_HEIGHT * 0.11)  # 11% of screen height
        card_spacing = int(APP_WIDTH * 0.008)  # 0.8% of screen width
        return card_width, card_height, card_spacing

    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        dialog_width = int(APP_WIDTH * 0.65)  # 65% of screen width
        dialog_height = int(APP_HEIGHT * 0.60)  # 60% of screen height
        return dialog_width, dialog_height

    def _setup_buttons(self) -> None:
        """Set up the card and submit buttons."""
        # Get button dimensions
        card_width, card_height, card_spacing = self._get_button_dimensions()
        max_cards_per_row = 10

        # Calculate how many rows we need
        num_cards = len(self.items)
        num_rows = (num_cards + max_cards_per_row - 1) // max_cards_per_row

        # Calculate starting position (leave room for submit button at bottom)
        start_y = int(
            APP_HEIGHT // 2
            - (num_rows * (card_height + card_spacing)) // 2
            - int(APP_HEIGHT * 0.06)
        )

        # Create buttons for each card
        for i, card in enumerate(self.items):
            row = i // max_cards_per_row
            col = i % max_cards_per_row
            cards_in_row = min(max_cards_per_row, num_cards - row * max_cards_per_row)
            row_width = cards_in_row * card_width + (cards_in_row - 1) * card_spacing
            start_x = int((APP_WIDTH - row_width) // 2)

            x = start_x + col * (card_width + card_spacing)
            y = start_y + row * (card_height + card_spacing)

            # Scale card image
            card_image = pygame.transform.scale(card.png, (card_width, card_height))
            button = MultiCardButton(x, y, card_width, card_height, card, card_image)
            self.buttons.append(button)

        # Create submit button - scale proportionally
        submit_width = int(APP_WIDTH * 0.17)  # 17% of screen width
        submit_height = int(APP_HEIGHT * 0.06)  # 6% of screen height
        submit_x = int((APP_WIDTH - submit_width) // 2)
        submit_y = int(APP_HEIGHT - int(APP_HEIGHT * 0.12))  # 12% from bottom
        self.submit_button = SubmitButton(
            submit_x, submit_y, submit_width, submit_height
        )

    def _update_submit_button_state(self) -> None:
        """Update the submit button enabled state based on selected cards."""
        if self.submit_button:
            self.submit_button.enabled = self._is_valid_selection()

    def show(self) -> list["VisualCard"]:
        """Show the cards selector and wait for user input.

        Returns:
            The list of selected cards.
        """
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if submit button was clicked
                    if self.submit_button and self.submit_button.is_clicked(
                        mouse_x, mouse_y
                    ):
                        return self._get_selected_items()

                    # Check if any card button was clicked
                    for button in self.buttons:
                        if button.is_clicked(mouse_x, mouse_y):
                            button.toggle_selection(
                                len(self._get_selected_items()), self.max_selections
                            )
                            self._update_submit_button_state()
                            break

            # Update hover state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover(mouse_x, mouse_y)
            if self.submit_button:
                self.submit_button.update_hover(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the cards selector dialog."""
        # Call base class _draw to handle overlay, dialog, title, and buttons
        super()._draw()

        # Get dialog dimensions for positioning
        _dialog_width, dialog_height = self._get_dialog_dimensions()
        dialog_y = int((APP_HEIGHT - dialog_height) // 2)

        # Draw instruction - scale font size
        instruction_font_size = int(APP_HEIGHT * 0.034)  # 3.4% of screen height
        instruction_font = pygame.font.Font(None, instruction_font_size)
        selected_cards = self._get_selected_items()
        is_valid = self._is_valid_selection()

        if selected_cards:
            if is_valid:
                instruction = f"Selected {len(selected_cards)} cards - Valid group!"
                color = (50, 255, 50)  # Green
            else:
                instruction = f"Selected {len(selected_cards)} cards - Invalid group"
                color = (255, 50, 50)  # Red
        else:
            instruction = "Click cards to select/deselect"
            color = (200, 200, 200)  # Gray

        instruction_text = instruction_font.render(instruction, ANTI_ALIASING, color)
        instruction_rect = instruction_text.get_rect(
            center=(int(APP_WIDTH // 2), dialog_y + int(APP_HEIGHT * 0.10))
        )
        self.screen.blit(instruction_text, instruction_rect)

        # Draw submit button
        if self.submit_button:
            self.submit_button.draw(self.screen)
