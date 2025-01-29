from textblob import TextBlob
import pandas as pd
import re
import logging

logger = logging.getLogger(__name__)

def validate_columns(df, required_cols):
    """Validate required columns exist in DataFrame"""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logger.error(f"Missing required columns: {missing}")
        raise ValueError(f"DataFrame missing required columns: {missing}")
    return True

def add_sentiment_features(df):
    """Add sentiment analysis features to DataFrame"""
    try:
        df['sentiment'] = df['message'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df['subjectivity'] = df['message'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
        logger.info("Successfully added sentiment features")
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise
    return df

def encode_categorical_features(df):
    """Encode categorical features with safety checks"""
    try:
        # Check for required columns
        validate_columns(df, ['media'])
        
        # Handle day_of_week if exists
        if 'day_of_week' in df.columns:
            df = pd.get_dummies(df, columns=['day_of_week', 'media'], 
                               prefix=['day', 'media'], dummy_na=False)
        else:
            df = pd.get_dummies(df, columns=['media'], 
                               prefix=['media'], dummy_na=False)
            logger.warning("day_of_week column not found - skipping encoding")
            
        return df
    except Exception as e:
        logger.error(f"Error in categorical encoding: {str(e)}")
        raise

def clean_message(text):
    """Clean message text with null handling"""
    try:
        text = str(text)
        text = re.sub(r'\n', ' ', text)  # Remove newlines
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text.strip()
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return ''

def add_text_features(df):
    """Add additional text features with validation"""
    try:
        validate_columns(df, ['message'])
        df['message_clean'] = df['message'].apply(clean_message)
        df['contains_special_char'] = df['message'].apply(
            lambda x: bool(re.search(r'[^\w\s]', str(x)))
        )
        logger.info("Text features added successfully")
        return df
    except Exception as e:
        logger.error(f"Error adding text features: {str(e)}")
        raise

def create_temporal_features(df):
    """Create time-based features"""
    try:
        validate_columns(df, ['date'])
        df['hour_of_day'] = df['date'].dt.hour
        df['day_of_week'] = df['date'].dt.day_name()
        df['is_weekend'] = df['date'].dt.dayofweek >= 5
        logger.info("Temporal features created successfully")
        return df
    except Exception as e:
        logger.error(f"Error creating temporal features: {str(e)}")
        raise