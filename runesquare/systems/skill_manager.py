import math
from typing import Dict

class Skill:
    """Represents a single player skill."""
    def __init__(self, name: str, current_xp: int = 0) -> None:
        self.name: str = name
        self.current_xp: int = current_xp

    @staticmethod
    def runescape_xp_for_level(level: int) -> int:
        xp = 0
        for k in range(1, level):
            xp += int((k + 300 * 2 ** (k / 7.0)) / 4)
        return xp

    @staticmethod
    def runescape_level_for_xp(xp: int) -> int:
        level = 1
        while Skill.runescape_xp_for_level(level + 1) <= xp:
            level += 1
        return level

    @property
    def level(self) -> int:
        # Use RuneScape XP formula for level calculation
        return self.runescape_level_for_xp(self.current_xp)

    def add_xp(self, amount: int) -> bool:
        """Adds XP and returns True if the level increased."""
        if amount < 0:
            raise ValueError("Experience amount cannot be negative.")
        old_level = self.level
        self.current_xp += amount
        return self.level > old_level

class SkillManager:
    """Manages all player skills."""
    def __init__(self) -> None:
        # Initialize with core skills. More can be added here or loaded.
        self.skills: Dict[str, Skill] = {
            "Woodcutting": Skill("Woodcutting"),
            # Add other core skills here later, e.g., "Mining": Skill("Mining"),
        }

    def add_xp_to_skill(self, skill_name: str, amount: int) -> bool:
        """Adds XP to a specific skill by name."""
        skill = self.skills.get(skill_name)
        if skill is None:
            # Raise an error if the skill doesn't exist, as per error handling rules
            raise ValueError(f"Attempted to add XP to non-existent skill: {skill_name}")
        return skill.add_xp(amount)

    def get_skill_level(self, skill_name: str) -> int:
        """Gets the current level of a skill by name."""
        skill = self.skills.get(skill_name)
        if skill is None:
            raise ValueError(f"Attempted to get level for non-existent skill: {skill_name}")
        return skill.level

    def get_skill_xp(self, skill_name: str) -> int:
        """Gets the current XP of a skill by name."""
        skill = self.skills.get(skill_name)
        if skill is None:
            raise ValueError(f"Attempted to get XP for non-existent skill: {skill_name}")
        return skill.current_xp

    def get_all_skills(self) -> Dict[str, Skill]:
        """Returns a dictionary of all skills."""
        return self.skills

    def to_dict(self) -> dict:
        """Serialize all skills to a dict of {skill_name: current_xp}."""
        return {name: skill.current_xp for name, skill in self.skills.items()}

    def from_dict(self, data: dict) -> None:
        """Restore skills from a dict of {skill_name: current_xp}."""
        for name, xp in data.items():
            if name in self.skills:
                self.skills[name].current_xp = xp
            else:
                self.skills[name] = Skill(name, xp)

    def total_experience(self) -> int:
        """Return the sum of all experience points across all skills."""
        return sum(skill.current_xp for skill in self.skills.values())

    def total_level(self) -> int:
        """Return the sum of all skill levels across all skills."""
        return sum(skill.level for skill in self.skills.values())
