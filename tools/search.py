import re
from typing import List, Dict
from pathlib import Path


class CodeSearch:
    def __init__(self, file_ops):
        # file_ops is an instance of FileOperations
        self.file_ops = file_ops

    def search_in_file(self, file_path: str, query: str, case_sensitive: bool = False) -> List[Dict]:
        """Search for a query in a single file."""
        result = self.file_ops.read_file(file_path)

        if "error" in result:
            return []

        content = result["content"]
        lines = content.splitlines()

        matches = []
        flags = 0 if case_sensitive else re.IGNORECASE

        # Try to compile as regex; if it fails, escape and treat as literal
        try:
            pattern = re.compile(query, flags)
        except re.error:
            pattern = re.compile(re.escape(query), flags)

        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                matches.append(
                    {
                        "line": i,
                        "content": line.strip(),
                        "file": file_path,
                    }
                )

        return matches

    def search_code(self, query: str, directory: str = ".", case_sensitive: bool = False) -> Dict:
        """Search for a query across all valid files in the project."""
        files_result = self.file_ops.list_files(directory, recursive=True)

        if "error" in files_result:
            return {"error": files_result["error"]}

        all_matches = []
        files_with_matches = set()

        for file_path in files_result["files"]:
            matches = self.search_in_file(file_path, query, case_sensitive)
            if matches:
                all_matches.extend(matches)
                files_with_matches.add(file_path)

        return {
            "query": query,
            "total_matches": len(all_matches),
            "files_searched": files_result["count"],
            "files_with_matches": len(files_with_matches),
            "matches": all_matches[:100],  # limit to 100 results
        }

    def find_function(self, function_name: str, directory: str = ".") -> Dict:
        """Find function definitions by name in various languages."""
        patterns = [
            rf"\bdef\s+{function_name}\s*\(",  # Python
            rf"\bfunction\s+{function_name}\s*\(",  # JavaScript
            rf"\bconst\s+{function_name}\s*=",  # JS arrow function
            rf"\b{function_name}\s*:\s*function",  # JS object method
            rf"\b(public|private|protected|static)?\s*\w+\s+{function_name}\s*\(",  # Java/C#/C++
            rf"\bfunc\s+{function_name}\s*\(",  # Go
            rf"\bfn\s+{function_name}\s*\(",  # Rust
        ]

        all_matches = []

        for pattern in patterns:
            result = self.search_code(pattern, directory, case_sensitive=True)
            if "matches" in result:
                all_matches.extend(result["matches"])

        # Remove duplicates by (file, line)
        seen = set()
        unique_matches = []
        for match in all_matches:
            key = (match["file"], match["line"])
            if key not in seen:
                seen.add(key)
                unique_matches.append(match)

        return {
            "function": function_name,
            "total_matches": len(unique_matches),
            "matches": unique_matches,
        }

    def find_class(self, class_name: str, directory: str = ".") -> Dict:
        """Find class or type definitions by name."""
        patterns = [
            rf"\bclass\s+{class_name}\s*[:\(]",  # Python, Java, C++, C#
            rf"\binterface\s+{class_name}\b",  # TypeScript/Java
            rf"\bstruct\s+{class_name}\b",  # C/C++/Rust/Go
        ]

        all_matches = []

        for pattern in patterns:
            result = self.search_code(pattern, directory, case_sensitive=True)
            if "matches" in result:
                all_matches.extend(result["matches"])

        return {
            "class": class_name,
            "total_matches": len(all_matches),
            "matches": all_matches,
        }


# Simple test when running directly
if __name__ == "__main__":
    from file_ops import FileOperations

    print("Testing Code Search...")
    ops = FileOperations()
    search = CodeSearch(ops)

    result = search.search_code("def ", ".")
    if "error" in result:
        print("Error:", result["error"])
    else:
        print(f"✓ Found {result['total_matches']} matches in {result['files_with_matches']} files")
