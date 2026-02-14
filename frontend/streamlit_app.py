"""Minimal Streamlit UI for the compliance QA backend."""

import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Compliance QA", layout="centered")
st.title("🎥 Multi-Modal Compliance QA")
st.caption("Upload a video or analyze a YouTube URL.")

mode = st.radio("Input Type", ["Upload Video", "YouTube URL"], horizontal=True)

if mode == "Upload Video":
    upload = st.file_uploader("Upload video", type=["mp4", "mov", "mkv", "avi"])
    if st.button("Analyze Upload", disabled=upload is None):
        with st.spinner("Running analysis..."):
            files = {"file": (upload.name, upload.read(), upload.type or "video/mp4")}
            response = requests.post(f"{API_BASE}/analyze/upload", files=files, timeout=1800)
            if response.ok:
                st.success("Analysis complete")
                st.json(response.json())
            else:
                st.error(response.text)

else:
    youtube_url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    if st.button("Analyze YouTube", disabled=not youtube_url):
        with st.spinner("Downloading + analyzing..."):
            response = requests.post(
                f"{API_BASE}/analyze/youtube",
                json={"youtube_url": youtube_url},
                timeout=1800,
            )
            if response.ok:
                st.success("Analysis complete")
                st.json(response.json())
            else:
                st.error(response.text)

if st.button("Build / Refresh Rule Index"):
    response = requests.post(f"{API_BASE}/rules/build-index", timeout=300)
    if response.ok:
        st.success("Vector index built")
    else:
        st.error(response.text)
