import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
import streamlit as st
from torch.amp import autocast  # Updated import to the new version

model_dir = "Yellow-AI-NLP/komodo-7b-base"
adapter_dir = "C:/Users/Komodo/Documents/Komodo-7b/training_final_finetuned_2000_v2"

id2label = {0: "Negative", 1: "Neutral", 2: "Positive"}
label2id = {"Negative": 0, "Neutral": 1, "Positive": 2}

# Load model
model = AutoModelForSequenceClassification.from_pretrained(
    model_dir,
    num_labels=3,
    id2label=id2label,
    label2id=label2id
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# Resize token embeddings
def smart_tokenizer_and_embedding_resize(model, tokenizer):
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

smart_tokenizer_and_embedding_resize(model, tokenizer)

# Load LoRA 
model = PeftModel.from_pretrained(model, adapter_dir)

# Check CUDA Available or not
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


#Agar Model yang sudah di load tidak dijalankan berulang kali ketika streamlit melakukan perubahan
@st.cache_resource  
def load_model():
    return model, tokenizer, device

model, tokenizer, device = load_model()

def predict_sentiment(texts):

    # Proses Tokenisasi
    inputs = tokenizer(texts, max_length=128, truncation=True, padding=True, return_tensors="pt").to(device)
    #Max length =>  panjang maksimal token
    #Truncation => Teks yang lebih panjang dipotong sesuai length
    #Padding => teks yang lebih pendek dari max length akan ditambahkan

    
    # Mengganti menggunakan (FP16)
    with autocast("cuda"):  
        with torch.no_grad():
            logits = model(**inputs).logits
    #autocast digunakan untuk memungkinkan presisi campuran, karena ditraining dengan bf16 yang lebih rendah dari fp32
    
    predictions = torch.argmax(logits, dim=-1)
    return [id2label[p.item()] for p in predictions]
