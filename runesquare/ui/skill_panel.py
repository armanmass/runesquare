import pygame
from runesquare.systems.skill_manager import SkillManager
from typing import Tuple

class SkillPanel:
    def __init__(self, font: pygame.font.Font, position: Tuple[int, int] = (10, 10)) -> None:
        self.font = font
        self.position = position  # Top-left corner of the panel
        self.line_height = self.font.get_height() + 4

    def draw(self, surface: pygame.Surface, skill_manager: SkillManager) -> None:
        x, y = self.position
        # Draw total experience and total level at the top
        total_xp = skill_manager.total_experience()
        total_level = skill_manager.total_level()
        header_text = f"Total Level: {total_level}  Total XP: {total_xp}"
        header_surf = self.font.render(header_text, True, (255, 255, 0))

        surface.blit(header_surf, (x, y))
        y += self.line_height + 2
        for idx, (name, skill) in enumerate(skill_manager.get_all_skills().items()):
            text = f"{name} Lv: {skill.level} ({skill.current_xp} XP)"
            text_surf = self.font.render(text, True, (255, 255, 255))
            surface.blit(text_surf, (x, y + idx * self.line_height))
