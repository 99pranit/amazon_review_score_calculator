import streamlit as st
from webscrap import get_reviews
from review_preprocessing import clean
from review_preprocessing import tokenize
from tensorflow.keras.models import load_model

# Set the title for the Streamlit app
st.title("Customer Review Score Calculator")

# Text input for product URL
url = st.text_input("Enter Product URL")

if st.button('GET REVIEW SCORE'):
    try:
        # Load the binary classification RNN model
        review_score_model = load_model('review_score_model.keras')
        
        # Get reviews using the custom web scraping function
        reviews = get_reviews(url)
        
        if not reviews:
            st.error("No reviews found for the provided URL.")
        else:
            # Preprocess the reviews
            reviews_cleaned = clean(reviews)
            reviews_tokenized = tokenize(reviews_cleaned)
            
            # Predict sentiment for each review
            predictions = review_score_model.predict(reviews_tokenized)
            
            # Classify predictions
            threshold = 0.5
            positive_count = sum(1 for pred in predictions if pred > threshold)
            negative_count = len(predictions) - positive_count
            
            # Display the results
            st.write(f"Total Reviews Analyzed: {len(predictions)}")
            st.write(f"Positive Reviews: {positive_count}")
            st.write(f"Negative Reviews: {negative_count}")
            
            # Optionally, display results as a bar chart
            st.bar_chart({"Sentiment": ["Positive", "Negative"], 
                          "Count": [positive_count, negative_count]})
    except Exception as e:
        st.error(f"An error occurred: {e}")
