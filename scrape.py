import requests
from bs4 import BeautifulSoup
import streamlit as st

def scrape_website(website):
    """
    Fetches website content using the requests library.
    """
    print("Fetching website content with requests...")
    try:
        # Add headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Add http:// if no scheme is present
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'https://' + website
            
        response = requests.get(website, headers=headers, timeout=10)
        
        # Check for successful response
        response.raise_for_status() 
        
        return response.text
        
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err} - Could not access {website}")
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        st.error(f"Connection error occurred: {conn_err} - Could not connect to {website}")
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        st.error(f"Timeout error occurred: {timeout_err} - The request to {website} timed out")
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"An unexpected error occurred: {req_err}")
        print(f"An unexpected error occurred: {req_err}")
    
    return None # Return None if scraping failed


def extract_body_content(html_content):
    """
    Extracts the <body> tag content from HTML.
    """
    if not html_content:
        return ""
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    """
    Cleans the HTML body content by removing scripts, styles,
    and extra whitespace.
    """
    if not body_content:
        return ""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text and remove excessive whitespace
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    """
    Splits the cleaned content into manageable chunks for the AI.
    """
    if not dom_content:
        return []
    return [
        dom_content[i: i + max_length]
        for i in range(0, len(dom_content), max_length)
    ]