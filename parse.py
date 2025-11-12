from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# --- NEW, STRONGER TEMPLATE ---
# This prompt is much stricter. It FORCES the AI to be silent if it finds nothing.
template = (
    "You are an information extraction robot. You will be given text: {dom_content}. "
    "Your one and only job is to find text that matches this user request: {parse_description}. "
    "RULES: "
    "1. ONLY output the extracted text. "
    "2. If no text matches the request, or if the text is irrelevant, you MUST output a single, empty string. "
    "3. Do NOT add 'None found', 'No section exists', or any other explanation. Just the data or nothing."
)

model = OllamaLLM(model="llama3")

def parse_with_ollama(dom_chunks, parse_Description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_Description}
            )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        
        # --- NEW LOGIC ---
        # Only add the response to our list if it's not empty or just whitespace.
        # This filters out the "None found" chunks.
        if response and response.strip():
            parsed_result.append(response)

    # --- NEW OUTPUT ---
    # If the list is still empty after all chunks, then we really found nothing.
    if not parsed_result:
        return "The AI could not find any matching information on the page."

    # Join the *good* results with a clear separator so you can see the different chunks.
    return "\n\n---\n\n".join(parsed_result)