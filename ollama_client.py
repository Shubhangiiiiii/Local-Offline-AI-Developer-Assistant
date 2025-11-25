import ollama
import json
import sys


class DeepSeekClient:
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.model = model
        self._test_connection()

    def _test_connection(self):
        """Test if Ollama is running."""
        try:
            # This will fail if Ollama isn't running
            ollama.list()
        except Exception as e:
            print("⚠️  Warning: Cannot connect to Ollama. Make sure Ollama is running.")
            print(f"   Error: {str(e)}")
            print("   Try running: ollama serve")
            print()
            # We don't exit here so the rest of the code can still be imported

    def ask(self, prompt: str, context: str = "") -> str:
        """Send a prompt to DeepSeek Coder via Ollama."""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt,
                    }
                ],
                options={
                    "temperature": 0.7,
                },
            )

            return response["message"]["content"]

        except Exception as e:
            return (
                f"❌ Error communicating with DeepSeek: {str(e)}\n\n"
                "Make sure Ollama is running (ollama serve) and the model is pulled."
            )

    def explain_code(self, code: str, filename: str = "") -> str:
        """Explain what a piece of code does with improved prompting."""
        prompt = f"""
You are a code analysis assistant.
You CAN see the full code provided. Never say you lack access.

File Name: {filename or 'unknown file'}

====== CODE START ======
{code}
====== CODE END ======

Now explain clearly:
1. What this code does overall
2. What each important function does
3. Any important logic or patterns
4. Any potential bugs or edge cases
        """

        return self.ask(prompt)

    def debug_code(self, code: str, error: str = "", line_number: int | None = None) -> str:
        """Help debug a piece of code."""
        location = f"Line {line_number}" if line_number else "Unknown location"

        prompt = f"""
You are a debugging assistant.
You CAN see the full code provided below.

Error message: {error or 'General debugging requested'}
Location: {location}

====== CODE START ======
{code}
====== CODE END ======

Analyze the code and error and provide:
1. What is likely wrong
2. Why it happens
3. How to fix it (specific explanation)
4. A corrected code snippet or patch
        """

        return self.ask(prompt)

    def suggest_improvements(self, code: str) -> str:
        """Suggest improvements for a piece of code."""
        prompt = f"""
You are a senior software engineer reviewing this code.

====== CODE START ======
{code}
====== CODE END ======

Review it and suggest improvements focusing on:
1. Code quality and readability
2. Performance optimizations
3. Best practices and style
4. Potential bugs or edge cases
5. Security concerns (if any)

Be specific and refer to concrete parts of the code where possible.
        """

        return self.ask(prompt)

    def answer_question(self, question: str, code_context: str = "") -> str:
        """Answer general coding questions with optional code context."""
        if code_context:
            prompt = f"""
You are a coding assistant. Use the code context below to answer the question.

====== CODE CONTEXT START ======
{code_context}
====== CODE CONTEXT END ======

Question: {question}

Give a clear, specific answer that references the code where helpful.
            """
        else:
            prompt = f"""
You are a coding assistant.

Question: {question}

Give a clear, helpful answer with examples if relevant.
            """

        return self.ask(prompt)

    def find_function_usage(self, function_name: str, code: str) -> str:
        """Explain how a function is used in given code."""
        prompt = f"""
You are analyzing usage of a function in code.

Function name: {function_name}

====== CODE START ======
{code}
====== CODE END ======

Explain:
1. What this function does
2. Its parameters and return value
3. Where and how it is used in the code
4. Any important implementation details or caveats
        """

        return self.ask(prompt)


# Simple test when running this file directly
if __name__ == "__main__":
    print("Testing DeepSeek Coder connection...\n")
    client = DeepSeekClient()

    print("Asking: 'Write a simple hello world in Python'\n")
    response = client.ask("Write a simple hello world in Python")
    print(response)
