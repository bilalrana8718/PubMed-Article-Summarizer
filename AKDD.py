import streamlit as st
from datasets import load_dataset
from transformers import pipeline
import re
from PyPDF2 import PdfReader
import docx
from PIL import Image
import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GEM_KEY"))

# Your API key and Programmable Search Engine ID
api_key = 'AIzaSyBDNFet0sGeuVEub-iTWjNEyyNhSGIpB50'
cse_id = '74a9c6ca4ecd7403c'


generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1024
}

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=generation_config
)

def preprocess(text):
    text = re.sub(r'\W', ' ', text)
    text = text.lower()
    return text

def chunk_text(text, max_length=1024):
    words = text.split()
    chunks = []
    chunk = []
    length = 0
    for word in words:
        length += len(word) + 1  # +1 for space
        if length > max_length:
            chunks.append(" ".join(chunk))
            chunk = [word]
            length = len(word) + 1
        else:
            chunk.append(word)
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

@st.cache_resource
def load_summarizer():
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")
    return summarizer

summarizer = load_summarizer()

def summarize(text):
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk,max_length=60, do_sample=False, clean_up_tokenization_spaces=True)
        summaries.append(summary[0]['summary_text'])
    final_summary = " ".join(summaries)
    return final_summary


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
