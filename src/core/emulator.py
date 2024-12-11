from typing import Optional, Union
import subprocess
import time
import socket
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmulatorError(Exception):
    """Base exception for emulator-related errors"""
    pass

class BizHawkEmulator:
    """Controls BizHawk emulator for Pokemon FireRed"""
    
    def __init__(
        self,
        bizhawk_path: Union[str, Path],
        rom_path: Union[str, Path],
        lua_path: Union[str, Path],
        save_state: Optional[Union[str, Path]] = None
    ):
        """
        Initialize BizHawk emulator controller
        
        Args:
            bizhawk_path: Path to BizHawk executable (EmuHawk.exe)
            rom_path: Path to Pokemon FireRed ROM
            lua_path: Path to Lua control script
            save_state: Optional path to savestate file
        """
        self.bizhawk_path = Path(bizhawk_path)
        self.rom_path = Path(rom_path)
        self.lua_path = Path(lua_path)
        self.save_state = Path(save_state) if save_state else None
        self.process = None
        
        # Set up socket configuration
        self.port = 65432  # Fixed port
        self.host = '127.0.0.1'
        
        # Create UDP socket for server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        logger.info(f"Socket bound to {self.host}:{self.port}")


        # Validate paths and initialize
        self._validate_paths()
        self._start_emulator()
        
    def _validate_paths(self) -> None:
        """Validate all required paths exist"""
        if not self.bizhawk_path.exists():
            raise FileNotFoundError(f"BizHawk executable not found at {self.bizhawk_path}")
        if not self.rom_path.exists():
            raise FileNotFoundError(f"ROM file not found at {self.rom_path}")
        if not self.lua_path.exists():
            raise FileNotFoundError(f"Lua script not found at {self.lua_path}")
        if self.save_state and not self.save_state.exists():
            raise FileNotFoundError(f"Save state file not found at {self.save_state}")
    
    def _start_emulator(self) -> None:
        """Start BizHawk with the ROM and Lua script"""
        try:
            cmd = [
                str(self.bizhawk_path),
                str(self.rom_path),
                "--lua=" + str(self.lua_path)
            ]
            
            logger.info("Starting BizHawk with command: %s", " ".join(cmd))
            self.process = subprocess.Popen(cmd)
            
            # Wait for Lua script to connect
            self.socket.settimeout(10.0)
            try:
                data, addr = self.socket.recvfrom(1024)
                if data.decode() == "ready":
                    logger.info("Lua script connected successfully")
                    self.socket.settimeout(1.0)  # Reset to shorter timeout for normal operation
            except socket.timeout:
                raise EmulatorError("Timeout waiting for Lua script connection")
            
            # Load save state if provided
            if self.save_state:
                self.load_state(self.save_state)
                
        except Exception as e:
            logger.error("Failed to start emulator: %s", str(e))
            self.close()
            raise
    
    def _send_command(self, command: str, wait_response: bool = True) -> Optional[str]:
        """Send command to Lua script and optionally wait for response"""
        try:
            self.socket.sendto(command.encode(), ('localhost', self.port))
            if wait_response:
                data, _ = self.socket.recvfrom(1024)
                return data.decode()
        except socket.timeout:
            logger.error("Timeout while sending command: %s", command)
            raise EmulatorError("Communication timeout with Lua script")
        except Exception as e:
            logger.error("Failed to send command: %s", str(e))
            raise EmulatorError("Failed to communicate with Lua script")
    
    def press_button(self, button: str, duration: float = 0.1) -> None:
        """
        Press a button for specified duration
        
        Args:
            button: Button to press (up, down, left, right, a, b, start, select)
            duration: How long to hold the button in seconds
        """
        try:
            self._send_command(f"press {button} {duration}", wait_response=False)
            time.sleep(duration + 0.05)  # Add small buffer for processing
        except Exception as e:
            logger.error("Failed to press button %s: %s", button, str(e))
            raise
    
    def load_state(self, state_path: Union[str, Path]) -> None:
        """Load a savestate file"""
        try:
            state_path = Path(state_path)
            if not state_path.exists():
                raise FileNotFoundError(f"Save state not found: {state_path}")
            
            response = self._send_command(f"loadstate {state_path}")
            if response != "ok":
                raise EmulatorError(f"Failed to load state: {response}")
            
            logger.info("Successfully loaded save state: %s", state_path)
            
        except Exception as e:
            logger.error("Failed to load save state: %s", str(e))
            raise
    
    def get_screen(self) -> bytes:
        """Get current screen content as bytes"""
        try:
            response = self._send_command("screen")
            return response.encode()  # You'll need to implement proper image handling
        except Exception as e:
            logger.error("Failed to get screen content: %s", str(e))
            raise
    
    def close(self) -> None:
        """Clean up resources and close emulator"""
        try:
            if self.socket:
                try:
                    self._send_command("exit", wait_response=False)
                except:
                    pass
                self.socket.close()
            
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5.0)
            
            logger.info("Emulator closed successfully")
            
        except Exception as e:
            logger.error("Error while closing emulator: %s", str(e))
            raise
        finally:
            self.process = None
            self.socket = None