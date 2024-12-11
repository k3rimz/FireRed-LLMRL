from setuptools import setup, find_packages

setup(
    name="pokemon_rl",
    version="0.1",
    packages=find_packages(where="src"),  # Look for packages in src directory
    package_dir={"": "src"},  # Tell setuptools packages are under src
    install_requires=[
        'numpy',
        'opencv-python',
        'pillow',
        'python-dotenv',
        'mss',
        'pywin32',
        'torch',
        'torchvision',
        'transformers',
        'ultralytics',
        'open_clip_torch',
        'pyautogui',
    ],
    python_requires='>=3.10',
)