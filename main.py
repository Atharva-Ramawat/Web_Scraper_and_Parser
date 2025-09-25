
## To activate : cd C:\python\AI_Web_Scraper.\ai\Scripts\activate
## Brightdata for selenium : https://brd-customer-hl_5b2633ca-zone-ai_scraper:74bri33hle5f@brd.superproxy.io:9515
## 1
import streamlit as st
from scrape import (scrape_website,split_dom_content,clean_body_content,extraxt_body_content)
from parse import parse_with_ollama


st.title(' AI Web Scraper ')
url = st.text_input('Enter Website URL:')

if st.button('Scrap Website'):
    st.write('\n Scraping Website ... \n ')

    result = scrape_website(url)
    body_content = extraxt_body_content(result)
    cleaned_content = clean_body_content(body_content)    

    st.session_state.dom_content = cleaned_content 

    with st.expander("View DOM content"):
        st.text_area("DOM Content",cleaned_content, height=300)

 
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want  to parse ?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("paring the content..")
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks,parse_description)
            st.write(result)

