from textblob import TextBlob
import pandas as pd

def add_sentiment_features(df):
    """Add sentiment analysis features to DataFrame"""
    df['sentiment'] = df['message'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['subjectivity'] = df['message'].apply(lambda x: TextBlob(x).sentiment.subjectivity)
    return df

def encode_categorical_features(df):
    """Encode categorical features"""
    df = pd.get_dummies(df, columns=['day_of_week', 'media'], prefix=['day', 'media'])
    return df