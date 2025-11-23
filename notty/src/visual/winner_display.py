"""Winner display dialog for showing the game winner."""

from typing import TYPE_CHECKING

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts.resources.visuals import players
from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_WIDTH

if TYPE_CHECKING:
    from notty.src.visual.player import VisualPlayer


class WinnerDisplay:
    """Dialog for displaying the winner of the game."""

    def __init__(self, screen: pygame.Surface, winner: "VisualPlayer") -> None:
        """Initialize the winner display.

        Args:
            screen: The pygame display surface.
            winner: The winning player object.
        """
        self.screen = screen
        self.winner = winner
        self.winner_name = winner.name

        # Load and scale the winner's image
        png_path = get_resource_path(winner.name + ".png", players)
        img = pygame.image.load(png_path)
        self.winner_image = pygame.transform.scale(img, (200, 200))

        # Button properties
        self.button_width = 250
        self.button_height = 60
        self.button_spacing = 20

        # Calculate button positions
        dialog_width = 600
        dialog_height = 550
        dialog_x = (APP_WIDTH - dialog_width) // 2
        dialog_y = (APP_HEIGHT - dialog_height) // 2

        # New Game button
        self.new_game_button_rect = pygame.Rect(
            dialog_x + (dialog_width - self.button_width) // 2,
            dialog_y + dialog_height - 140,
            self.button_width,
            self.button_height,
        )

        # Quit button
        self.quit_button_rect = pygame.Rect(
            dialog_x + (dialog_width - self.button_width) // 2,
            dialog_y + dialog_height - 140 + self.button_height + self.button_spacing,
            self.button_width,
            self.button_height,
        )

        # Hover states
        self.new_game_hovered = False
        self.quit_hovered = False

    def show(self) -> str:
        """Show the winner display and wait for user to click a button.

        This displays a congratulations message and waits for the user to
        click either "Start New Game" or "Quit".

        Returns:
            "new_game" if user clicked Start New Game, "quit" if user clicked Quit.
        """
        clock = pygame.time.Clock()

        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Check if New Game button was clicked
                    if self.new_game_button_rect.collidepoint(mouse_x, mouse_y):
                        return "new_game"

                    # Check if Quit button was clicked
                    if self.quit_button_rect.collidepoint(mouse_x, mouse_y):
                        return "quit"

            # Update hover states
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.new_game_hovered = self.new_game_button_rect.collidepoint(
                mouse_x, mouse_y
            )
            self.quit_hovered = self.quit_button_rect.collidepoint(mouse_x, mouse_y)

            # Draw
            self._draw()

            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

    def _draw(self) -> None:
        """Draw the winner display dialog."""
        # Draw semi-transparent overlay
        overlay = pygame.Surface((APP_WIDTH, APP_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw dialog background
        dialog_width = 600
        dialog_height = 550
        dialog_x = (APP_WIDTH - dialog_width) // 2
        dialog_y = (APP_HEIGHT - dialog_height) // 2

        # Draw background with gradient effect (using solid color for simplicity)
        pygame.draw.rect(
            self.screen,
            (20, 60, 20),  # Dark green background
            (dialog_x, dialog_y, dialog_width, dialog_height),
        )

        # Draw dialog border with gold color
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (dialog_x, dialog_y, dialog_width, dialog_height),
            5,
        )

        # Draw inner border for extra emphasis
        pygame.draw.rect(
            self.screen,
            (200, 200, 100),  # Lighter gold
            (dialog_x + 10, dialog_y + 10, dialog_width - 20, dialog_height - 20),
            2,
        )

        # Draw "WINNER!" title
        title_font = pygame.font.Font(None, 96)
        title_text = title_font.render("WINNER!", ANTI_ALIASING, (255, 215, 0))
        title_rect = title_text.get_rect(center=(APP_WIDTH // 2, dialog_y + 60))
        self.screen.blit(title_text, title_rect)

        # Draw winner image with gold border
        image_size = 200
        image_x = (APP_WIDTH - image_size) // 2
        image_y = dialog_y + 140

        # Draw gold border around image
        border_padding = 10
        pygame.draw.rect(
            self.screen,
            (255, 215, 0),  # Gold border
            (
                image_x - border_padding,
                image_y - border_padding,
                image_size + 2 * border_padding,
                image_size + 2 * border_padding,
            ),
            5,
        )

        # Draw the winner's image
        self.screen.blit(self.winner_image, (image_x, image_y))

        # Draw winner name below image
        name_font = pygame.font.Font(None, 56)
        name_text = name_font.render(self.winner_name, ANTI_ALIASING, (255, 255, 255))
        name_rect = name_text.get_rect(
            center=(APP_WIDTH // 2, image_y + image_size + 40)
        )
        self.screen.blit(name_text, name_rect)

        # Draw buttons
        self._draw_button(
            self.new_game_button_rect,
            "Start New Game",
            hovered=self.new_game_hovered,
            normal_color=(50, 150, 50),  # Green
            hover_color=(70, 200, 70),  # Lighter green on hover
        )

        self._draw_button(
            self.quit_button_rect,
            "Quit",
            hovered=self.quit_hovered,
            normal_color=(150, 50, 50),  # Red
            hover_color=(200, 70, 70),  # Lighter red on hover
        )

    def _draw_button(
        self,
        rect: pygame.Rect,
        text: str,
        *,
        hovered: bool,
        normal_color: tuple[int, int, int],
        hover_color: tuple[int, int, int],
    ) -> None:
        """Draw a button with hover effect.

        Args:
            rect: The button rectangle.
            text: The button text.
            hovered: Whether the button is hovered.
            normal_color: The normal button color.
            hover_color: The hover button color.
        """
        # Choose color based on hover state
        color = hover_color if hovered else normal_color

        # Draw button background
        pygame.draw.rect(self.screen, color, rect, border_radius=10)

        # Draw button border
        border_color = (255, 215, 0) if hovered else (200, 200, 100)
        pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=10)

        # Draw button text
        button_font = pygame.font.Font(None, 48)
        button_text = button_font.render(text, ANTI_ALIASING, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, text_rect)
