#!/usr/bin/env python3
"""Basic control test for BizHawk emulator."""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
import logging

from src.core.emulator import BizHawkEmulator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_project_root() -> Path:
    """Find the project root directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.env').exists():
            return current
        current = current.parent
    raise FileNotFoundError("Could not find project root (no .env file found)")

def test_basic_control():
    """Test basic emulator controls and save state loading."""
    try:
        # Load environment configuration
        project_root = find_project_root()
        load_dotenv(project_root / '.env')
        
        # Get paths
        bizhawk_path = os.getenv("BIZHAWK_PATH")
        rom_path = os.getenv("ROM_PATH")
        lua_path = os.getenv("LUA_PATH")
        save_state = project_root / "logs" / "saveStates" / "TEST_SAVE.mGBA.QuickSave0.State"

        logger.info("Starting emulator test...")
        logger.info(f"ROM Path: {rom_path}")
        logger.info(f"Save State: {save_state}")

        # Initialize emulator
        emulator = BizHawkEmulator(bizhawk_path, rom_path, lua_path, save_state)

        # Wait for everything to load
        logger.info("Waiting for game to load...")
        time.sleep(3)

        # Test movement sequence
        movements = [
            ("up", 0.5),
            ("right", 0.5),
            ("down", 0.5),
            ("left", 0.5)
        ]

        logger.info("Testing movement controls...")
        for direction, duration in movements:
            logger.info(f"Moving {direction} for {duration} seconds")
            emulator.press_button(direction, duration)
            time.sleep(0.3)  # Brief pause between movements

        logger.info("Movement test completed.")
        
        # Keep window open briefly to observe results
        time.sleep(2)

    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    finally:
        if 'emulator' in locals():
            emulator.close()
            logger.info("Emulator closed.")

if __name__ == "__main__":
    test_basic_control()