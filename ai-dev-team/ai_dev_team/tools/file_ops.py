"""
File operation tools for AI agents
"""
from pathlib import Path
from typing import Optional
import os


class FileOperations:
    """Tools for file and directory operations"""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)

    def _resolve_path(self, filepath: str) -> Path:
        """Resolve and validate path within base directory"""
        path = (self.base_dir / filepath).resolve()
        # Security: ensure path is within base_dir
        if not str(path).startswith(str(self.base_dir.resolve())):
            raise ValueError(f"Access denied: {filepath} is outside workspace")
        return path

    def write_file(self, filepath: str, content: str) -> str:
        """
        Write content to a file

        Args:
            filepath: Relative path to file
            content: File content

        Returns:
            Success message
        """
        try:
            path = self._resolve_path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            size = len(content)
            lines = content.count("\n") + 1
            return f"✅ File written: {filepath} ({size} chars, {lines} lines)"

        except Exception as e:
            return f"❌ Error writing file: {str(e)}"

    def read_file(self, filepath: str) -> str:
        """
        Read content from a file

        Args:
            filepath: Relative path to file

        Returns:
            File content or error message
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return f"❌ File not found: {filepath}"

            if path.is_dir():
                return f"❌ {filepath} is a directory, not a file"

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            size = len(content)
            lines = content.count("\n") + 1
            return f"📄 File: {filepath} ({size} chars, {lines} lines)\n\n{content}"

        except UnicodeDecodeError:
            return f"❌ Cannot read {filepath} - binary file or incompatible encoding"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"

    def list_files(self, directory: str = ".") -> str:
        """
        List files and directories

        Args:
            directory: Relative path to directory

        Returns:
            Formatted list of files
        """
        try:
            path = self._resolve_path(directory)

            if not path.exists():
                return f"❌ Directory not found: {directory}"

            if not path.is_dir():
                return f"❌ {directory} is not a directory"

            items = []
            for item in sorted(path.iterdir()):
                rel_path = item.relative_to(self.base_dir)
                if item.is_dir():
                    items.append(f"📁 {rel_path}/")
                else:
                    size = item.stat().st_size
                    items.append(f"📄 {rel_path} ({size} bytes)")

            if not items:
                return f"📂 {directory}/ (empty)"

            return f"📂 {directory}/\n" + "\n".join(items)

        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"

    def create_directory(self, directory: str) -> str:
        """
        Create a directory

        Args:
            directory: Relative path to directory

        Returns:
            Success message
        """
        try:
            path = self._resolve_path(directory)
            path.mkdir(parents=True, exist_ok=True)
            return f"✅ Directory created: {directory}"

        except Exception as e:
            return f"❌ Error creating directory: {str(e)}"

    def delete_file(self, filepath: str) -> str:
        """
        Delete a file

        Args:
            filepath: Relative path to file

        Returns:
            Success message
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return f"❌ File not found: {filepath}"

            if path.is_dir():
                return f"❌ {filepath} is a directory. Use delete_directory instead"

            path.unlink()
            return f"✅ File deleted: {filepath}"

        except Exception as e:
            return f"❌ Error deleting file: {str(e)}"

    def search_in_file(self, filepath: str, pattern: str) -> str:
        """
        Search for pattern in file

        Args:
            filepath: Relative path to file
            pattern: Search pattern

        Returns:
            Matching lines with line numbers
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return f"❌ File not found: {filepath}"

            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            matches = []
            for i, line in enumerate(lines, 1):
                if pattern.lower() in line.lower():
                    matches.append(f"{i}: {line.rstrip()}")

            if not matches:
                return f"❌ No matches found for '{pattern}' in {filepath}"

            return f"🔍 Found {len(matches)} matches in {filepath}:\n" + "\n".join(matches)

        except Exception as e:
            return f"❌ Error searching file: {str(e)}"

    def get_file_info(self, filepath: str) -> str:
        """
        Get file information

        Args:
            filepath: Relative path to file

        Returns:
            File metadata
        """
        try:
            path = self._resolve_path(filepath)

            if not path.exists():
                return f"❌ File not found: {filepath}"

            stat = path.stat()

            info = [
                f"📄 File: {filepath}",
                f"Size: {stat.st_size} bytes",
                f"Type: {'Directory' if path.is_dir() else 'File'}",
                f"Modified: {stat.st_mtime}",
            ]

            if path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    lines = len(f.readlines())
                info.append(f"Lines: {lines}")

            return "\n".join(info)

        except Exception as e:
            return f"❌ Error getting file info: {str(e)}"
