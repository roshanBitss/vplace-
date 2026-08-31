
from ai_core.llm.client import LLMClient
from resume_analyzer.prompt.prompt_loader import load_prompt
import json

class ResumeAnalyzer:
    def __init__(self):
        self.llm =LLMClient()

    def analyze(self,resume_text):
        prompt = load_prompt(
            "prompt.txt",
            resume_text=resume_text,
            
            
        )
        response = self.llm.generate(prompt)

        if not response:
            raise ValueError("LLM returned an empty response or failed to generate text")

        try:
            analysis = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON")

        return analysis
