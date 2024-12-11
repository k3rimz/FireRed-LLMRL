from PIL import Image, ImageDraw
import logging
import os

def tile_screenshots(screenshot_path, output_dir):
    """
    Creates individual screenshots of each tile in the given screenshot,
    with a red box highlighting the tile and an enlarged cropped section.
    Handles a game overworld that is 10.5 tiles tall by 15 tiles wide,
    where the bottom row is half-height.

    Args:
        screenshot_path: Path to the screenshot image.
        output_dir: Directory to save the individual tile screenshots.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('tile_screenshots.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    try:
        logger.debug("Checking if screenshot path exists: %s", screenshot_path)
        if not os.path.exists(screenshot_path):
            logger.error(f"Screenshot path not found: {screenshot_path}")
            return

        logger.debug("Loading screenshot image: %s", screenshot_path)
        img = Image.open(screenshot_path)
        width, height = img.size
        logger.debug("Image dimensions: %s x %s", width, height)

        # Calculate tile dimensions based on 15 columns and 10.5 rows
        # (9 full-height rows + 2 half-height rows at top and bottom)
        tile_width = width // 15
        total_tile_height = height / 10  # Height for middle rows (9 full rows + 1 total for both half rows)
        full_tile_height = int(total_tile_height)  # Full tiles in the middle
        half_tile_height = int(total_tile_height / 2)  # Half tiles for top and bottom
        logger.debug("Tile dimensions - Width: %s, Full Height: %s, Half Height: %s", 
                    tile_width, full_tile_height, half_tile_height)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.debug("Created output directory: %s", output_dir)

        # Process all rows (11 rows total, with the last one being half-height)
        for i in range(11):
            logger.debug("Processing row: %d", i)
            is_half_height = (i == 0 or i == 10)  # Check if it's top or bottom row
            current_tile_height = half_tile_height if is_half_height else full_tile_height

            for j in range(15):
                logger.debug("Processing tile: (%d, %d)", i, j)

                # Create a new image with space for the enlarged tile
                new_width = width + tile_width * 2
                tile_img = Image.new('RGB', (new_width, height), (255, 255, 255))
                tile_img.paste(img, (0, 0))

                # Calculate tile coordinates
                x1 = j * tile_width
                # Special handling for top row (half height), middle rows (full height), and bottom row (half height)
                if i == 0:  # Top row
                    y1 = 0
                    current_tile_height = half_tile_height
                elif i == 10:  # Bottom row
                    y1 = height - half_tile_height
                    current_tile_height = half_tile_height
                else:  # Middle rows (1-9)
                    y1 = half_tile_height + (i - 1) * full_tile_height
                    current_tile_height = full_tile_height
                    
                x2 = x1 + tile_width
                y2 = y1 + current_tile_height

                logger.debug("Tile coordinates: (%d, %d) - (%d, %d)", x1, y1, x2, y2)

                # Draw a red box around the tile
                draw = ImageDraw.Draw(tile_img)
                draw.rectangle([(x1 - 2, y1 - 2), (x2 + 2, y2 + 2)], outline=(255, 0, 0), width=2)

                try:
                    # Extract and enlarge the tile
                    cropped_tile = img.crop((x1, y1, x2, y2))
                    # For top/bottom rows, double the width but maintain half-height aspect ratio
                    if is_half_height:
                        enlarged_height = half_tile_height * 2
                    else:
                        enlarged_height = full_tile_height * 2
                    cropped_tile = cropped_tile.resize((tile_width * 2, enlarged_height))
                except Exception as e:
                    logger.error(f"Error cropping/resizing tile ({i}, {j}): {e}")
                    continue

                try:
                    # Paste the enlarged tile onto the right side
                    # Center it vertically
                    paste_y = (height - enlarged_height) // 2
                    tile_img.paste(cropped_tile, (width, paste_y))
                except Exception as e:
                    logger.error(f"Error pasting tile ({i}, {j}): {e}")
                    continue

                # Save the tile image
                try:
                    tile_img.save(f"{output_dir}/tile_{i}_{j}.png")
                    logger.debug("Saved tile image: %s", f"{output_dir}/tile_{i}_{j}.png")
                except Exception as e:
                    logger.error(f"Error saving tile image ({i}, {j}): {e}")
                    continue

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Example usage
screenshot_path = "sc_fr1.png"  # Replace with the actual path to your screenshot
output_dir = "tile_screenshots"  # Directory to save the individual tile screenshots

tile_screenshots(screenshot_path, output_dir)