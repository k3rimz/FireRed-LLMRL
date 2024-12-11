"""Manages game state tracking and transitions."""
from enum import Enum, auto
from typing import Optional, Dict, Any
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class GameState(Enum):
    """Possible game states."""
    UNKNOWN = auto()
    TITLE_SCREEN = auto()
    MAIN_MENU = auto()
    OVERWORLD = auto()
    BATTLE = auto()
    DIALOG = auto()
    MENU = auto()
    INVENTORY = auto()

class StateManager:
    """Tracks and manages game state."""
    
    def __init__(self):
        """Initialize state manager."""
        self.current_state = GameState.UNKNOWN
        self.previous_state = GameState.UNKNOWN
        self.state_data: Dict[str, Any] = {}
        
    def update_state(self, new_state: GameState, **kwargs) -> None:
        """
        Update current game state and associated data.
        
        Args:
            new_state: New game state
            **kwargs: Additional state-specific data
        """
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_data.update(kwargs)
        
        logger.info(f"State transition: {self.previous_state.name} -> {self.current_state.name}")
        
    def get_state_data(self) -> Dict[str, Any]:
        """Get current state data."""
        return {
            'current_state': self.current_state.name,
            'previous_state': self.previous_state.name,
            'data': self.state_data
        }
        
    def save_state(self, path: Path) -> None:
        """Save state data to file."""
        try:
            state_data = self.get_state_data()
            with open(path, 'w') as f:
                json.dump(state_data, f, indent=2)
            logger.info(f"Saved state data to {path}")
        except Exception as e:
            logger.error(f"Failed to save state data: {e}")
            raise
            
    def load_state(self, path: Path) -> None:
        """Load state data from file."""
        try:
            with open(path, 'r') as f:
                state_data = json.load(f)
            
            self.current_state = GameState[state_data['current_state']]
            self.previous_state = GameState[state_data['previous_state']]
            self.state_data = state_data['data']
            
            logger.info(f"Loaded state data from {path}")
        except Exception as e:
            logger.error(f"Failed to load state data: {e}")
            raise
            
    def is_in_state(self, state: GameState) -> bool:
        """Check if currently in specified state."""
        return self.current_state == state
        
    def has_transitioned(self) -> bool:
        """Check if state has changed since last update."""
        return self.current_state != self.previous_state