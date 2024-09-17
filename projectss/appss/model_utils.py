import os
import pickle

def load_models():
    # Get the directory of the current script
    base_dir = os.path.dirname(__file__)

    # Construct the full path to the model files
    category_model_path = os.path.join(base_dir, 'best_model_category.pkl')
    type_model_path = os.path.join(base_dir, 'best_model_type.pkl')
    vectorizer_path = os.path.join(base_dir, 'best_vectorizer.pkl')

    # Check if the model files exist
    if not os.path.exists(category_model_path):
        raise FileNotFoundError(f"The category model file was not found at {category_model_path}")
    if not os.path.exists(type_model_path):
        raise FileNotFoundError(f"The type model file was not found at {type_model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"The vectorizer file was not found at {vectorizer_path}")

    # Load the category model, type model, and vectorizer using pickle
    with open(category_model_path, 'rb') as category_file:
        category_model = pickle.load(category_file)

    with open(type_model_path, 'rb') as type_file:
        type_model = pickle.load(type_file)

    with open(vectorizer_path, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)

    return category_model, type_model, vectorizer





