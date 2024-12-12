import streamlit as st
import matplotlib.pyplot as plt
from model import predict_sentiment
from comment_scraper import fetch_comments
from text_cleaning import clean_comments_list
from youtube_details import get_video_info
import time
import random
import pandas as pd
import io

# Apply custom CSS for spacing and alignment
st.markdown("""
    <style>
    .video-info {
        display: flex;
        align-items: flex-start;
        gap: 20px;
    }
    .video-details, .channel-details {
        margin-top: 10px;
    }
    .channel-info {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
    st.session_state.sentiment_counts = None
    st.session_state.sentiment_comments = None
    st.session_state.results_df = None

# Main content
st.title("Analisa Sentimen Komentar Video YouTube")

# Set custom sidebar titles or routing labels
st.sidebar.title("📊 Analisa Sentimen Komentar Video YouTube")
api_key = st.sidebar.text_input("🔑 Masukan API KEY :", type="password")
default_api_key = "AIzaSyDU3SwEXmP9Hr4XPMOM7Gax1WuC5w0_0dI"
st.sidebar.markdown("Biarkan kosong untuk menggunakan default API key", unsafe_allow_html=True)
st.sidebar.markdown("[Dapatkan YouTube API KEY](https://developers.google.com/youtube/v3/getting-started)", unsafe_allow_html=True)

st.sidebar.markdown("""
    <hr style='border: none; border-top: 1px solid #ccc; margin: 10px 0;' />
    <p style='color: red; font-size: medium;'>
        Disclaimer: Proses Analisa Sentimen hanya dapat bekerja pada Video dengan komentar berbahasa Indonesia
    </p>
""", unsafe_allow_html=True)

video_id = st.text_input("Masukan YouTube Video ID:")

if st.button("Mulai Analisa Sentimen"):
    # Use default API key if the input is blank
    api_key = api_key or default_api_key

    if video_id:
        # Initialize the progress bar
        progress_bar = st.progress(0)
        progress_text = st.empty()

        # Step 1: Fetch comments
        progress_text.text("Step 1: Menangkap Komentar YouTube...")
        try:
            comments = fetch_comments(api_key, video_id)
        except Exception as e:
            st.error("Video ID tidak valid, mohon periksa kembali")
            st.stop()
        time.sleep(1)
        progress_bar.progress(33)

        # Step 2: Clean comments
        progress_text.text("Step 2: Membersihkan Komentar...")
        cleaned_comments = clean_comments_list(comments)
        time.sleep(1)
        progress_bar.progress(66)

        # Step 3: Sentiment analysis
        progress_text.text("Step 3: Melakukan Analisis Sentimen...")
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        sentiment_comments = {"Positive": [], "Neutral": [], "Negative": []}
        batch_size = 8

        for i in range(0, len(cleaned_comments), batch_size):
            batch = cleaned_comments[i:i+batch_size]
            sentiments = predict_sentiment(batch)
            for sentiment, comment in zip(sentiments, batch):
                sentiment_counts[sentiment] += 1
                sentiment_comments[sentiment].append(comment)

        progress_bar.progress(100)
        progress_text.text("Analysis Selesai!")

        # Store analysis results in session state
        st.session_state.analysis_done = True
        st.session_state.sentiment_counts = sentiment_counts
        st.session_state.sentiment_comments = sentiment_comments
        st.session_state.results_df = pd.DataFrame({
            "Comment": sentiment_comments["Positive"] + sentiment_comments["Neutral"] + sentiment_comments["Negative"],
            "Sentiment": ["Positive"] * len(sentiment_comments["Positive"]) +
                        ["Neutral"] * len(sentiment_comments["Neutral"]) +
                        ["Negative"] * len(sentiment_comments["Negative"])
        })
    else:
        st.warning("Silahkan masukan Video ID terlebih dahulu")

# Display analysis results if they exist in session state
if st.session_state.analysis_done:
    sentiment_counts = st.session_state.sentiment_counts
    sentiment_comments = st.session_state.sentiment_comments
    results_df = st.session_state.results_df

    # Display video information
    video_info = get_video_info(api_key, video_id)
    if "error" not in video_info:
        st.markdown("<div class='video-info'>", unsafe_allow_html=True)
        st.image(video_info["thumbnail_url"], width=300)
        st.markdown(f"""
            <div class='video-details'>
                <p><b>Judul:</b> {video_info['video_title']}</p>
                <p><b>Tanggal Rilis:</b> {video_info['release_date']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='channel-info'>", unsafe_allow_html=True)
        st.image(video_info["channel_image_url"], width=150)
        st.markdown(f"<p class='channel-details'><b>Nama Channel:</b> {video_info['channel_name']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning(video_info["error"])

    # Display sentiment counts and pie chart
    st.write("### Ringkasan Hasil Analisis Sentimen")
    st.write(f"Total Komentar Positif: {sentiment_counts['Positive']}")
    st.write(f"Total Komentar Netral: {sentiment_counts['Neutral']}")
    st.write(f"Total Komentar Negatif: {sentiment_counts['Negative']}")

    # Update labels to Bahasa Indonesia
    labels = ["Positif", "Netral", "Negatif"]
    sizes = sentiment_counts.values()
    colors = ['#66c2a5', '#fc8d62', '#8da0cb']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

    # Add download button
    st.write("### Download Hasil Analisis")
    csv_buffer = io.StringIO()
    results_df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_data = csv_buffer.getvalue()
    st.download_button(
        label="💾 Download CSV",
        data=csv_data,
        file_name="youtube_sentiment_analysis.csv",
        mime="text/csv"
    )
