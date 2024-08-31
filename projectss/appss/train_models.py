
# import numpy as np
# import pandas as pd
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, accuracy_score
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pickle
# import string

# # Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('wordnet')

# # Load JSON data into a DataFrame for complaints, categories, and type
# with open('complaints.json', 'r') as file:
#     data = json.load(file)

# df = pd.DataFrame(data)

# # Keywords for each office
# office_keywords = {
#     "VP Administration and Finance": ["tuition", "fee", "billing", "financial aid", "parking", "security", "wifi"],

#     "VP Academic Affairs": ["library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", "advisors"],
    
#     "VP Students and External Affairs": ["dormitories", "food", "cafeteria", "sports", "career services", "maintenance"],
   
#     "GAD Office": ["catcalling", "wolf whistling","sexual","gender jokes","sexual names","unwanted invitation","discrimination", 
#                    "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
#                    "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing", 
#                    "taunting", "gossiping lies", "gender-based", "bullying", "verbal harrassment", "non-verbal harrasment", 
#                    "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
#                    "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action" "smacking lips", "underwear",
#                    "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harrassment",
#                    "aggression", "abuse", "abusive", "abused", "sexual favor", "grooping", "grabbing", "breast", "intentionally", "private part", 
#                    "unwanted hugging", "consistent messaging", "private part", "buttocks", "genital", "online sexual harrasment", "blackmailing", "emotional threats",
#                    "cyber stalking", "incessant messaging", "incessant message", "unauthorized recording", "impersonating", "negative", "manipulating",
#                    "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
#                    "threating", "threatened", "harrasing", "harrased", "pinching"]
# }

# # Enhanced text preprocessing
# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
#     return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# df['complaint'] = df['complaint'].apply(preprocess_text)

# # Create a list to hold additional data generated from keywords
# additional_data = []

# # Generate additional complaints and reports from keywords for each category
# for office, keywords in office_keywords.items():
#     for keyword in keywords:
#         additional_data.append({'complaint': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
#         additional_data.append({'complaint': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# # Convert additional data into a DataFrame
# df_additional = pd.DataFrame(additional_data)

# # Combine original data with additional generated data
# df_combined = pd.concat([df, df_additional], ignore_index=True)

# # Split data into training and test sets with a slightly different test size to adjust accuracy
# X_train, X_test, y_train, y_test = train_test_split(df_combined['complaint'], df_combined['category'],
#                                                     test_size=0.25, random_state=42)

# # Vectorize text data using TF-IDF with bigrams and trigrams
# vectorizer = TfidfVectorizer(ngram_range=(1, 3))  # Include trigrams
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # Hyperparameter tuning for Naive Bayes using GridSearchCV
# param_grid = {'alpha': np.logspace(-3, 1, 10)}  # Searching through a wide range of alpha values
# grid_search = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
# grid_search.fit(X_train_vec, y_train)

# # Best model after GridSearch
# best_nb_model = grid_search.best_estimator_

# # Train the best model
# best_nb_model.fit(X_train_vec, y_train)

# # Predict on test data using the best model
# y_pred_nb = best_nb_model.predict(X_test_vec)

# # Evaluate model performance
# accuracy = accuracy_score(y_test, y_pred_nb)
# print(f"Accuracy: {accuracy:.2f}\n")

# # Classification report
# print("Classification Report:")
# print(classification_report(y_test, y_pred_nb))

# # Save the best model and vectorizer
# with open('best_model.pkl', 'wb') as model_file:
#     pickle.dump(best_nb_model, model_file)
# with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)

# # Example of predicting category for a new complaint or report and calculating cosine similarity
# new_complaint = ["There is a discrimination issue in the classroom."]
# new_complaint_vec = vectorizer.transform(new_complaint)
# predicted_category = best_nb_model.predict(new_complaint_vec)[0]
# print(f"\nPredicted Category for '{new_complaint[0]}': {predicted_category}")

# # Vectorize office keywords text data instead of office names
# office_texts = []
# for office, keywords in office_keywords.items():
#     office_text = ' '.join(keywords)  # Combine keywords into a single string
#     office_texts.append(office_text)

# # Transform office keyword texts using the same vectorizer
# office_vectors = vectorizer.transform(office_texts)

# # Calculate cosine similarity between new complaint vector and office keyword vectors
# similarities = cosine_similarity(new_complaint_vec, office_vectors).flatten()
# best_match_index = similarities.argmax()
# best_match_office = list(office_keywords.keys())[best_match_index]

