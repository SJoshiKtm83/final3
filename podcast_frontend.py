import streamlit as st
import modal
import json
import os

def main():
    st.set_page_config(page_title="Podcast Newsletter Dashboard", layout="wide")

    st.title("Podcast Newsletter Dashboard")

    available_podcast_info = create_dict_from_json_files('.')

    st.sidebar.header("Podcast RSS Feeds")

    selected_podcast = st.sidebar.selectbox("Select Podcast", options=list(available_podcast_info.keys()))

    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]

        st.header("Episode Details")
        st.subheader(podcast_info['podcast_details']['episode_title'])

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        st.header("Podcast Guest")
        st.subheader(podcast_info['podcast_guest']['name'])

        st.subheader("Guest Details")
        st.write(podcast_info["podcast_guest"]['summary'])

        st.header("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(f"🔹 {moment}", unsafe_allow_html=True)

    st.sidebar.header("Add New Podcast Feed")
    url = st.sidebar.text_input("Enter RSS Feed URL")
    process_button = st.sidebar.button("Process Feed")

    if process_button:
        with st.spinner("Processing..."):
            podcast_info = process_podcast_info(url)

        st.header("Episode Details")
        st.subheader(podcast_info['podcast_details']['episode_title'])

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Podcast Episode Summary")
            st.write(podcast_info['podcast_summary'])

        with col2:
            st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

        st.header("Podcast Guest")
        st.subheader(podcast_info['podcast_guest']['name'])

        st.subheader("Guest Details")
        st.write(podcast_info["podcast_guest"]['summary'])

        st.header("Key Moments")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(f"🔹 {moment}", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
