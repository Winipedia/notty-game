"""Base selector dialog for choosing items with images."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar

import pygame

from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH

T = TypeVar("T")


class SelectableButton[T](ABC):
    """Base class for selectable buttons with images."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        item: T,
        image: pygame.Surface | None = None,
        *,
        enabled: bool = True,
        selectable: bool = False,
    ) -> None:
        """Initialize a selectable button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            item: The item this button represents.
            image: The image to display.
            enabled: Whether the button is enabled (clickable).
            selectable: Whether the button can be selected (for multi-select).
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item = item
        self.image = image
        self.enabled = enabled
        self.selectable = selectable
        self.hovered = False
        self.selected = False

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
        if not self.enabled:
            self.hovered = False
            return
        self.hovered = (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def toggle_selection(
        self, current_selected_count: int, max_selections: int
    ) -> None:
        """Toggle the selection state of this button.

        Args:
            current_selected_count: Number of currently selected items.
            max_selections: Maximum number of selections allowed.
        """
        if self.selectable:
            if self.selected:
                # Always allow deselection
                self.selected = False
            elif current_selected_count < max_selections:
                # Only allow selection if under max
                self.selected = True

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        ...


class BaseSelector[T](ABC):
    """Base class for selector dialogs."""

    def __init__(
        self,
        screen: pygame.Surface,
        title: str,
        items: list[T],
        *,
        max_selections: int = 1,
        validation_func: Callable[[list[T]], bool] | None = None,
    ) -> None:
        """Initialize the base selector.

        Args:
            screen: The pygame display surface.
            title: Title to display in the dialog.
            items: List of items that can be selected.
            max_selections: Maximum number of items that can be selected
                (1 for single select).
            validation_func: Optional function to validate if selection is valid.
        """
        self.screen = screen
        self.title = title
        self.items = items
        self.max_selections = max_selections
        self.validation_func = validation_func
        self.buttons: list[SelectableButton[T]] = []
        self._setup_buttons()

    @abstractmethod
    def _setup_buttons(self) -> None:
        """Set up the selectable buttons. Must be implemented by subclasses."""
        ...

    @abstractmethod
    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        ...

    @abstractmethod
    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        ...

    def _get_selected_items(self) -> list[T]:
        """Get the list of currently selected items.

        Returns:
            List of selected items.
        """
        return [button.item for button in self.buttons if button.selected]

    def _is_valid_selection(self) -> bool:
        """Check if the current selection is valid.

        Returns:
            True if the selection is valid.
        """
        selected = self._get_selected_items()
        if not selected:
            return False
        if self.validation_func:
            return self.validation_func(selected)
        return len(selected) <= self.max_selections

    def show(self) -> list[T] | T | None:
        """Show the selector and wait for user input.

        Returns:
            The selected item(s). Returns single item if max_selections=1,
                list otherwise.
            Returns None if no selection was made.
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

                    # Check if any button was clicked
                    for button in self.buttons:
                        if button.is_clicked(mouse_x, mouse_y):
                            if self.max_selections == 1:
                                # Single selection - return immediately
                                return button.item
                            # Multi-selection - toggle selection
                            current_count = len(self._get_selected_items())
                            button.toggle_selection(current_count, self.max_selections)
                            break

            # Update hover state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the selector dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((int(APP_WIDTH), int(APP_HEIGHT)))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Get dialog dimensions
        dialog_width, dialog_height = self._get_dialog_dimensions()
        dialog_x = int((APP_WIDTH - dialog_width) // 2)
        dialog_y = int((APP_HEIGHT - dialog_height) // 2)

        # Draw dialog background
        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            (dialog_x, dialog_y, dialog_width, dialog_height),
        )

        # Draw dialog border
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            (dialog_x, dialog_y, dialog_width, dialog_height),
            3,
        )

        # Draw title
        font_size = int(APP_HEIGHT * 0.06)  # 6% of screen height
        font = pygame.font.Font(None, font_size)
        title_text = font.render(self.title, ANTI_ALIASING, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(int(APP_WIDTH // 2), dialog_y + int(APP_HEIGHT * 0.06))
        )
        self.screen.blit(title_text, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
