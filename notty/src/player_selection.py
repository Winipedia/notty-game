"""Player selection screen and player setup."""

import pygame

from notty.src.visual.player import VisualPlayer
from notty.src.visual.player_name_selector import PlayerNameSelector


def get_players(screen: pygame.Surface) -> list[VisualPlayer]:
    """Get the players with a selection screen to choose who you are."""
    # Show selection screen to choose yourself
    selected_player = show_player_selection_screen(screen)

    # Show opponent selection screen
    opponent_names = show_opponent_selection_screen(screen, selected_player)

    # Create all players
    players_list: list[VisualPlayer] = []

    # Add human player
    players_list.append(VisualPlayer(selected_player, is_human=True, screen=screen))

    players_list.extend(
        VisualPlayer(name, is_human=False, screen=screen) for name in opponent_names
    )

    return players_list


def show_player_selection_screen(screen: pygame.Surface) -> str:
    """Show a screen to select which player you want to be.

    Args:
        screen: The pygame display surface.

    Returns:
        The name of the selected player.
    """
    all_names = VisualPlayer.get_all_player_names()
    selector = PlayerNameSelector(
        screen=screen,
        available_names=all_names,
        title="Choose Your Player",
        max_selections=1,
        min_selections=1,
    )
    result = selector.show()
    # Return single string (not list)
    return result if isinstance(result, str) else result[0]


def show_opponent_selection_screen(
    screen: pygame.Surface, human_player: str
) -> list[str]:
    """Show a screen to select 1-2 opponents.

    Args:
        screen: The pygame display surface.
        human_player: The name of the human player to exclude.

    Returns:
        List of selected opponent names.
    """
    all_names = VisualPlayer.get_all_player_names()
    available_names = [name for name in all_names if name != human_player]

    selector = PlayerNameSelector(
        screen=screen,
        available_names=available_names,
        title="Choose Opponents (1-2)",
        max_selections=2,
        min_selections=1,
    )
    result = selector.show()
    # Return list of strings
    return result if isinstance(result, list) else [result]
