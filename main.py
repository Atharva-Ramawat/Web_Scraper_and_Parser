import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_ollama

# 1. Page Config
st.set_page_config(page_title="AI Web Scraper", page_icon="🕵️‍♂️")

# --- NEW CODE: Add this to change the sidebar width ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            width: 350px !important; /* You can change 350px to your liking */
        }
    </style>
    """,
    unsafe_allow_html=True
)
# --- END OF NEW CODE ---


st.title('🕵️‍♂️ AI Web Scraper')
st.markdown("### Interactive Web Scraping with Ollama")

# 2. Sidebar for Input
st.sidebar.header("Configuration")
url = st.sidebar.text_input('Enter Website URL:')

# Initialize session state if it doesn't exist
if 'dom_content' not in st.session_state:
    st.session_state.dom_content = None

# --- SCRAPING SECTION ---
if st.sidebar.button('Scrape Website'):
    if url:
        st.sidebar.success("Scraping started...")
        
        # Scrape and Clean
        try:
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            
            # Store in session state
            st.session_state.dom_content = cleaned_content
            st.sidebar.success("Website scraped and content cleaned successfully!")
        except Exception as e:
            st.sidebar.error(f"An error occurred during scraping: {e}")
    else:
        st.sidebar.error("Please enter a valid URL.")

# --- INTERACTIVE PARSING SECTION ---
if st.session_state.dom_content:
    
    # Show raw content in an expander
    with st.expander("View Raw DOM Content"):
        st.text_area("DOM Content", st.session_state.dom_content, height=300)

    st.divider()
    
    st.subheader("🤖 Ask the AI")
    st.write("Describe what information you want to extract from this page.")
    
    # User input for the AI prompt
    parse_description = st.text_area("Extraction Goal (e.g., 'Extract all product names and prices', 'Summarize the main points')")

    if st.button("Parse Content"):
        if parse_description:
            with st.spinner("Parsing content with Ollama..."):
                
                # Use split_dom_content to handle token limits
                dom_chunks = split_dom_content(st.session_state.dom_content)
                
                # Parse each chunk
                try:
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    
                    st.subheader("Results:")
                    st.write(parsed_result)
                    
                    # Download Button
                    st.download_button(
                        label="Download Results as Text",
                        data=parsed_result,
                        file_name="scraped_data.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"An error occurred during parsing: {e}")
        else:
            st.warning("Please describe what you want to parse.")