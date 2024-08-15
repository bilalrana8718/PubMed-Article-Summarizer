# PubMed Article Summarizer

## Overview

The PubMed Article Summarizer is a web application built with Streamlit that allows users to upload PubMed articles in `.txt` format, and generates concise summaries using both local summarization models and Google Generative AI. The application supports text extraction and summarization from various formats including `.txt`, `.pdf`, and `.doc` files.

## Features

- **Upload and Process Files:** Supports uploading `.txt`, `.pdf`, and `.doc` files for summarization.
- **Local Summarization Model:** Uses Hugging Face's transformers library to summarize text.
- **Interactive Interface:** Streamlit provides an easy-to-use web interface for uploading files and viewing summaries.

## Requirements

- Python 3.7 or later
- Streamlit
- Hugging Face Transformers


## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/bilalrana8718/PubMed-Article-Summarizer
   cd PubMed-Article-Summarizer


   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

   pip install -r requirements.txt

   streamlit run AKDD.py

