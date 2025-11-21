"""Main entrypoint for the project."""

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts import resources
from notty.src.card import Color
from notty.src.consts import ANTI_ALIASING, APP_NAME
from notty.src.deck import Deck
from notty.src.game import Game
from notty.src.player import Player

# Color constants
CARD_BACK_COLOR = "NEUTRAL"

# Global color map for cards and deck
COLOR_MAP = {
    Color.RED: (220, 20, 60),
    Color.GREEN: (34, 139, 34),
    Color.YELLOW: (255, 215, 0),
    Color.BLACK: (50, 50, 50),
    Color.BLUE: (30, 144, 255),
    CARD_BACK_COLOR: (100, 100, 120),  # Neutral gray-blue for deck
}


def main() -> None:
    """Start the notty game."""
    pygame.init()

    run()

    pygame.quit()


def run() -> None:
    """Run the game."""
    # Get screen dimensions
    app_width, app_height = get_window_size()

    screen = create_window(app_width, app_height)

    # initialize game
    game = init_game()

    # load background image
    background = load_background(app_width, app_height)

    # simulate first shuffle and deal
    simulate_first_shuffle_and_deal(screen, game, background, app_width, app_height)

    # run the event loop
    run_event_loop(screen, game, background, app_width, app_height)


def get_window_size() -> tuple[int, int]:
    """Get the window size based on screen dimensions.

    Returns:
        Tuple of (width, height) for the window.
    """
    # Get the display info to determine screen size
    display_info = pygame.display.Info()
    screen_width = display_info.current_w
    screen_height = display_info.current_h

    # Use 80% of screen width and 70% of screen height
    factor = 0.8
    app_width = int(screen_width * factor)
    app_height = int(screen_height * factor)

    # Set minimum dimensions to ensure usability
    min_width = 800
    min_height = 500

    app_width = max(app_width, min_width)
    app_height = max(app_height, min_height)

    return app_width, app_height


def create_window(app_width: int, app_height: int) -> pygame.Surface:
    """Create the game window.

    Args:
        app_width: Width of the window.
        app_height: Height of the window.
    """
    screen = pygame.display.set_mode((app_width, app_height))
    # set the title
    pygame.display.set_caption(APP_NAME)
    return screen


def load_background(app_width: int, app_height: int) -> pygame.Surface:
    """Load and scale the background image.

    Args:
        app_width: Width of the window.
        app_height: Height of the window.
    """
    # Get the path to the icon.png file
    icon_path = get_resource_path("icon.png", resources)

    # Load the image
    background = pygame.image.load(icon_path).convert()

    # Scale it to fit the window
    background = pygame.transform.scale(background, (app_width, app_height))

    # Make the background less visible by creating a dimmed version
    # Create a semi-transparent dark overlay
    overlay = pygame.Surface((app_width, app_height))
    overlay.set_alpha(150)  # High opacity for the dark overlay (200 out of 255)
    overlay.fill((20, 20, 20))  # Very dark gray

    # Blend the overlay onto the background
    background.blit(overlay, (0, 0))

    return background


