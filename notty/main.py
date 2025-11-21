"""Main entrypoint for the project."""

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts import resources
from notty.src.card import Color
from notty.src.consts import ANTI_ALIASING, APP_HEIGHT, APP_NAME, APP_WIDTH
from notty.src.deck import Deck
from notty.src.game import Game
from notty.src.player import Player


def main() -> None:
    """Start the notty game."""
    pygame.init()

    run()

    pygame.quit()


def run() -> None:
    """Run the game."""
    screen = create_window()

    # initialize game
    game = init_game()

    # load background image
    background = load_background()

    # run the event loop
    run_event_loop(screen, game, background)


def create_window() -> pygame.Surface:
    """Create the game window."""
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    # set the title
    pygame.display.set_caption(APP_NAME)
    return screen


def load_background() -> pygame.Surface:
    """Load and scale the background image."""
    # Get the path to the icon.png file
    icon_path = get_resource_path("icon.png", resources)

    # Load the image
    background = pygame.image.load(icon_path)

    # Scale it to fit the window
    return pygame.transform.scale(background, (APP_WIDTH, APP_HEIGHT))


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


def show_deck(screen: pygame.Surface, deck: Deck) -> None:
    """Display the deck widget.

    Args:
        screen: The pygame display surface.
        deck: The deck to display.
    """
    # Deck position (top center of screen)
    deck_x = APP_WIDTH // 2 - 50
    deck_y = 50
    deck_width = 100
    deck_height = 140

    # Draw deck background (card back)
    pygame.draw.rect(screen, (200, 0, 0), (deck_x, deck_y, deck_width, deck_height))
    pygame.draw.rect(
        screen, (255, 255, 255), (deck_x, deck_y, deck_width, deck_height), 3
    )

    # Display card count
    font = pygame.font.Font(None, 32)
    count_text = font.render(str(deck.size()), ANTI_ALIASING, (255, 255, 255))
    text_rect = count_text.get_rect(
        center=(deck_x + deck_width // 2, deck_y + deck_height // 2)
    )
    screen.blit(count_text, text_rect)

    # Display "DECK" label
    label_font = pygame.font.Font(None, 24)
    label_text = label_font.render("DECK", ANTI_ALIASING, (255, 255, 255))
    label_rect = label_text.get_rect(
        center=(deck_x + deck_width // 2, deck_y + deck_height + 20)
    )
    screen.blit(label_text, label_rect)


def show_players(screen: pygame.Surface, game: Game) -> None:
    """Display all players.

    Args:
        screen: The pygame display surface.
        game: The game instance.
    """
    # Position players horizontally across the bottom of the screen
    num_players = len(game.players)
    player_width = APP_WIDTH // num_players

    for i, player in enumerate(game.players):
        player_x = i * player_width
        show_player_with_hand(screen, player, player_x)


def show_player_with_hand(
    screen: pygame.Surface, player: Player, x_position: int
) -> None:
    """Display a player with their hand.

    Args:
        screen: The pygame display surface.
        player: The player to display.
        x_position: The x position to start drawing the player area.
    """
    # Player area dimensions
    player_y = APP_HEIGHT - 300
    card_width = 70
    card_height = 100
    card_spacing = 10

    # Draw player name
    font = pygame.font.Font(None, 28)
    player_type = "👤 " if player.is_human else "🤖 "
    name_text = font.render(
        f"{player_type}{player.name}", ANTI_ALIASING, (255, 255, 255)
    )
    screen.blit(name_text, (x_position + 20, player_y - 40))

    # Draw each card in the player's hand
    for i, card in enumerate(player.hand.cards):
        card_x = x_position + 20 + i * (card_width + card_spacing)
        card_y = player_y

        # Determine card color
        color_map = {
            Color.RED: (220, 20, 60),
            Color.GREEN: (34, 139, 34),
            Color.YELLOW: (255, 215, 0),
            Color.BLACK: (50, 50, 50),
            Color.BLUE: (30, 144, 255),
        }
        card_color = color_map[card.color]

        # Draw card background
        pygame.draw.rect(
            screen, (255, 255, 255), (card_x, card_y, card_width, card_height)
        )
        pygame.draw.rect(
            screen,
            card_color,
            (card_x + 5, card_y + 5, card_width - 10, card_height - 10),
        )
        pygame.draw.rect(
            screen, (0, 0, 0), (card_x, card_y, card_width, card_height), 2
        )

        # Draw card number
        number_font = pygame.font.Font(None, 48)
        number_text = number_font.render(
            str(card.number), ANTI_ALIASING, (255, 255, 255)
        )
        number_rect = number_text.get_rect(
            center=(card_x + card_width // 2, card_y + card_height // 2)
        )
        screen.blit(number_text, number_rect)


def run_event_loop(
    screen: pygame.Surface, game: Game, background: pygame.Surface
) -> None:
    """Run the main event loop.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        background: The background image surface.
    """
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Draw background image
        screen.blit(background, (0, 0))

        # Display deck
        show_deck(screen, game.deck)

        # Display players
        show_players(screen, game)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


if __name__ == "__main__":
    main()
