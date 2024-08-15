import streamlit as st
from datasets import load_dataset
from transformers import pipeline
import re
from PyPDF2 import PdfReader
import docx
from PIL import Image

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
    summary = summarizer(text, max_length=394, min_length=30, do_sample=False, clean_up_tokenization_spaces=True)
    return summary[0]['summary_text']

@st.cache_data
def load_data():
    dataset = load_dataset('scientific_papers', 'pubmed', split='train[:1%]', trust_remote_code=True)
    return dataset

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

dataset = load_data()
st.title("PubMed Article Summarizer")

image = Image.open('streamlit.png')
st.image(image, width=200)

uploaded_file = st.file_uploader("Upload an article", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".txt"):
        article = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        article = read_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        article = read_docx(uploaded_file)

    article = preprocess(article)

    st.subheader("Original Article")
    st.text_area(" ", value=article, height=300, max_chars=None)
    summary = summarize(article)
    st.subheader("Summarized Article")
    st.text_area(" ", value=summary, height=300, max_chars=None)
