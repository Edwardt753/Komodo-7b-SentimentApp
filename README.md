# Komodo-7b-SentimentApp
Aplikasi untuk melakukan sentimen analisis untuk komentar video pada YouTube dengan menggunakan base model Komodo-7B oleh YellowAI

## Link HuggingFace
https://huggingface.co/Edwardt753/komodo-7b-sentiment

## Dataset
Dataset yang digunakan adalah dataset yang discraping manual berisikan kolom komentar dan sentimen yang dilabeling secara manual
dengan 3 buah label yaitu Positif, Negatif, dan Netral

## Library yang harus di Instal
1.	NumPy 2.1.2
2.	Pandas  2.2.3
3.	Torch 2.5.1+cu118
4.	Transformers 4.46.1
5.	Datasets 2.16.1
6.	Evaluate 0.4.3
7.	PEFT
8.	Scikit-learn 1.5.2
9.	Streamlit
10.	Matplotlib

# Script Instalasi
pip install numpy==2.1.2 pandas==2.2.3 torch==2.5.1+cu118 torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118 transformers==4.46.1 datasets==2.16.1 evaluate==0.4.3 peft scikit-learn==1.5.2 streamlit matplotlib


## Cara Penggunaan
### 1. Download Folder Streamlit_Sentiment Analysis
### 2. Install semua Library yang diperlukan
### 3. Jalankan dengan perintah "python -m streamlit run 📊Sentiment_App.py"


