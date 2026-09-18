
import json
from ai_core.llm.client import LLMClient
from resume_analyzer.prompt.prompt_loader import load_prompt

class ResumeJDMatcher:
    def __init__(self):
        self.llm = LLMClient()

    def match(self,resume_text,job_role, skills_required,job_description):
        prompt = load_prompt(
            "resume_jd_matching.txt",
            resume_text=resume_text,
            job_role = job_role,
            skills_required = skills_required,
            job_description=job_description

        )

        print("\n========== PROMPT ==========")
        print(prompt[:5000])
        print("============================\n")

        response = self.llm.generate(prompt)
        print("\n========== LLM RESPONSE ==========")
        print(response)
        print("==================================\n")

        if not response:
            raise ValueError("LLM returned an empty response or failed to generate text")

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON")
