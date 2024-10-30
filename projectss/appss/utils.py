import pickle
from langdetect import detect, LangDetectException


def load_models():
    """Load and return the category model, type model, and vectorizer."""
    try:
        # Open and load the category model
        with open('appss/best_model_category.pkl', 'rb') as cat_model_file:
            category_model = pickle.load(cat_model_file)

        # Open and load the type model
        with open('appss/best_model_type.pkl', 'rb') as type_model_file:
            type_model = pickle.load(type_model_file)

        # Open and load the vectorizer
        with open('appss/best_vectorizer.pkl', 'rb') as vec_file:
            vectorizer = pickle.load(vec_file)

        # Return the models
        return category_model, type_model, vectorizer

    except FileNotFoundError as e:
        # Handle case where the model files are not found
        raise FileNotFoundError(f"Model file not found: {e}")
    
    except Exception as e:
        # Handle any other errors
        raise Exception(f"An error occurred while loading models: {e}")


def is_english_text(text):
    """Detect if the given text is in English."""
    try:
        # Detect language using langdetect
        language = detect(text)
        return language == 'en'
    except LangDetectException:
        # Handle cases where detection fails
        return False
