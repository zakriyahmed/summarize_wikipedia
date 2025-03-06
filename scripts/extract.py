from typing import Annotated
import requests
from bs4 import BeautifulSoup as bs
import re
import spacy
import json

nlp = spacy.load("en_core_web_sm")


def get_article(link: Annotated[str, 'URL to the article']):
    response = requests.get(link)

    if response.status_code != 200:
        print("Failed to fetch page")
        return None

    soup = bs(response.text, 'html.parser')

    content = soup.find("div", {"id": "bodyContent"})  # Extract main content
    if not content:
        print("Could not find content")
        return None
    
    paragraphs = content.find_all("p") # Extract paras

    paragraphs = content.find_all('p')
    article_text = ''.join([para.get_text() for para in paragraphs])
    return article_text

def clean_text(text: Annotated[str, 'Text to be cleaned']):
    # Remove references like [1], [23], etc.
    text = re.sub(r'\[\d+\]', '', text)
    # Remove special characters and extra spaces
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Process text with SpaCy (lemmatization, stopword removal)
    doc = nlp(text)
    cleaned_text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
    
    return cleaned_text

def save_data(title, cleaned_text):
    data = {"title": title, "text": cleaned_text}
    with open(f"../data/{title}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved: {title}.json")

url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
wikipedia_text = get_article(url)
if wikipedia_text:
    cleaned_text = clean_text(wikipedia_text)
    save_data("Artificial Intelligence", cleaned_text)



