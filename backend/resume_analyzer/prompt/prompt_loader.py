from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(prompt_name: str, **kwargs) -> str:
    """
    Load a prompt from a .txt file and replace
    template variables with the provided values.

    Example:
        load_prompt(
            "resume_analysis.txt",
            resume_text="Python Developer..."
        )
    """

    prompt_path = PROMPTS_DIR / prompt_name

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    prompt = prompt_path.read_text(encoding="utf-8")

    for key, value in kwargs.items():
        prompt = prompt.replace(
            f"{{{{{key}}}}}",
            str(value)
        )

    return prompt