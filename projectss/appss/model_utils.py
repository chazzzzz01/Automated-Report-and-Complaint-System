# import os
# import pickle

# def load_model():
#     # Get the directory of the current script
#     base_dir = os.path.dirname(__file__)

#     # Construct the full path to the model.pkl file
#     model_path = os.path.join(base_dir, 'best_model.pkl')  # Ensure to use the correct file name

#     # Check if the model file exists
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"The model file was not found at {model_path}")

#     # Load the model and vectorizer using pickle
#     with open(model_path, 'rb') as file:
#         model = pickle.load(file)

#     # Load the vectorizer
#     vectorizer_path = os.path.join(base_dir, 'best_vectorizer.pkl')
#     with open(vectorizer_path, 'rb') as file:
#         vectorizer = pickle.load(file)

#     return model, vectorizer


# import os
# import pickle
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.feature_extraction.text import TfidfVectorizer
# from typing import Tuple

# def load_model() -> Tuple[MultinomialNB, TfidfVectorizer]:
#     """
#     Load the trained Naive Bayes model and the associated TF-IDF vectorizer.
    
#     Returns:
#         Tuple[MultinomialNB, TfidfVectorizer]: A tuple containing the trained model and the vectorizer.
        
#     Raises:
#         FileNotFoundError: If the model or vectorizer file is not found.
#     """
#     # Get the directory of the current script
#     base_dir = os.path.dirname(__file__)

#     # Paths to the model and vectorizer files
#     model_path = os.path.join(base_dir, 'best_model.pkl')
#     vectorizer_path = os.path.join(base_dir, 'best_vectorizer.pkl')

#     # Check if the model file exists
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"The model file was not found at {model_path}")

#     # Check if the vectorizer file exists
#     if not os.path.exists(vectorizer_path):
#         raise FileNotFoundError(f"The vectorizer file was not found at {vectorizer_path}")

#     # Load the model and vectorizer using pickle
#     with open(model_path, 'rb') as model_file:
#         model = pickle.load(model_file)

#     with open(vectorizer_path, 'rb') as vectorizer_file:
#         vectorizer = pickle.load(vectorizer_file)

#     return model, vectorizer








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
