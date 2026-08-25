from django.http import response
from ai_core.llm.client import LLMClient
from resume_analyzer.prompt.prompt_loader import load_prompt

class ResumeAnalyzer:
    def __init__(self):
        self.llm =LLMClient()

    def analyze(self,resume_text):
        prompt = load_prompt(
            "prompt.txt",
            resume_text=resume_text,
            
            
        )
        response = self.llm.generate(prompt)

        return response