"""Utilities for processing emulator screen captures."""
import numpy as np
import cv2
from PIL import Image
import io
import base64
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles processing and analysis of game screen images."""
    
    GBA_RESOLUTION = (240, 160)  # Native GBA resolution
    
    @staticmethod
    def decode_screenshot(screen_data: bytes) -> np.ndarray:
        """Convert raw screenshot data to numpy array."""
        try:
            # BizHawk provides PNG data
            image = Image.open(io.BytesIO(screen_data))
            # Convert to RGB numpy array
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            logger.error(f"Failed to decode screenshot: {e}")
            raise
    
    @staticmethod
    def normalize_size(image: np.ndarray) -> np.ndarray:
        """Ensure image is at GBA resolution."""
        if image.shape[:2] != ImageProcessor.GBA_RESOLUTION[::-1]:
            return cv2.resize(image, ImageProcessor.GBA_RESOLUTION)
        return image
    
    @staticmethod
    def to_base64(image: np.ndarray) -> str:
        """Convert image to base64 string."""
        try:
            success, buffer = cv2.imencode('.png', image)
            if not success:
                raise ValueError("Failed to encode image")
            return base64.b64encode(buffer).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to convert image to base64: {e}")
            raise
            
    @staticmethod
    def save_screenshot(image: np.ndarray, path: str) -> None:
        """Save screenshot to file."""
        try:
            cv2.imwrite(path, image)
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            raise
            
    @staticmethod
    def get_pixel_color(image: np.ndarray, x: int, y: int) -> Tuple[int, int, int]:
        """Get RGB color of pixel at (x,y)."""
        try:
            return tuple(image[y, x])  # OpenCV uses (y,x) indexing
        except IndexError:
            logger.error(f"Pixel coordinates ({x},{y}) out of bounds")
            raise