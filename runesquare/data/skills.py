import math

class Skill:
    """Represents a player skill with XP and level progression."""

    def __init__(self, name: str, current_xp: int):
        """
        Initializes a new Skill instance.

        Args:
            name: The name of the skill.
            current_xp: The current experience points for the skill.
        """
        if current_xp < 0:
             raise ValueError("Initial experience amount cannot be negative.")
        self.name: str = name
        self.current_xp: int = current_xp

    @property
    def level(self) -> int:
        """Calculates the current level based on current_xp."""
        # Formula: level = floor(sqrt(xp / 100))
        # Ensure non-negative input to sqrt
        safe_xp = max(0, self.current_xp)
        return int(math.sqrt(safe_xp / 100))

    def add_xp(self, amount: int) -> bool:
        """
        Adds experience points to the skill.

        Args:
            amount: The amount of XP to add.

        Returns:
            True if the skill leveled up, False otherwise.
        """
        if amount < 0:
             raise ValueError("Experience amount cannot be negative.")

        old_level = self.level
        self.current_xp += amount
        return self.level > old_level

