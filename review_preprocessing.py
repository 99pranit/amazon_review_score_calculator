import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing import sequence
import nltk
from nltk.corpus import stopwords
import re

def clean(df):
    """
    Cleans the 'Reviews' column of a DataFrame by removing unwanted characters, 
    converting to lowercase, and removing stopwords.

    Args:
        df (pd.DataFrame): DataFrame containing a column named 'Reviews'.

    Returns:
        pd.Series: Cleaned reviews as a pandas Series.
    """
    try:
        # Ensure the 'Reviews' column exists
        if 'Reviews' not in df.columns:
            raise ValueError("DataFrame must contain a 'Reviews' column.")
        
        # Convert to lowercase and remove digits and special characters
        clean_df = df['Reviews'].str.lower().replace('[^\w\s]', ' ').replace('\d', ' ')
        
        def clean_text(text):
            """
            Removes all characters except alphabets and spaces.
            """
            if isinstance(text, str):
                return re.sub(r'[^a-zA-Z\s]', ' ', text)
            return text
        
        # Apply text cleaning
        clean_df = clean_df.apply(clean_text)
        
        # Download stopwords
        nltk.download('stopwords', quiet=True)
        sw = stopwords.words('english')
        
        # Remove stopwords
        clean_df = clean_df.apply(lambda x: " ".join(word for word in str(x).split() if word not in sw))
        
        return clean_df
    
    except Exception as e:
        print(f"An error occurred during cleaning: {e}")
        return pd.Series(dtype='str')

def tokenize(df):
    """
    Tokenizes and pads the text data.

    Args:
        df (pd.Series): Series of cleaned text data.

    Returns:
        np.ndarray: Tokenized and padded sequences.
    """
    try:
        # Initialize the tokenizer with an out-of-vocabulary token
        tokenizer = Tokenizer(oov_token='<UNK>')
        tokenizer.fit_on_texts(df)
        tokenizer.word_index['<PAD>'] = 0  # Assign PAD token
        
        # Sort words by frequency and trim to VOCAB_SIZE
        word_counts = tokenizer.word_counts
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        VOCAB_SIZE = 30000  # Define vocabulary size
        trimmed_words = sorted_words[:VOCAB_SIZE]
        
        # Create a new tokenizer with the trimmed vocabulary
        trimmed_vocab = [word for word, count in trimmed_words]
        trimmed_tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token='<UNK>')
        trimmed_tokenizer.fit_on_texts(trimmed_vocab)
        
        # Tokenize the text
        tokenized_df = tokenizer.texts_to_sequences(df)
        
        # Pad sequences to ensure uniform length
        tokenized_df = sequence.pad_sequences(tokenized_df, maxlen=105)
        
        return tokenized_df
    
    except Exception as e:
        print(f"An error occurred during tokenization: {e}")
        return np.array([])

