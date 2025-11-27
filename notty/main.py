"""Main entrypoint for the project."""

import logging

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.dev.artifacts.resources import music
from notty.src.computer_action_selection import (
    computer_chooses_action,
    save_qlearning_agent,
)
from notty.src.consts import APP_HEIGHT, APP_NAME, APP_WIDTH
from notty.src.player_selection import get_players
from notty.src.visual.game import VisualGame
from notty.src.visual.player import VisualPlayer
from notty.src.visual.winner_display import WinnerDisplay


def main() -> None:
    """Start the notty game."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    pygame.init()
    start_background_music()

    try:
        # Main loop - allows restarting the game
        while True:
            result = run()

            # If user chose to quit, exit
            if result == "quit":
                break
            # If result is "new_game", loop continues and starts fresh

    finally:
        # Save Q-Learning agent before exiting
        save_qlearning_agent()
        pygame.quit()


def start_background_music() -> None:
    """Start looping background music if possible."""
    music_path = get_resource_path("music.mp3", music)

    pygame.mixer.init()
    pygame.mixer.music.load(str(music_path))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)  # # loop forever


def run() -> str:
    """Run the game.

    Returns:
        "new_game" if user wants to restart, "quit" if user wants to exit.
    """
    # Clear active players list to prevent positioning issues on restart
    VisualPlayer.ACTIVE_PLAYERS.clear()

    screen = get_screen()
    players = get_players(screen)
    game = VisualGame(screen, players)

    # Run the event loop and return the result
    return run_event_loop(game)


def get_screen() -> pygame.Surface:
    """Create the game window.

    Args:
        app_width: Width of the window.
        app_height: Height of the window.
    """
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    # set the title
    pygame.display.set_caption(APP_NAME)
    return screen


def run_event_loop(game: VisualGame) -> str:
    """Run the main event loop.

    Args:
        game: The game instance.

    Returns:
        "new_game" if user wants to start a new game, "quit" if user wants to quit.
    """
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if game.all_players_have_no_cards():
                VisualGame.distribute_starting_cards(game)
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                game.action_board.handle_click(mouse_x, mouse_y)
                continue

        computer_chooses_action(game)

        game.draw()

        # Check for winner
        if game.check_win_condition():
            # Draw one final time to show the winning state
            game.draw()
            pygame.display.flip()

            # Show winner and get user choice
            return show_winner(game)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


def show_winner(game: VisualGame) -> str:
    """Show the winner display and get user choice.

    Args:
        game: The game instance.

    Returns:
        "new_game" if user wants to start a new game, "quit" if user wants to quit.
    """
    if game.winner is None:
        return "quit"

    # Show winner display
    winner_display = WinnerDisplay(game.screen, game.winner)
    return winner_display.show()


if __name__ == "__main__":
    main()
