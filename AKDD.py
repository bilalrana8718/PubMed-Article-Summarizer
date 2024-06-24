import streamlit as st
from datasets import load_dataset
from transformers import pipeline
import re

def preprocess(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

@st.cache_resource
def load_summarizer():
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")
    return summarizer

summarizer = load_summarizer()

def summarize(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

@st.cache_data
def load_data():

    dataset = load_dataset('scientific_papers', 'pubmed', split='train[:1%]', trust_remote_code=True)
    return dataset

dataset = load_data()
st.title("PubMed Article Summarizer")

from PIL import Image
image = Image.open('streamlit.png')
st.image(image, width=200)

uploaded_file = st.file_uploader("Upload a PubMed article", type="txt")

if uploaded_file is not None:

    article = uploaded_file.read().decode("utf-8")
    article = preprocess(article)


    st.subheader("Original Article")
    st.text_area(" ", value=article, height=300, max_chars=None)
    summary = summarize(article)
    st.subheader("Summarized Article")
    st.text_area(" ", value = summary, height = 300, max_chars=None)
