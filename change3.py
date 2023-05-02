import openai
import streamlit as st

# Set up OpenAI credentials
openai.api_key = "YOUR_API_KEY"

# Choose an OpenAI language model
model_engine = "davinci"  # or another model of your choice

# Define a function to generate suggestions using the OpenAI language model
def get_suggestions(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=50,
        n=5,
        stop=None,
        temperature=0.5,
    )
    return [choice.text for choice in completions.choices]

# Create a Streamlit search bar widget with autocomplete
search_input = st.text_input("Search", "")

# Display suggestions in a dropdown menu as the user types
if search_input:
    suggestions = get_suggestions(search_input)
    if suggestions:
        st.write("Did you mean:")
        selected_suggestion = st.selectbox("", suggestions, index=0)
        search_input = selected_suggestion

# Display the final search query after any suggestions have been selected
if search_input:
    st.write(f"Searching for: {search_input}")
