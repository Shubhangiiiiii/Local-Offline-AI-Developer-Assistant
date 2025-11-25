import os
import json
from pathlib import Path


class FileOperations:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.project_root = Path(self.config['project_root']).resolve()
        self.excluded_dirs = set(self.config['excluded_dirs'])
        self.allowed_extensions = set(
            ext.lower() for ext in self.config['allowed_extensions']
        )

    def is_valid_path(self, path: Path) -> bool:
        """Check if a path should be processed (Windows friendly)."""
        try:
            path_str = str(path).lower()

            for excluded in self.excluded_dirs:
                if excluded.lower() in path_str:
                    return False

            if path.suffix.lower() not in self.allowed_extensions:
                return False

            return True

        except Exception:
            return False

    def read_file(self, file_path: str) -> dict:
        """Read file content with Windows-safe path handling."""
        try:
            file_path = file_path.replace('/', os.sep).replace('\\', os.sep)
            path = Path(file_path)

            if not path.is_absolute():
                path = self.project_root / path

            if not path.exists():
                return {"error": f"File not found: {file_path}"}

            if not path.is_file():
                return {"error": f"Not a file: {file_path}"}

            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            return {
                "path": str(path),
                "content": content,
                "lines": len(content.splitlines()),
                "size": len(content)
            }

        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}

    def list_files(self, directory: str = ".", recursive: bool = True) -> dict:
        """List all files in a directory (Windows friendly)."""
        try:
            directory = directory.replace('/', os.sep).replace('\\', os.sep)
            dir_path = Path(directory)

            if not dir_path.is_absolute():
                dir_path = self.project_root / dir_path

            if not dir_path.exists():
                return {"error": f"Directory not found: {directory}"}

            files = []

            if recursive:
                for path in dir_path.rglob('*'):
                    if path.is_file() and self.is_valid_path(path):
                        try:
                            rel_path = path.relative_to(self.project_root)
                            files.append(str(rel_path))
                        except ValueError:
                            files.append(str(path))
            else:
                for path in dir_path.iterdir():
                    if path.is_file() and self.is_valid_path(path):
                        try:
                            rel_path = path.relative_to(self.project_root)
                            files.append(str(rel_path))
                        except ValueError:
                            files.append(str(path))

            return {
                "directory": str(dir_path),
                "files": sorted(files),
                "count": len(files)
            }

        except Exception as e:
            return {"error": f"Error listing files: {str(e)}"}

    def get_file_info(self, file_path: str) -> dict:
        """Get metadata about a file."""
        try:
            file_path = file_path.replace('/', os.sep).replace('\\', os.sep)
            path = Path(file_path)

            if not path.is_absolute():
                path = self.project_root / path

            if not path.exists():
                return {"error": f"File not found: {file_path}"}

            stat = path.stat()

            return {
                "path": str(path),
                "name": path.name,
                "extension": path.suffix,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "modified": stat.st_mtime
            }

        except Exception as e:
            return {"error": f"Error getting file info: {str(e)}"}


# Test
if __name__ == "__main__":
    print("Testing File Operations...")
    ops = FileOperations()

    result = ops.list_files(".")
    if "error" in result:
        print("Error:", result["error"])
    else:
        print(f"✓ Found {result['count']} files")
