import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

def extract_features(data, feature_type='tfidf'):
    """
    Generic function for feature extraction
    
    Parameters:
        data: input data
        feature_type: type of feature extraction ('tfidf' or 'numerical')
    """
    if feature_type == 'tfidf':
        # Text feature extraction
        vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        features = vectorizer.fit_transform(data)
        
    elif feature_type == 'numerical':
        # Numerical feature extraction and standardization
        scaler = StandardScaler()
        features = scaler.fit_transform(data)
    
    return features

# Usage example
if __name__ == "__main__":
     # Text data example
    text_data = [
        "this is the first document",
        "this is another document",
        "here is some text data"
    ]
    
    # Numerical data example
    numerical_data = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])
    
    # Extract text features
    text_features = extract_features(text_data, 'tfidf')
    print("\nTF-IDF Feature Matrix:")
    print(text_features.toarray())  # Convert sparse matrix to dense matrix for display
    print(f"Feature matrix shape: {text_features.shape}")
    
    # Extract numerical features
    num_features = extract_features(numerical_data, 'numerical')
    print("\nStandardized Numerical Features:")
    print(num_features)
    print(f"Feature matrix shape: {num_features.shape}")
    
