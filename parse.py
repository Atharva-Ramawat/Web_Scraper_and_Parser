from groq import Groq
import os
import streamlit as st

# --- NEW, STRONGER TEMPLATE ---
# This prompt is much stricter. It FORCES the AI to be silent if it finds nothing.
template = (
    "You are a web scraper's AI assistant. Your ONLY job is to extract specific information from a chunk of website text."
    "The user will provide the text chunk and an extraction goal."
    "---"
    "WEBSITE TEXT CHUNK: {dom_content}"
    "---"
    "EXTRACTION GOAL: {parse_description}"
    "---"
    "Follow these rules STRICTLY:"
    "1. ONLY output the information that directly matches the EXTRACTION GOAL."
    "2. If no information in the text chunk matches the goal, you MUST return an empty string. Do not say 'None found', 'I can't find this', or anything else. Just return ''. "
    "3. Do not add any extra words, explanations, or greetings. Only output the raw, extracted data."
)

# --- NEW MODEL: Use the official Groq library ---
try:
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
except Exception as e:
    print(f"Error initializing Groq: {e}")
    st.error(f"Error initializing Groq: {e}. Did you set the GROQ_API_KEY environment variable?")
    client = None

def parse_with_ollama(dom_chunks, parse_Description):
    if client is None:
        return "Error: Groq client is not configured. Check API key."

    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        print(f"Parsing batch {i} of {len(dom_chunks)}")
        
        # Format the prompt for this chunk
        formatted_prompt = template.format(dom_content=chunk, parse_description=parse_Description)
        
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": formatted_prompt,
                    }
                ],
                # --- THIS IS THE ONLY LINE I CHANGED ---
                model="llama-3.1-8b-instant", 
            )
            
            response = chat_completion.choices[0].message.content
            
            # Check our "empty string" rule
            if response.strip(): # If the response isn't just whitespace
                parsed_results.append(response)
                
        except Exception as e:
            print(f"Error parsing chunk {i}: {e}")
            # Show the actual error message on the Streamlit page
            st.error(f"Error parsing chunk {i}: {e}")

    return "\n\n".join(parsed_results)