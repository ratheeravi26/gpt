import openai
import streamlit as st

# Set up the OpenAI API key
openai.api_key = "YOUR_API_KEY"

# Define the Streamlit app
def main():
    # Create a search bar using the Streamlit text_input function
    search_query = st.text_input("Search query:", "")

    # Only generate suggestions if the search query is at least 3 characters long
    if len(search_query) >= 3:
        # Generate suggestions using the OpenAI GPT-3 model
        suggestions = generate_suggestions(search_query)

        # Display the suggestions using the Streamlit write function
        if suggestions:
            st.write("Suggestions:")
            st.write(suggestions)
        else:
            st.write("No suggestions found.")

# Define function to generate suggestions using the OpenAI GPT-3 model
def generate_suggestions(prompt):
    # Call the OpenAI Completion API to generate suggestions
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=3,
        stop=None,
        temperature=0.5,
    )

    # Parse the response and extract the suggestions
    suggestions = []
    for choice in response.choices:
        suggestion = choice.text.strip()
        if suggestion:
            suggestions.append(suggestion)

    # Return the suggestions as a list
    return suggestions

if __name__ == "__main__":
    main()
