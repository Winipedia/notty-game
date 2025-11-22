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

# ---------------------------------------------------------
# MAIN EXECUTION FLOW (Added by Hanmiao for UI Assessment)
# ---------------------------------------------------------

def main():
    # 1. 初始化 / Initialize Pygame
    pygame.init()
    
    # 2. 设置窗口 / Setup Window
    app_width = 1200
    app_height = 800
    screen = pygame.display.set_mode((app_width, app_height))
    pygame.display.set_caption("Notty Game - Dev Build")

    # 3. 显示主菜单 / Show Main Menu
    # 调用前面定义的UI函数
    try:
        choice = show_main_menu(screen, app_width, app_height)
    except NameError:
        print("Menu function missing, defaulting to start.")
        choice = "start"

    # 4. 处理菜单选择 / Handle Selection
    if choice is None:
        pygame.quit()
        sys.exit(0)
        
    elif choice == "tutorial":
        print("Starting Tutorial Mode...")
        run_tutorial_placeholder(screen, app_width, app_height)
        # 教程结束后继续游戏，或者可以直接退出
        
    # 5. 进入核心游戏逻辑 / Enter Core Gameplay
    # (Existing logic by teammates)
    print("Initializing Core Game...")
    game = init_game()
    background = load_background(app_width, app_height)
    simulate_first_shuffle_and_deal(screen, game, background, app_width, app_height)
    run_event_loop(screen, game, background, app_width, app_height)


# ---------------------------------------------------------
# UI & MENU FUNCTIONS (Added by Hanmiao for UI Assessment)
# ---------------------------------------------------------

