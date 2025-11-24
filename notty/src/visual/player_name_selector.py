"""Player name selector for initial player selection."""

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts.resources.visuals import players
from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH
from notty.src.visual.base_selector import BaseSelector, SelectableButton


class PlayerNameButton(SelectableButton[str]):
    """Represents a clickable player name button with image."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        player_name: str,
        player_image: pygame.Surface,
        *,
        enabled: bool = True,
        selectable: bool = False,
    ) -> None:
        """Initialize a player name button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            player_name: The name of the player.
            player_image: The image of the player.
            enabled: Whether the button is enabled.
            selectable: Whether the button can be selected/deselected.
        """
        super().__init__(
            x,
            y,
            width,
            height,
            player_name,
            player_image,
            enabled=enabled,
            selectable=selectable,
        )
        self.player_name = player_name
        self.player_image = player_image

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button.

        Args:
            screen: The pygame display surface.
        """
        # Determine border color based on state
        if self.selected:
            border_color = (50, 255, 50)  # Green for selected
            border_width = 5
        elif self.hovered:
            border_color = (100, 200, 255)  # Light blue for hover
            border_width = 5
        else:
            border_color = (255, 255, 255)  # White
            border_width = 2

        # Draw border
        border_padding = int(APP_WIDTH * 0.008)  # 0.8% of screen width
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

        # Draw player image
        screen.blit(self.player_image, (self.x, self.y))

        # Draw player name
        name_font_size = int(APP_HEIGHT * 0.06)  # 6% of screen height
        name_font = pygame.font.Font(None, name_font_size)
        color = (
            (50, 255, 50)
            if self.selected
            else ((100, 200, 255) if self.hovered else (255, 255, 255))
        )
        name_text = name_font.render(
            self.player_name.capitalize(), ANTI_ALIASING, color
        )
        name_rect = name_text.get_rect(
            center=(
                self.x + self.width // 2,
                self.y + self.height + int(APP_HEIGHT * 0.04),
            )
        )
        screen.blit(name_text, name_rect)


class PlayerNameSelector(BaseSelector[str]):
    """Dialog for selecting player name(s) at game start."""

    def __init__(
        self,
        screen: pygame.Surface,
        available_names: list[str],
        title: str,
        *,
        max_selections: int = 1,
        min_selections: int = 1,
    ) -> None:
        """Initialize the player name selector.

        Args:
            screen: The pygame display surface.
            available_names: List of available player names.
            title: Title to display.
            max_selections: Maximum number of selections allowed.
            min_selections: Minimum number of selections required.
        """
        self.min_selections = min_selections
        self.needs_submit = max_selections > 1
        super().__init__(
            screen,
            title=title,
            items=available_names,
            max_selections=max_selections,
        )

    def _get_button_dimensions(self) -> tuple[int, int, int]:
        """Get button dimensions (width, height, spacing).

        Returns:
            Tuple of (button_width, button_height, button_spacing).
        """
        image_size = int(APP_WIDTH * 0.12)  # 12% of screen width
        spacing = int(APP_WIDTH * 0.02)  # 2% of screen width
        return image_size, image_size, spacing

    def _get_dialog_dimensions(self) -> tuple[int, int]:
        """Get dialog dimensions.

        Returns:
            Tuple of (dialog_width, dialog_height).
        """
        # Full screen for player selection
        return APP_WIDTH, APP_HEIGHT

    def _setup_buttons(self) -> None:
        """Set up the player name buttons."""
        image_size, _, _spacing = self._get_button_dimensions()

        # Load player images
        player_images: dict[str, pygame.Surface] = {}
        for name in self.items:
            png_path = get_resource_path(name + ".png", players)
            img = pygame.image.load(png_path)
            player_images[name] = pygame.transform.scale(img, (image_size, image_size))

        # Calculate positions - center horizontally
        player_spacing = APP_WIDTH // (len(self.items) + 1)
        for i, name in enumerate(self.items):
            x = player_spacing * (i + 1) - image_size // 2
            y = APP_HEIGHT // 2 - image_size // 2

            button = PlayerNameButton(
                x,
                y,
                image_size,
                image_size,
                name,
                player_images[name],
                enabled=True,
                selectable=self.needs_submit,
            )
            self.buttons.append(button)

    def _draw(self) -> None:
        """Draw the player name selector."""
        # Draw black background (no overlay for full screen)
        self.screen.fill((0, 0, 0))

        # Draw title
        title_font_size = int(APP_HEIGHT * 0.09)  # 9% of screen height
        title_font = pygame.font.Font(None, title_font_size)
        title_text = title_font.render(self.title, ANTI_ALIASING, (255, 255, 255))
        title_rect = title_text.get_rect(
            center=(APP_WIDTH // 2, int(APP_HEIGHT * 0.12))
        )
        self.screen.blit(title_text, title_rect)

        # Draw instruction
        instruction_font_size = int(APP_HEIGHT * 0.045)  # 4.5% of screen height
        instruction_font = pygame.font.Font(None, instruction_font_size)
        if self.needs_submit:
            instruction = "Click to select/deselect • Press ENTER when done"
        else:
            instruction = "Click on a player to select"
        instruction_text = instruction_font.render(
            instruction, ANTI_ALIASING, (255, 255, 255)
        )
        instruction_rect = instruction_text.get_rect(
            center=(APP_WIDTH // 2, int(APP_HEIGHT * 0.22))
        )
        self.screen.blit(instruction_text, instruction_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

    def show(self) -> str | list[str]:  # noqa: C901
        """Show the player name selector and wait for user input.

        Returns:
            Selected player name (single) or list of names (multiple).
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
                    for button in self.buttons:
                        if button.is_clicked(mouse_x, mouse_y):
                            if self.needs_submit:
                                # Multi-select mode: toggle selection
                                current_count = len(self._get_selected_items())
                                button.toggle_selection(
                                    current_count, self.max_selections
                                )
                            else:
                                # Single-select mode: return immediately
                                return button.item
                elif event.type == pygame.KEYDOWN and self.needs_submit:
                    if event.key == pygame.K_RETURN:
                        selected = self._get_selected_items()
                        if len(selected) >= self.min_selections:
                            return selected

            # Update hover state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update_hover(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
