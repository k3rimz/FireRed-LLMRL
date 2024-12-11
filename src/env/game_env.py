"""Pokemon FireRed environment for reinforcement learning."""
from typing import Tuple, Dict, Any, Optional
import numpy as np
import gymnasium as gym
from gymnasium import spaces
import logging
from pathlib import Path

from ..core.emulator import BizHawkEmulator
from ..core.state_manager import StateManager, GameState
from ..core.image_utils import ImageProcessor

logger = logging.getLogger(__name__)

class PokemonFireRedEnv(gym.Env):
    """OpenAI Gym environment for Pokemon FireRed."""
    
    metadata = {'render_modes': ['rgb_array']}
    
    # Action space mapping
    ACTIONS = {
        0: 'up',
        1: 'down',
        2: 'left',
        3: 'right',
        4: 'a',
        5: 'b',
        6: 'start',
        7: 'select'
    }
    
    def __init__(
        self,
        bizhawk_path: Path,
        rom_path: Path,
        lua_path: Path,
        save_state: Optional[Path] = None
    ):
        """
        Initialize Pokemon FireRed environment.
        
        Args:
            bizhawk_path: Path to BizHawk executable
            rom_path: Path to Pokemon FireRed ROM
            lua_path: Path to Lua control script
            save_state: Optional path to starting save state
        """
        super().__init__()
        
        # Initialize components
        self.emulator = BizHawkEmulator(bizhawk_path, rom_path, lua_path, save_state)
        self.state_manager = StateManager()
        self.image_processor = ImageProcessor()
        
        # Define action and observation spaces
        self.action_space = spaces.Discrete(len(self.ACTIONS))
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(160, 240, 3),  # GBA resolution, RGB
            dtype=np.uint8
        )
        
        # Environment state
        self.current_screen = None
        self.steps_taken = 0
        self.max_steps = 1000  # Configurable
        
    def reset(self, *, seed=None, options=None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Reset environment to initial state."""
        super().reset(seed=seed)
        
        # Reset internal state
        self.steps_taken = 0
        self.state_manager = StateManager()
        
        # Get initial observation
        self.current_screen = self._get_observation()
        
        return self.current_screen, {}
        
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take action in environment.
        
        Args:
            action: Integer action from action space
            
        Returns:
            observation: Game screen as numpy array
            reward: Reward for action
            terminated: Whether episode is done
            truncated: Whether episode was truncated
            info: Additional information
        """
        # Execute action
        if action in self.ACTIONS:
            self.emulator.press_button(self.ACTIONS[action])
        
        # Get new observation
        self.current_screen = self._get_observation()
        
        # Update state and get reward
        reward = self._calculate_reward()
        
        # Check if episode is done
        self.steps_taken += 1
        terminated = False  # Implement proper termination conditions
        truncated = self.steps_taken >= self.max_steps
        
        # Additional info
        info = {
            'steps': self.steps_taken,
            'state': self.state_manager.get_state_data()
        }
        
        return self.current_screen, reward, terminated, truncated, info
    
    def render(self):
        """Return current screen."""
        return self.current_screen
        
    def close(self):
        """Clean up environment."""
        if self.emulator:
            self.emulator.close()
    
    def _get_observation(self) -> np.ndarray:
        """Get current game screen."""
        screen_data = self.emulator.get_screen()
        screen = self.image_processor.decode_screenshot(screen_data)
        return self.image_processor.normalize_size(screen)
    
    def _calculate_reward(self) -> float:
        """Calculate reward based on current state."""
        # Implement reward calculation based on game events
        return 0.0  # Placeholder