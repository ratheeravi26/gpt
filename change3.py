import openai
import streamlit as st

# Set up OpenAI credentials
openai.api_key = "YOUR_API_KEY"

# Choose an OpenAI language model
model_engine = "davinci"  # or another model of your choice

# Define some custom CSS styling for the search bar
st.markdown(
    """
    <style>
    .stTextInput > input {
        padding-right: 120px;
    }
    .stTextInput > div {
        position: absolute;
        right: 0;
        top: 100%;
        width: 100%;
        max-height: 200px;
        overflow-y: auto;
        z-index: 10;
        background-color: white;
        border: 1px solid #d3d3d3;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create a Streamlit search bar widget with autocomplete
search_input = st.text_input("Search", "")

if search_input:
    # Generate completions using the OpenAI language model
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=search_input,
        max_tokens=50,
        n=5,
        stop=None,
        temperature=0.5,
    )

    # Extract the text of each completion and format as a string
    suggestions = "\n".join([choice.text for choice in completions.choices])

    # Display the suggestions below the search bar
    st.markdown(f"<div>{suggestions}</div>", unsafe_allow_html=True)
