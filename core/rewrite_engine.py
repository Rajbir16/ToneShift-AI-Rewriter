def rewrite_text(groq_client, *, prompt: str) -> str:
    return groq_client.rewrite(prompt)

