import os
import fnmatch
from typing import List, Set
import json
from pathlib import Path

class ProjectExporter:
    def __init__(self, config_file: str = 'export_config.json'):
        self.config_file = config_file
        self.default_config = {
            "exclude_patterns": [
                "*/__pycache__/*",
                "*.pyc",
                "*.pyo",
                "*.pyd",
                ".git/*",
                ".env",
                ".env.template",
                "*.exe",
                "*.gba",
                "logs/*",
                "*.egg-info/*",
                ".pytest_cache/*",
                ".coverage",
                "__pycache__",
                "*.log",
                "export_script.py",
                "project_files.txt"
            ],
            "exclude_dirs": [
                "BizHawk",
                "logs",
                "pokemon_rl.egg-info"
            ],
            "exclude_files": [
                ".env.template",
                "export_script.py",
                "project_files.txt",
                "Pokemon - Fire Red Version (U) (V1.1).gba",
                "visualboyadvance-m.exe"
            ],
            "output_file": "project_files.txt",
            "delimiter": "# <FILE_DELIMITER> #"
        }
        self.config = self.load_config()

    def load_config(self) -> dict:
        """Load configuration from file or create default if it doesn't exist."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {self.config_file}, using default configuration")
                return self.default_config
        else:
            # Save default config
            with open(self.config_file, 'w') as f:
                json.dump(self.default_config, f, indent=4, sort_keys=True)
            return self.default_config

    def should_exclude(self, path: str) -> bool:
        """Check if a path should be excluded based on patterns and explicit exclusions."""
        rel_path = os.path.relpath(path, '.')
        
        # Check explicit directory exclusions
        for exclude_dir in self.config["exclude_dirs"]:
            if rel_path.startswith(exclude_dir):
                return True

        # Check explicit file exclusions
        if rel_path in self.config["exclude_files"]:
            return True

        # Check pattern-based exclusions
        for pattern in self.config["exclude_patterns"]:
            if fnmatch.fnmatch(rel_path, pattern):
                return True

        return False

    def save_file_content(self, file_path: str, output_file) -> None:
        """Save file content with proper encoding handling."""
        encodings = ['utf-8-sig', 'utf-8', 'latin-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as source_file:
                    content = source_file.read()
                    output_file.write(content)
                    output_file.write('\n')
                return
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error reading {file_path}: {str(e)}")
                return
        
        print(f"Could not decode file: {file_path}")

    def export_project(self) -> None:
        """Export project files according to configuration."""
        with open(self.config["output_file"], 'w', encoding='utf-8-sig') as f:
            for root, dirs, files in os.walk('.', topdown=True):
                # Filter directories in-place
                dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
                
                # Process files
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.should_exclude(file_path):
                        rel_path = os.path.relpath(file_path, '.')
                        f.write(f'{self.config["delimiter"]}\n{rel_path}\n\n')
                        self.save_file_content(file_path, f)

        print(f'Project files saved to {self.config["output_file"]}')

    def update_config(self, new_config: dict) -> None:
        """Update configuration with new values."""
        self.config.update(new_config)
        with open(self.config_file, 'w') as f:
            json.dump(self.default_config, f, indent=4, sort_keys=True)

def main():
    exporter = ProjectExporter()
    exporter.export_project()

if __name__ == "__main__":
    main()