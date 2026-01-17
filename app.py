import pandas as pd

data = pd.read_csv("mental_health_sentiment_dataset.csv")

import streamlit as st
from textblob import TextBlob

def generate_response(sentiment):
    responses = {
        "Very Positive": "I'm really happy to hear that! Keep up this positive mindset 🌟",
        "Positive": "That's good to hear. You're doing well—keep moving forward 💪",
        "Neutral": "Thanks for sharing. Would you like to talk more about your day?",
        "Negative": "I'm sorry you're feeling this way. You're not alone 🤍 Take it one step at a time.",
        "Very Negative": "That sounds really difficult. Please consider reaching out to someone you trust or a mental health professional."
    }
    return responses.get(sentiment, "I'm here to listen.")


# Analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.5:
        return "Very Positive", polarity
    elif 0.1 < polarity <= 0.5:
        return "Positive", polarity
    elif -0.1 <= polarity <= 0.1:
        return "Neutral", polarity
    elif -0.5 < polarity < -0.1:
        return "Negative", polarity
    else:
        return "Very Negative", polarity


# Provide coping strategies
def provide_coping_strategy(sentiment):
    strategies = {
        "Very Positive": "Keep up the positive vibes! Consider sharing your good mood with others.",
        "Positive": "It's great to see you're feeling positive. Keep doing what you're doing!",
        "Neutral": "Feeling neutral is okay. Consider engaging in activities you enjoy.",
        "Negative": "It seems you're feeling down. Try to take a break and do something relaxing.",
        "Very Negative": "I'm sorry to hear that you're feeling very negative. Consider talking to a friend or seeking professional help."
    }
    return strategies.get(sentiment, "Keep going, you're doing great!")


# Disclaimer regarding data privacy
def display_disclaimer():
    st.sidebar.markdown(
        "<h2 style='color: #FF5733;'>Data Privacy Disclaimer</h2>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<span style='color: #FF5733;'>This application stores your session data, including your messages and "
        "sentiment analysis results, in temporary storage during your session. "
        "This data is not stored permanently and is used solely to improve your interaction with the chatbot. "
        "Please avoid sharing personal or sensitive information during your conversation.</span>",
        unsafe_allow_html=True
    )

st.title("Mental Health Support Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'mood_tracker' not in st.session_state:
    st.session_state['mood_tracker'] = []

with st.form(key='chat_form'):
    user_message = st.text_input("You:")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_message:
    st.session_state['messages'].append(("You", user_message))

    sentiment, polarity = analyze_sentiment(user_message)
    coping_strategy = provide_coping_strategy(sentiment)

    response = generate_response(sentiment)

    st.session_state['messages'].append(("Bot", response))
    st.session_state['mood_tracker'].append((user_message, sentiment, polarity))

for sender, message in st.session_state['messages']:
    if sender == "You":
        st.text(f"You: {message}")
    else:
        st.text(f"Bot: {message}")

# Display mood tracking chart
if st.session_state['mood_tracker']:
    mood_data = pd.DataFrame(st.session_state['mood_tracker'], columns=["Message", "Sentiment", "Polarity"])
    st.line_chart(mood_data['Polarity'])

# Display coping strategies
if user_message:
    st.write(f"Suggested Coping Strategy: {coping_strategy}")

# Display resources
st.sidebar.title("Resources")
st.sidebar.write("If you need immediate help, please contact one of the following resources:")
st.sidebar.write("1. National Suicide Prevention Lifeline: 1-800-273-8255")
st.sidebar.write("2. Crisis Text Line: Text 'HELLO' to 741741")
st.sidebar.write("[More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")

# Display session summary
if st.sidebar.button("Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (message, sentiment, polarity) in enumerate(st.session_state['mood_tracker']):
        st.sidebar.write(f"{i + 1}. {message} - Sentiment: {sentiment} (Polarity: {polarity})")


display_disclaimer()