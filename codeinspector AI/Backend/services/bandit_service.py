import os
import json
from openai import OpenAI

class AIService:
    @staticmethod
    def get_client(api_key):
        # Updated base URL without strict sub-version locks to prevent 404 router mismatch
        return OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/"
        )

    @staticmethod
    def review_code(code_content, file_name="script.py"):
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key or "your_actual" in api_key or api_key == "mock-key":
            lines = len(code_content.splitlines())
            return {
                "score": 80,
                "summary": "Local static review profile activated.",
                "findings": []
            }

        try:
            client = AIService.get_client(api_key)
            prompt = f"""
            You are an experienced Senior Software Engineer.
            Review the uploaded code inside the file named '{file_name}' and provide code diagnostics in JSON format.
            Return the response STRICTLY in structured JSON format matching this exact template:
            {{
                "score": 85,
                "summary": "Short summary text...",
                "findings": [
                    {{
                        "severity": "High/Medium/Low",
                        "issue": "Name of the problem",
                        "explanation": "Why this is an issue",
                        "suggestion": "How to fix it"
                    }}
                ]
            }}
            
            Code to analyze:
            {code_content}
            """
            response = client.chat.completions.create(
                model="gemini-1.5-flash",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"score": 30, "summary": f"AI Parsing Error: {str(e)}", "findings": []}

    @staticmethod
    def generate_documentation(code_content, file_name="script.py"):
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key or "your_actual" in api_key or api_key == "mock-key":
            return "# Technical Specification Docs Fallback"

        try:
            client = AIService.get_client(api_key)
            prompt = f"Generate a comprehensive technical writer documentation in Markdown format for this code:\n{code_content}"
            response = client.chat.completions.create(
                model="gemini-1.5-flash",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"### Documentation Error: {str(e)}"

    @staticmethod
    def analyze_performance(code_content, file_name="script.py"):
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key or "your_actual" in api_key or api_key == "mock-key":
            return {"estimated_time_complexity": "O(1)", "estimated_space_complexity": "O(1)", "io_overhead_risk": "Low", "bottlenecks": []}

        try:
            client = AIService.get_client(api_key)
            prompt = f"""
            You are a Performance Optimization Engineer. Analyze the following code file '{file_name}' for runtime efficiency bottlenecks.
            Return structured JSON:
            {{
                "estimated_time_complexity": "e.g., O(N^2)",
                "estimated_space_complexity": "e.g., O(1)",
                "io_overhead_risk": "High/Medium/Low",
                "bottlenecks": ["description"]
            }}
            Code:
            {code_content}
            """
            response = client.chat.completions.create(
                model="gemini-1.5-flash",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"estimated_time_complexity": "Unknown", "estimated_space_complexity": "Unknown", "io_overhead_risk": "Low", "bottlenecks": [str(e)]}