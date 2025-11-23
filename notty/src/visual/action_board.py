"""Action board for displaying available actions to the human player."""

from typing import TYPE_CHECKING

import pygame

from notty.src.consts import (
    ACTION_BOARD_HEIGHT,
    ACTION_BOARD_WIDTH,
    ACTION_BOARD_X,
    ACTION_BOARD_Y,
    ANTI_ALIASING,
)

if TYPE_CHECKING:
    from notty.src.visual.game import VisualGame


class Action:
    """Represents an action in the Notty game."""

    DRAW_MULTIPLE = "draw_multiple"
    STEAL = "steal"
    DRAW_DISCARD_DRAW = "draw_discard_draw"
    DRAW_DISCARD_DISCARD = "draw_discard_discard"
    DISCARD_GROUP = "discard_group"
    NEXT_TURN = "next_turn"
    PLAY_FOR_ME = "play_for_me"

    @classmethod
    def get_all_actions(cls) -> set[str]:
        """Get all actions."""
        return {
            cls.DRAW_MULTIPLE,
            cls.STEAL,
            cls.DRAW_DISCARD_DRAW,
            cls.DRAW_DISCARD_DISCARD,
            cls.DISCARD_GROUP,
            cls.NEXT_TURN,
        }


class ActionButton:
    """Represents a clickable action button."""

    def __init__(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        action_name: str,
        *,
        enabled: bool = True,
    ) -> None:
        """Initialize an action button.

        Args:
            x: X coordinate of the button.
            y: Y coordinate of the button.
            width: Width of the button.
            height: Height of the button.
            text: Text to display on the button.
            action_name: Name of the action this button represents.
            enabled: Whether the button is enabled.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.action_name = action_name
        self.enabled = enabled
        self.hovered = False

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
            alpha = 100  # Faded out
        elif self.hovered:
            bg_color = (100, 200, 255)  # Light blue for hover
            text_color = (0, 0, 0)  # Black text
            border_color = (50, 150, 255)
            alpha = 255  # Fully visible
        else:
            bg_color = (50, 150, 50)  # Green for enabled
            text_color = (255, 255, 255)  # White text
            border_color = (30, 100, 30)
            alpha = 255  # Fully visible

        # Create a surface for the button with alpha channel
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw button background on the surface
        pygame.draw.rect(button_surface, bg_color, (0, 0, self.width, self.height))

        # Draw button border on the surface
        pygame.draw.rect(
            button_surface, border_color, (0, 0, self.width, self.height), 3
        )

        # Draw button text on the surface - scale font size based on button height
        font_size = int(self.height * 0.5)  # 70% of button height (doubled from 35%)
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(self.text, ANTI_ALIASING, text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        button_surface.blit(text_surface, text_rect)

        # Set alpha and blit to screen
        button_surface.set_alpha(alpha)
        screen.blit(button_surface, (self.x, self.y))


class ActionBoard:
    """Action board that displays available actions for the human player."""

    def __init__(
        self,
        screen: pygame.Surface,
        human_player_index: int,
        game: "VisualGame",
    ) -> None:
        """Initialize the action board.

        Args:
            screen: The pygame display surface.
            human_player_index: Index of the human player (0-2).
            game: The game instance for checking action availability.
        """
        self.screen = screen
        self.human_player_index = human_player_index
        self.game = game
        self.buttons: list[ActionButton] = []
        self._setup_buttons()

    def _setup_buttons(self) -> None:
        """Set up the action buttons."""
        # Use constants from consts.py for action board position and size
        board_x = ACTION_BOARD_X
        board_y = ACTION_BOARD_Y
        board_width = ACTION_BOARD_WIDTH
        board_height = ACTION_BOARD_HEIGHT

        # Define all possible actions
        actions = [
            ("Draw 1-3 Cards", Action.DRAW_MULTIPLE),
            ("Steal Card", Action.STEAL),
            ("Draw & Discard (Draw)", Action.DRAW_DISCARD_DRAW),
            ("Draw & Discard (Discard)", Action.DRAW_DISCARD_DISCARD),
            ("Discard Group", Action.DISCARD_GROUP),
            ("Next Turn", Action.NEXT_TURN),
            ("Play for Me", Action.PLAY_FOR_ME),
        ]

        # Calculate button dimensions based on action board size and number of buttons
        num_buttons = len(actions)
        button_spacing = 10
        total_spacing = button_spacing * (
            num_buttons + 1
        )  # Spacing above, below, and between buttons

        # Button width is board width minus padding on both sides
        button_padding = 15
        button_width = board_width - (2 * button_padding)

        # Button height is calculated to fit all buttons with spacing
        button_height = (board_height - total_spacing) // num_buttons

        # Create buttons
        for i, (text, action_name) in enumerate(actions):
            y = board_y + button_spacing + i * (button_height + button_spacing)
            x = board_x + button_padding
            button = ActionButton(
                x=x,
                y=y,
                width=button_width,
                height=button_height,
                text=text,
                action_name=action_name,
                enabled=False,  # Will be updated based on game state
            )
            self.buttons.append(button)

    def update_button_states(self, game: "VisualGame") -> None:
        """Update button enabled states based on current game state.

        Args:
            game: The game instance to check action availability.
        """
        current_player = game.get_current_player()
        is_human_turn = current_player.is_human

        for button in self.buttons:
            if not is_human_turn:
                button.enabled = False
            elif button.action_name == Action.PLAY_FOR_ME:
                # "Play for Me" button is always enabled during human's turn
                button.enabled = True
            else:
                button.enabled = game.action_is_possible(button.action_name)

    def update_hover(self, mouse_x: int, mouse_y: int) -> None:
        """Update hover state for all buttons.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.
        """
        for button in self.buttons:
            button.update_hover(mouse_x, mouse_y)

    def handle_click(self, mouse_x: int, mouse_y: int) -> None:
        """Handle click on action board.

        Args:
            mouse_x: Mouse x coordinate.
            mouse_y: Mouse y coordinate.

        Returns:
            The action name if a button was clicked, None otherwise.
        """
        game = self.game
        for button in self.buttons:
            enabled = button.enabled
            clicked = button.is_clicked(mouse_x, mouse_y)
            action_name = button.action_name
            if enabled and clicked:
                game.do_action(action_name)

    def draw(self) -> None:
        """Draw the action board and all buttons.

        Automatically updates button states before drawing.
        """
        # Automatically update button states based on current game state
        self.update_button_states(self.game)

        # Draw background panel
        panel_padding = 15
        if self.buttons:
            first_button = self.buttons[0]
            last_button = self.buttons[-1]

            panel_x = first_button.x - panel_padding
            panel_y = first_button.y - panel_padding
            panel_width = first_button.width + 2 * panel_padding
            panel_height = (
                last_button.y + last_button.height - first_button.y + 2 * panel_padding
            )

            # Draw semi-transparent background
            panel_surface = pygame.Surface((panel_width, panel_height))
            panel_surface.set_alpha(200)
            panel_surface.fill((40, 40, 40))
            self.screen.blit(panel_surface, (panel_x, panel_y))

            # Draw border
            pygame.draw.rect(
                self.screen,
                (200, 200, 200),
                (panel_x, panel_y, panel_width, panel_height),
                3,
            )

            # Draw title - scale font size
            font_size = int(ACTION_BOARD_HEIGHT * 0.04)  # 4% of action board height
            font = pygame.font.Font(None, font_size)
            title_text = font.render("Actions", ANTI_ALIASING, (255, 255, 255))
            title_rect = title_text.get_rect(
                center=(
                    panel_x + panel_width // 2,
                    panel_y - int(ACTION_BOARD_HEIGHT * 0.025),
                )
            )
            self.screen.blit(title_text, title_rect)

        # Draw all buttons
        for button in self.buttons:
            button.draw(self.screen)