def show_main_menu(screen, app_width, app_height):
    """
    Displays the graphical main menu.
    Features:
    - Loads external assets via pathlib for cross-platform compatibility.
    - Distinct visual style with promo art.
    - Interactive buttons for Start/Tutorial.
    """
    import pygame
    import sys
    from pathlib import Path

    clock = pygame.time.Clock()

    # --- 资源加载 / Asset Loading ---
    # 使用 pathlib 确保路径兼容性，定位到 dev/artifacts/.../sprites
    # Ensure correct path to assets regardless of OS or execution directory
    current_dir = Path(__file__).resolve().parent
    promo_path = current_dir / "dev" / "artifacts" / "resources" / "sprites" / "notty_promo.png"

    try:
        # 尝试加载图片，如果失败则使用紫色占位块
        # Try to load the image; fallback to a colored block if missing
        if not promo_path.exists():
            print(f"Warning: Promo image not found at {promo_path}")
            raise FileNotFoundError("Asset missing")
            
        promo_img = pygame.image.load(str(promo_path)).convert_alpha()
    except Exception as e:
        # 容错处理 / Error Handling
        print(f"UI Asset Error: {e}. Using placeholder.")
        promo_img = pygame.Surface((int(app_width*0.6)-40, int(app_height*0.8)))
        promo_img.fill((200, 180, 230))

    # --- 字体与布局 / Fonts & Layout ---
    font = pygame.font.SysFont("arial", 26, bold=True)
    title_font = pygame.font.SysFont("arial", 40, bold=True)

    left_w = int(app_width * 0.62)
    right_w = app_width - left_w
    padding = 24
    btn_w = right_w - padding*2
    btn_h = 64
    btn_x = left_w + padding
    total_btns_h = 4 * btn_h + 3 * 12
    start_y = (app_height - total_btns_h) // 2

    # 按钮定义 / Button Definitions
    labels = [("Start Game", "start"),
              ("Tutorial", "tutorial"),
              ("Settings", "settings"),
              ("Quit", "quit")]
    btn_rects = []
    for i, (lbl, key) in enumerate(labels):
        rect = pygame.Rect(btn_x, start_y + i*(btn_h+12), btn_w, btn_h)
        btn_rects.append((rect, lbl, key))

    # --- 事件循环 / Event Loop ---
    running = True
    result = None
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                mx, my = e.pos
                for rect, lbl, key in btn_rects:
                    if rect.collidepoint((mx, my)):
                        if key == "quit":
                            pygame.quit()
                            sys.exit(0)
                        result = key
                        running = False

        # 绘制背景 / Draw Background
        screen.fill((20,20,28))

        # 绘制左侧宣传图 (自动缩放) / Draw Promo Image
        promo_w = left_w - 40
        promo_h = app_height - 120
        scaled = pygame.transform.smoothscale(promo_img, (promo_w, promo_h))
        screen.blit(scaled, (20, 60))

        # 绘制右侧面板 / Draw Right Panel
        right_rect = pygame.Rect(left_w, 0, right_w, app_height)
        pygame.draw.rect(screen, (12, 12, 18), right_rect)

        # 绘制标题 / Draw Title
        title_s = title_font.render("Notty Game", True, (230,230,230))
        screen.blit(title_s, (left_w + 24, 24))

        # 绘制按钮与悬停效果 / Draw Buttons & Hover
        for rect, lbl, key in btn_rects:
            mx, my = pygame.mouse.get_pos()
            hover = rect.collidepoint((mx, my))
            bg = (70,90,120) if not hover else (90,110,140)
            pygame.draw.rect(screen, bg, rect, border_radius=8)
            txt = font.render(lbl, True, (255,255,255))
            screen.blit(txt, txt.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(60)

    return result


def run_tutorial_placeholder(screen, app_width, app_height):
    """
    Runs the Tutorial Scene.
    Currently displays the character sprite (Notty) and introduction text.
    Designed to be expanded with the full storyboard script.
    """
    import pygame
    from pathlib import Path
    
    clock = pygame.time.Clock()
    
    # --- 教程立绘加载 / Load Character Sprite ---
    current_dir = Path(__file__).resolve().parent
    # 优先加载小写文件名，兼容性更好
    sprite_path = current_dir / "dev" / "artifacts" / "resources" / "sprites" / "nottystandard.png"
    
    try:
        # 检查文件是否存在，如果不存在尝试大写变体 (Keep fallback for safety)
        if not sprite_path.exists():
            alt_path = current_dir / "dev" / "artifacts" / "resources" / "sprites" / "NottyStandard.png"
            if alt_path.exists():
                sprite_path = alt_path
            else:
                print(f"Warning: Sprite not found at {sprite_path}")

        notty_img = pygame.image.load(str(sprite_path)).convert_alpha()
    except Exception as e:
        # 失败时显示占位符，防止游戏崩溃
        print(f"Tutorial Asset Error: {e}")
        notty_img = pygame.Surface((300,400))
        notty_img.fill((220,200,220))

    font = pygame.font.SysFont("arial", 28, bold=True)
    btn_rect = pygame.Rect(app_width//2 - 120, app_height - 140, 240, 64)

    showing = True
    while showing:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return False
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if btn_rect.collidepoint(e.pos):
                    showing = False  # End tutorial

        screen.fill((25,25,30))
        
        # 绘制立绘 / Draw Sprite
        if notty_img:
            n_w = int(app_width * 0.35)
            img_w = notty_img.get_width() if notty_img.get_width() > 0 else 1
            n_h = int(n_w * (notty_img.get_height() / img_w))
            scaled = pygame.transform.smoothscale(notty_img, (n_w, n_h))
            screen.blit(scaled, (40, app_height//2 - n_h//2))

        # 绘制对话框 / Draw Text Box
        text = "Hello! This is the tutorial placeholder. Click Begin Battle to start the tutorial battle."
        wrapped = []
        words = text.split(" ")
        line = ""
        for w in words:
            if len(line + " " + w) > 50:
                wrapped.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        wrapped.append(line)

        tx = app_width//2
        ty = 120
        for i, ln in enumerate(wrapped):
            txt_s = font.render(ln, True, (230,230,230))
            screen.blit(txt_s, (tx, ty + i*34))

        # 绘制按钮 / Draw Button
        pygame.draw.rect(screen, (70,90,120), btn_rect, border_radius=8)
        txt_s = font.render("Begin Battle", True, (255,255,255))
        screen.blit(txt_s, txt_s.get_rect(center=btn_rect.center))

        pygame.display.flip()
        clock.tick(60)
    return True


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

        # show actions to take in top right
        show_actions(screen, game, app_width, app_height)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


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
    display_order = get_player_display_order(game)
    num_players = len(display_order)

    for card_num in range(cards_per_player):
        for player_idx in range(num_players):
            # Animate card moving from deck to player
            deal_frames = 15

            # Calculate player position (using display order)
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


def get_player_display_order(game: Game) -> list[Player]:
    """Get the display order of players with human in the right.

    Args:
        game: The game instance.

    Returns:
        List of players in display order (left to right).
    """
    # Separate human and computer players
    all_players = game.players
    human_player = next(p for p in all_players if p.is_human)
    display_order = [p for p in all_players if p != human_player]

    display_order.append(human_player)

    return display_order


def show_players(
    screen: pygame.Surface, game: Game, app_width: int, app_height: int
) -> None:
    """Display all players with human player in the middle.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        app_width: Width of the window.
        app_height: Height of the window.
    """
    # Get display order with human in the middle
    display_order = get_player_display_order(game)

    # Position players horizontally across the bottom of the screen
    num_players = len(game.players)
    player_width = app_width // num_players

    for i, player in enumerate(display_order):
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


def show_actions(
    screen: pygame.Surface, game: Game, app_width: int, app_height: int
) -> None:
    """Display the actions that can be taken.

    Args:
        screen: The pygame display surface.
        game: The game instance.
        app_width: Width of the window.
        app_height: Height of the window.
    """


if __name__ == "__main__":
    main()