# # Display the best matching office
# print(f"Best match office based on cosine similarity: {best_match_office}")



import numpy as np
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import string

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Load JSON data into a DataFrame
with open('complaints.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Keywords for each office
office_keywords = {
        "VP Administration and Finance": ["tuition", "fee", "billing", "financial aid", "parking", "security", "wifi"],

    "VP Academic Affairs": ["library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", "advisors"],
    
    "VP Students and External Affairs": ["dormitories", "food", "cafeteria", "sports", "career services", "maintenance"],
   
    "GAD Office": ["catcalling", "wolf whistling","sexual","gender jokes","sexual names","unwanted invitation","discrimination", 
                   "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
                   "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing", 
                   "taunting", "gossiping lies", "gender-based", "bullying", "verbal harrassment", "non-verbal harrasment", 
                   "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
                   "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action" "smacking lips", "underwear",
                   "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harrassment",
                   "aggression", "abuse", "abusive", "abused", "sexual favor", "grooping", "grabbing", "breast", "intentionally", "private part", 
                   "unwanted hugging", "consistent messaging", "private part", "buttocks", "genital", "online sexual harrasment", "blackmailing", "emotional threats",
                   "cyber stalking", "incessant messaging", "incessant message", "unauthorized recording", "impersonating", "negative", "manipulating",
                   "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
                   "threating", "threatened", "harrasing", "harrased", "pinching"]
}

# Enhanced text preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

df['description'] = df['description'].apply(preprocess_text)

# Create a list to hold additional data generated from keywords
additional_data = []

# Generate additional descriptions and reports from keywords for each category
for office, keywords in office_keywords.items():
    for keyword in keywords:
        additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
        additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# Convert additional data into a DataFrame
df_additional = pd.DataFrame(additional_data)

# Combine original data with additional generated data
df_combined = pd.concat([df, df_additional], ignore_index=True)

# Split data into training and test sets for both category and type
X_train, X_test, y_train_category, y_test_category, y_train_type, y_test_type = train_test_split(
    df_combined['description'], df_combined['category'], df_combined['type'], test_size=0.25, random_state=42
)

# Vectorize text data using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 3))  # Include trigrams
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Hyperparameter tuning for Naive Bayes using GridSearchCV (for category prediction)
param_grid = {'alpha': np.logspace(-3, 1, 10)}
grid_search_category = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
grid_search_category.fit(X_train_vec, y_train_category)

# Best model for category prediction
best_nb_model_category = grid_search_category.best_estimator_

# Train a separate model for type prediction (complaint or report)
type_model = MultinomialNB()
type_model.fit(X_train_vec, y_train_type)

# Evaluate both models
y_pred_category = best_nb_model_category.predict(X_test_vec)
y_pred_type = type_model.predict(X_test_vec)

print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

print("Classification Report for Category:")
print(classification_report(y_test_category, y_pred_category))

print("Classification Report for Type:")
print(classification_report(y_test_type, y_pred_type))

# Save both models and the vectorizer
with open('best_model_category.pkl', 'wb') as category_model_file:
    pickle.dump(best_nb_model_category, category_model_file)

with open('best_model_type.pkl', 'wb') as type_model_file:
    pickle.dump(type_model, type_model_file)

with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Example of predicting both category and type for a new description
new_description = ["More financial aid options should be available."]
new_description_vec = vectorizer.transform(new_description)
predicted_category = best_nb_model_category.predict(new_description_vec)[0]
predicted_type = type_model.predict(new_description_vec)[0]
print(f"\nPredicted Category for '{new_description[0]}': {predicted_category}")
print(f"Predicted Type for '{new_description[0]}': {predicted_type}")

# Vectorize office keywords text data instead of office names
office_texts = []
for office, keywords in office_keywords.items():
    office_text = ' '.join(keywords)  # Combine keywords into a single string
    office_texts.append(office_text)

# Transform office keyword texts using the same vectorizer
office_vectors = vectorizer.transform(office_texts)

# Calculate cosine similarity between new description vector and office keyword vectors
similarities = cosine_similarity(new_description_vec, office_vectors).flatten()
best_match_index = similarities.argmax()
best_match_office = list(office_keywords.keys())[best_match_index]

# Display the best matching office
print(f"Best match office based on cosine similarity: {best_match_office}")