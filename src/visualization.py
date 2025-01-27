# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
from logging_utils import setup_logger

# Set up logging
logger = setup_logger(name='visualization_logger', log_file='logs/visualization.log')

def plot_views_distribution(df):
    """
    Plot the distribution of views.
    """
    logger.info("Plotting distribution of views...")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['views'], bins=30, kde=True)
    plt.title('Distribution of Views')
    plt.xlabel('Views')
    plt.ylabel('Frequency')
    plt.show()

def plot_messages_over_time(df):
    """
    Plot the number of messages over time.
    """
    logger.info("Plotting messages over time...")
    plt.figure(figsize=(12, 6))
    df.set_index('date')['id'].resample('M').count().plot()
    plt.title('Number of Messages Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Messages')
    plt.show()

def plot_messages_by_day(df):
    """
    Plot the number of messages by day of the week.
    """
    logger.info("Plotting messages by day of the week...")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='day_of_week', data=df, order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.title('Number of Messages by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Messages')
    plt.show()

def plot_messages_by_hour(df):
    """
    Plot the number of messages by hour of the day.
    """
    logger.info("Plotting messages by hour of the day...")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='hour', data=df)
    plt.title('Number of Messages by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Messages')
    plt.show()

def plot_messages_with_media(df):
    """
    Plot the proportion of messages with media.
    """
    logger.info("Plotting messages with media...")
    plt.figure(figsize=(6, 4))
    sns.countplot(x='media', data=df)
    plt.title('Messages with Media')
    plt.xlabel('Media (True/False)')
    plt.ylabel('Count')
    plt.show()

def plot_correlation_matrix(df):
    """
    Plot the correlation matrix for numerical columns.
    """
    logger.info("Plotting correlation matrix...")
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[['views', 'message_length', 'word_count']].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
