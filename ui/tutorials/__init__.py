"""
ui/tutorials
Modular, sandboxed, action-driven interactive tutorials for the Arbor desktop application.
"""

from .sandbox_manager import SandboxManager
from .tutorial_runner import TutorialRunner, ActionStep
from .review_tutorial import start_review_tutorial
from .triage_tutorial import start_triage_tutorial
from .discrepancy_tutorial import start_discrepancy_tutorial
from .database_tutorial import start_database_tutorial
from .micro_guides import (
    start_hallway_followup_guide,
    start_armed_shelf_guide,
    start_image_controls_guide,
)

__all__ = [
    "SandboxManager",
    "TutorialRunner",
    "ActionStep",
    "start_review_tutorial",
    "start_triage_tutorial",
    "start_discrepancy_tutorial",
    "start_database_tutorial",
    "start_hallway_followup_guide",
    "start_armed_shelf_guide",
    "start_image_controls_guide",
]
