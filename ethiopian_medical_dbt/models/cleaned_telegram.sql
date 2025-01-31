WITH raw_data AS (
    SELECT * FROM public.cleaned_telegram_messages
)
SELECT 
    id, 
    date, 
    message_clean AS message, 
    sentiment, 
    subjectivity, 
    hour_of_day, 
    day_of_week, 
    is_weekend
FROM raw_data
WHERE message IS NOT NULL;