def simulate_first_shuffle_and_deal(
    screen: pygame.Surface,
    game: Game,
    background: pygame.Surface,
    app_width: int,
    app_height: int,
) -> None:
    """Simulate the first shuffle and deal with visual animation.

    Game internally already calls setup and does the logic.
    But we want to show the cards being shuffled and dealt.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        background: The background image surface.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    clock = pygame.time.Clock()

    # Deck dimensions (same as in show_deck)
    deck_width = int(app_width * 0.10)
    deck_height = int(app_height * 0.3)
    deck_x = app_width // 2 - deck_width // 2
    deck_y = int(app_height * 0.05)

    # Shuffling animation - show deck "shaking"
    shuffle_frames = 30
    for frame in range(shuffle_frames):
        screen.blit(background, (0, 0))

        # Shake the deck by offsetting it slightly
        shake_offset_x = (frame % 4 - 2) * 3
        shake_offset_y = (frame % 3 - 1) * 2

        # Draw shaking deck
        pygame.draw.rect(
            screen,
            COLOR_MAP[CARD_BACK_COLOR],
            (deck_x + shake_offset_x, deck_y + shake_offset_y, deck_width, deck_height),
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (deck_x + shake_offset_x, deck_y + shake_offset_y, deck_width, deck_height),
            3,
        )

        # Show "SHUFFLING..." text
        font_size = max(int(app_height * 0.05), 24)
        font = pygame.font.Font(None, font_size)
        shuffle_text = font.render("SHUFFLING...", ANTI_ALIASING, (255, 255, 255))
        text_rect = shuffle_text.get_rect(center=(app_width // 2, app_height // 2))
        screen.blit(shuffle_text, text_rect)

        pygame.display.flip()
        clock.tick(30)  # 30 FPS for animation

    # Dealing animation - show cards moving from deck to players
    cards_per_player = game.INITIAL_HAND_SIZE
    num_players = len(game.players)

    for card_num in range(cards_per_player):
        for player_idx in range(num_players):
            # Animate card moving from deck to player
            deal_frames = 15

            # Calculate player position
            player_width = app_width // num_players
            player_x = player_idx * player_width

            # Calculate card dimensions
            card_height = int(app_height * 0.08)
            card_width = int(card_height * 0.7)

            # Calculate destination position
            name_offset_x = int(app_height * 0.03)
            total_cards_height = 4 * card_height + 3 * int(app_height * 0.01)
            name_height = int(app_height * 0.06)
            total_player_height = (
                name_height + total_cards_height + int(app_height * 0.02)
            )
            player_y = app_height - total_player_height - int(app_height * 0.02)

            dest_x = (
                player_x
                + name_offset_x
                + card_num * (card_width + int(app_height * 0.008))
            )
            dest_y = player_y

            # Animate card movement
            for frame in range(deal_frames):
                screen.blit(background, (0, 0))

                # Draw static deck
                show_deck(screen, game.deck, app_width, app_height)

                # Calculate moving card position (interpolate from deck to player)
                t = frame / deal_frames  # 0 to 1
                card_x = deck_x + (dest_x - deck_x) * t
                card_y = deck_y + (dest_y - deck_y) * t

                # Draw moving card
                pygame.draw.rect(
                    screen,
                    COLOR_MAP[CARD_BACK_COLOR],
                    (card_x, card_y, card_width, card_height),
                )
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (card_x, card_y, card_width, card_height),
                    2,
                )

                pygame.display.flip()
                clock.tick(60)  # 60 FPS for smooth animation


def init_game() -> Game:
    """Add players to the game."""
    return Game(get_players())


def get_players() -> list[Player]:
    """Get the players."""
    # Needed: Make players configurable by the real player
    player_1 = Player("Human", is_human=True)
    player_2 = Player("Computer 1", is_human=False)
    player_3 = Player("Computer 2", is_human=False)
    return [player_1, player_2, player_3]


def show_deck(
    screen: pygame.Surface, deck: Deck, app_width: int, app_height: int
) -> None:
    """Display the deck widget.

    Args:
        screen: The pygame display surface.
        deck: The deck to display.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    # Deck dimensions scale with window size (twice as big)
    deck_width = int(app_width * 0.10)  # 16% of window width
    deck_height = int(app_height * 0.3)  # 50% of window height

    # Deck position (top center of screen, positioned higher)
    deck_x = app_width // 2 - deck_width // 2
    deck_y = int(app_height * 0.05)  # 5% from top

    # Draw deck background (card back) using neutral color
    pygame.draw.rect(
        screen, COLOR_MAP[CARD_BACK_COLOR], (deck_x, deck_y, deck_width, deck_height)
    )
    pygame.draw.rect(
        screen, (255, 255, 255), (deck_x, deck_y, deck_width, deck_height), 3
    )

    # Display card count (font size scales with deck size)
    font_size = max(int(deck_height * 0.2), 16)  # At least 16px
    font = pygame.font.Font(None, font_size)
    count_text = font.render(str(deck.size()), ANTI_ALIASING, (255, 255, 255))
    text_rect = count_text.get_rect(
        center=(deck_x + deck_width // 2, deck_y + deck_height // 2)
    )
    screen.blit(count_text, text_rect)

    # Display "DECK" label
    label_font_size = max(int(deck_height * 0.15), 14)  # At least 14px
    label_font = pygame.font.Font(None, label_font_size)
    label_text = label_font.render("DECK", ANTI_ALIASING, (255, 255, 255))
    label_spacing = int(app_height * 0.03)
    label_rect = label_text.get_rect(
        center=(deck_x + deck_width // 2, deck_y + deck_height + label_spacing)
    )
    screen.blit(label_text, label_rect)


def show_players(
    screen: pygame.Surface, game: Game, app_width: int, app_height: int
) -> None:
    """Display all players.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    # Position players horizontally across the bottom of the screen
    num_players = len(game.players)
    player_width = app_width // num_players

    for i, player in enumerate(game.players):
        player_x = i * player_width
        show_player_with_hand(screen, player, player_x, app_height)


def show_player_with_hand(
    screen: pygame.Surface, player: Player, x_position: int, app_height: int
) -> None:
    """Display a player with their hand.

    Args:
        screen: The pygame display surface.
        player: The player to display.
        x_position: The x position to start drawing the player area.
        app_height: Height of the window.
    """
    # Card dimensions scale with window size (sized to fit 4 rows of 5 cards)
    cards_per_row = 5
    max_rows = 4

    # Calculate card size to fit 4 rows in the available space
    card_height = int(app_height * 0.08)  # 8% of window height per card
    card_width = int(card_height * 0.7)  # Maintain aspect ratio
    card_spacing_x = int(app_height * 0.008)  # Horizontal spacing
    card_spacing_y = int(app_height * 0.01)  # Vertical spacing between rows

    # Player area dimensions (positioned to fit 4 rows + name)
    # Calculate total height needed: name + 4 rows of cards
    total_cards_height = max_rows * card_height + (max_rows - 1) * card_spacing_y
    name_height = int(app_height * 0.06)
    total_player_height = name_height + total_cards_height + int(app_height * 0.02)

    # Position from bottom to fit everything
    player_y = app_height - total_player_height - int(app_height * 0.02)

    # Draw player name (font size scales with window)
    name_font_size = max(int(app_height * 0.045), 16)  # At least 16px
    font = pygame.font.Font(None, name_font_size)
    player_type = "👤 " if player.is_human else "🤖 "
    name_text = font.render(
        f"{player_type}{player.name}", ANTI_ALIASING, (255, 255, 255)
    )
    name_offset_x = int(app_height * 0.03)
    name_offset_y = int(app_height * 0.06)
    screen.blit(name_text, (x_position + name_offset_x, player_y - name_offset_y))

    # Draw each card in the player's hand (5 cards per row)
    card_border = max(int(card_height * 0.05), 2)  # Border scales with card size
    card_padding = max(int(card_height * 0.05), 2)  # Padding scales with card size

    for i, card in enumerate(player.hand.cards):
        # Calculate row and column for this card
        row = i // cards_per_row
        col = i % cards_per_row

        # Calculate card position
        card_x = x_position + name_offset_x + col * (card_width + card_spacing_x)
        card_y = player_y + row * (card_height + card_spacing_y)

        # Determine card color using global COLOR_MAP
        card_color = COLOR_MAP[card.color]

        # Draw card background
        pygame.draw.rect(
            screen, (255, 255, 255), (card_x, card_y, card_width, card_height)
        )
        pygame.draw.rect(
            screen,
            card_color,
            (
                card_x + card_padding,
                card_y + card_padding,
                card_width - 2 * card_padding,
                card_height - 2 * card_padding,
            ),
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (card_x, card_y, card_width, card_height), card_border
        )

        # Draw card number (font size scales with card size)
        number_font_size = max(int(card_height * 0.4), 16)  # At least 16px
        number_font = pygame.font.Font(None, number_font_size)
        number_text = number_font.render(
            str(card.number), ANTI_ALIASING, (255, 255, 255)
        )
        number_rect = number_text.get_rect(
            center=(card_x + card_width // 2, card_y + card_height // 2)
        )
        screen.blit(number_text, number_rect)


def run_event_loop(
    screen: pygame.Surface,
    game: Game,
    background: pygame.Surface,
    app_width: int,
    app_height: int,
) -> None:
    """Run the main event loop.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        background: The background image surface.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Draw background image
        screen.blit(background, (0, 0))

        # Display deck
        show_deck(screen, game.deck, app_width, app_height)

        # Display players
        show_players(screen, game, app_width, app_height)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


if __name__ == "__main__":
    main()
