from langchain_core.prompts import PromptTemplate

template = """
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate.from_template(
    template
)

formatted_prompt = prompt.format(
    context="Redis is an in-memory database.",
    question="What is Redis?"
)

print(formatted_prompt)