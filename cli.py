import sys
import os
from colorama import Fore, Style, init, just_fix_windows_console
from ollama_client import DeepSeekClient
from tools.file_ops import FileOperations
from tools.search import CodeSearch

# Fix Windows console for colors
just_fix_windows_console()
init(autoreset=True)


class AIDevCLI:
    def __init__(self):
        print(f"{Fore.YELLOW}Initializing AI Assistant...{Style.RESET_ALL}")
        self.client = DeepSeekClient()
        self.file_ops = FileOperations()
        self.search = CodeSearch(self.file_ops)
        print(f"{Fore.GREEN}✓ Ready!{Style.RESET_ALL}\n")

    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{text}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    def print_success(self, text):
        print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")

    def print_error(self, text):
        print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

    def print_info(self, text):
        print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")

    def explain_command(self, file_path):
        """Explain a file"""
        self.print_header(f"Explaining: {file_path}")

        result = self.file_ops.read_file(file_path)

        if "error" in result:
            self.print_error(result["error"])
            return

        self.print_success(f"Read {result['lines']} lines ({result['size']} bytes)")
        self.print_info("Asking DeepSeek Coder...\n")

        explanation = self.client.explain_code(result['content'], file_path)
        print(explanation)

    def search_command(self, query):
        """Search for code"""
        self.print_header(f"Searching for: {query}")

        result = self.search.search_code(query)

        if "error" in result:
            self.print_error(result["error"])
            return

        print(
            f"Found {Fore.GREEN}{result['total_matches']}{Style.RESET_ALL} matches "
            f"in {Fore.CYAN}{result['files_with_matches']}{Style.RESET_ALL} files "
            f"(searched {result['files_searched']} files)\n"
        )

        if result['total_matches'] == 0:
            self.print_info("No matches found. Try a different search term.")
            return

        for match in result['matches'][:15]:
            print(
                f"{Fore.YELLOW}Line {match['line']}{Style.RESET_ALL} "
                f"in {Fore.CYAN}{match['file']}{Style.RESET_ALL}"
            )
            print(f"  {match['content']}\n")

        if result['total_matches'] > 15:
            print(
                f"{Fore.YELLOW}... and {result['total_matches'] - 15} more matches"
                f"{Style.RESET_ALL}"
            )

    def debug_command(self, file_path, error_msg=""):
        """Debug a file"""
        self.print_header(f"Debugging: {file_path}")

        result = self.file_ops.read_file(file_path)

        if "error" in result:
            self.print_error(result["error"])
            return

        if error_msg:
            print(f"Error: {Fore.RED}{error_msg}{Style.RESET_ALL}\n")

        self.print_info("Analyzing code...\n")

        debug_info = self.client.debug_code(result['content'], error_msg)
        print(debug_info)

    def improve_command(self, file_path):
        """Suggest improvements"""
        self.print_header(f"Analyzing: {file_path}")

        result = self.file_ops.read_file(file_path)

        if "error" in result:
            self.print_error(result["error"])
            return

        self.print_info("Looking for improvements...\n")

        suggestions = self.client.suggest_improvements(result['content'])
        print(suggestions)

    def ask_command(self, question, file_path=None):
        """Ask a question"""
        self.print_header("AI Assistant")

        print(f"{Fore.CYAN}Question:{Style.RESET_ALL} {question}\n")

        context = ""
        if file_path:
            result = self.file_ops.read_file(file_path)
            if "error" not in result:
                context = result['content']
                self.print_success(f"Using context from: {file_path}\n")
            else:
                self.print_error(f"Could not read context file: {result['error']}\n")

        self.print_info("Thinking...\n")

        answer = self.client.answer_question(question, context)
        print(answer)

    def list_command(self, directory="."):
        """List files"""
        self.print_header(f"Files in: {directory}")

        result = self.file_ops.list_files(directory)

        if "error" in result:
            self.print_error(result["error"])
            return

        self.print_success(f"Found {result['count']} files\n")

        for file in result['files'][:30]:
            print(f"  {Fore.CYAN}•{Style.RESET_ALL} {file}")

        if result['count'] > 30:
            print(
                f"\n  {Fore.YELLOW}... and {result['count'] - 30} more files"
                f"{Style.RESET_ALL}"
            )

    def function_command(self, function_name):
        """Find function definitions"""
        self.print_header(f"Finding function: {function_name}")

        result = self.search.find_function(function_name)

        if result['total_matches'] == 0:
            self.print_error(f"Function '{function_name}' not found")
            return

        self.print_success(f"Found {result['total_matches']} definitions\n")

        for match in result['matches']:
            print(
                f"{Fore.YELLOW}Line {match['line']}{Style.RESET_ALL} "
                f"in {Fore.CYAN}{match['file']}{Style.RESET_ALL}"
            )
            print(f"  {match['content']}\n")

    def run(self):
        """Main CLI loop"""
        if len(sys.argv) < 2:
            self.print_help()
            return

        command = sys.argv[1].lower()

        if command == "explain" and len(sys.argv) > 2:
            self.explain_command(sys.argv[2])

        elif command == "search" and len(sys.argv) > 2:
            self.search_command(sys.argv[2])

        elif command == "debug" and len(sys.argv) > 2:
            error = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            self.debug_command(sys.argv[2], error)

        elif command == "improve" and len(sys.argv) > 2:
            self.improve_command(sys.argv[2])

        elif command == "ask" and len(sys.argv) > 2:
            question = sys.argv[2]
            file_path = sys.argv[3] if len(sys.argv) > 3 else None
            self.ask_command(question, file_path)

        elif command == "list":
            directory = sys.argv[2] if len(sys.argv) > 2 else "."
            self.list_command(directory)

        elif command == "function" and len(sys.argv) > 2:
            self.function_command(sys.argv[2])

        else:
            self.print_help()

    def print_help(self):
        print(f"""
{Fore.CYAN}AI Developer Assistant - Windows Edition{Style.RESET_ALL}

Usage:
  python cli.py <command> [arguments]

Commands:
  explain <file>          Explain what a file does
  search <query>          Search for code patterns
  debug <file> [error]    Debug a file with optional error message
  improve <file>          Suggest code improvements
  ask <question> [file]   Ask a question (with optional context)
  list [directory]        List files in directory
  function <name>         Find function definitions

Examples:
  python cli.py explain app.py
  python cli.py search "def login"
  python cli.py debug auth.py "TypeError on line 45"
  python cli.py improve utils.py
  python cli.py ask "How does this work?" app.py
  python cli.py list src
  python cli.py function calculate_total
        """)


if __name__ == "__main__":
    cli = AIDevCLI()
    cli.run()
