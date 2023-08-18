import streamlit as st
import modal
import json
import os

st.markdown(
    """
    <style>
    body {
        background-image: url('path_to_your_image.jpg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    st.title("Newsletter Dashboard")
    st.markdown(
        """
        <style>
        .main-container {
            background-color: #f4f4f4;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar-container {
            background-color: #333333;
            padding: 2rem;
            border-radius: 10px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    with st.sidebar.container():
        st.sidebar.header("Podcast RSS Feeds")
        selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

        if selected_podcast:
            podcast_info = available_podcast_info[selected_podcast]
            # Rest of the code remains the same...

    # User Input box
    with st.sidebar.container():
        st.sidebar.subheader("Add and Process New Podcast Feed")
        url = st.sidebar.text_input("Link to RSS Feed")

        process_button = st.sidebar.button("Process Podcast Feed")
        st.sidebar.markdown("**Note**: Podcast processing can take up to 5 mins, please be patient.")

        if process_button:
            podcast_info = process_podcast_info(url)
            # Rest of the code remains the same...

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}

    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            # Process the file data as needed
            data_dict[podcast_name] = podcast_info

    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
