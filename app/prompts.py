from textwrap import dedent

def make_system_prompt(base: str) -> str:
    return dedent(base).strip()
