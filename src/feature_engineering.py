from textblob import TextBlob
import pandas as pd
import re

def add_sentiment_features(df):
    """Add sentiment analysis features to DataFrame"""
    df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['subjectivity'] = df['message'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    return df

def encode_categorical_features(df):
    """Encode categorical features"""
    df = pd.get_dummies(df, columns=['day_of_week', 'media'], prefix=['day', 'media'])
    return df
# Add to feature_engineering.py

def clean_message(text):
    """Clean message text"""
    text = re.sub(r'\n', ' ', text)  # Remove newlines
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.strip()

def add_text_features(df):
    """Add additional text features"""
    df['message_clean'] = df['message'].apply(clean_message)
    df['contains_special_char'] = df['message'].apply(lambda x: bool(re.search(r'[^\w\s]', x)))
    return df