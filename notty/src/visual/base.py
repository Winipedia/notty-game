"""Contains a base clöass Visual to represent a visual element."""

from abc import ABC, abstractmethod
from pathlib import Path
from types import ModuleType

import pygame
from pyrig.dev.artifacts.resources.resource import get_resource_path

from notty.src.consts import ANIMATION_SPEED


class Visual(ABC):
    """Base class for all visual elements."""

    def __init__(
        self,
        x: int,
        y: int,
        height: int,
        width: int,
        screen: pygame.Surface,
    ) -> None:
        """Initialize a visual element.

        Args:
            x: X coordinate. Always represents the top-left corner.
            y: Y coordinate. Always represents the top-left corner.
            height: Height of the visual element.
            width: Width of the visual element.
            screen: The pygame display surface.
        """
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.height = height
        self.width = width
        self.screen = screen

        png = pygame.image.load(self.get_png_path())
        self.png = pygame.transform.scale(png, (self.width, self.height))

    def get_center(self) -> tuple[int, int]:
        """Get the center of the visual element."""
        return self.x + self.width // 2, self.y + self.height // 2

    def move(self, x: int, y: int) -> None:
        """Move the visual element.

        Animates the movement in a straight line to that given location.

        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self.target_x = x
        self.target_y = y

    def set_position(self, x: int, y: int) -> None:
        """Set the position of the visual element.

        Args:
            x: X coordinate.
            y: Y coordinate.
        """
        self.x = x
        self.y = y

    def draw(self) -> None:
        """Draw the visual element.

        Args:
            screen: The pygame display surface.
        """
        # Smoothly move toward target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance > ANIMATION_SPEED:
            # Move toward target at constant speed
            self.x += (dx / distance) * ANIMATION_SPEED
            self.y += (dy / distance) * ANIMATION_SPEED
        else:
            # Snap to target when close enough
            self.x = self.target_x
            self.y = self.target_y

        # Draw the image at current position
        self.screen.blit(self.png, (self.x, self.y))

    def get_png_path(self) -> Path:
        """Get the png for the visual element."""
        return get_resource_path(self.get_png_name() + ".png", self.get_png_pkg())

    @abstractmethod
    def get_png_name(self) -> str:
        """Get the png for the visual element."""

    @abstractmethod
    def get_png_pkg(self) -> ModuleType:
        """Get the png for the visual element."""
