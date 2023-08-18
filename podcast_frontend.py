import streamlit as st
import modal
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Newsletter Dashboard",
    page_icon="🎧",
    layout="wide"
)

# Apply custom styles
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar {
        background-color: #333333;
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }
    .header {
        color: #333333;
        padding: 1rem;
        text-align: center;
    }
    .subheader {
        color: #666666;
        padding: 1rem 0;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .content-container {
        padding: 1rem;
    }
    .footer {
        color: #666666;
        text-align: center;
        padding: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    st.title("Newsletter Dashboard")

    # Sidebar
    with st.sidebar.container():
        st.sidebar.header("Podcast RSS Feeds")
        selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())

        if selected_podcast:
            podcast_info = available_podcast_info[selected_podcast]
            display_podcast_details(podcast_info)

    # Main content
    with st.container():
        st.header("Newsletter Content")

        if selected_podcast:
            display_podcast_details(podcast_info)

    # Footer
    st.markdown(
        """
        <div class="footer">
        Powered by Streamlit &middot; Created by Your Name
        </div>
        """,
        unsafe_allow_html=True
    )

def display_podcast_details(podcast_info):
    # Display podcast title
    st.subheader("Episode Title")
    st.write(podcast_info['podcast_details']['episode_title'])

    # Display podcast summary and cover image
    col1, col2 = st.columns([7, 3])

    with col1:
        st.subheader("Podcast Episode Summary")
        st.write(podcast_info['podcast_summary'])

    with col2:
        st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

    # Display podcast host and host details
    col3, col4 = st.columns([3, 7])

    with col3:
        st.subheader("Podcast Host")
        st.write(podcast_info['podcast_host']['name'])

    with col4:
        st.subheader("Podcast Host Details")
        st.write(podcast_info["podcast_host"]['summary'])

    # Display key moments
    st.subheader("Key Moments")
    key_moments = podcast_info['podcast_highlights']
    for moment in key_moments.split('\n'):
        st.markdown(
            f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True
        )

# Load podcast data
available_podcast_info = create_dict_from_json_files('.')

if __name__ == '__main__':
    main()
