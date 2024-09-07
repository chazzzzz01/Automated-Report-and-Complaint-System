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

# # Load JSON data into a DataFrame
# with open('complaints.json', 'r') as file:
#     data = json.load(file)

# df = pd.DataFrame(data)

# # Keywords for each office
# office_keywords = {
#         "VP Administration and Finance": ["tuition", "fee", "billing", "financial aid", "parking", "security", "wifi"],

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

# df['description'] = df['description'].apply(preprocess_text)

# # Create a list to hold additional data generated from keywords
# additional_data = []

# # Generate additional descriptions and reports from keywords for each category
# for office, keywords in office_keywords.items():
#     for keyword in keywords:
#         additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
#         additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# # Convert additional data into a DataFrame
# df_additional = pd.DataFrame(additional_data)

# # Combine original data with additional generated data
# df_combined = pd.concat([df, df_additional], ignore_index=True)

# # Split data into training and test sets for both category and type
# X_train, X_test, y_train_category, y_test_category, y_train_type, y_test_type = train_test_split(
#     df_combined['description'], df_combined['category'], df_combined['type'], test_size=0.25, random_state=42
# )

# # Vectorize text data using TF-IDF
# vectorizer = TfidfVectorizer(ngram_range=(1, 3))  # Include trigrams
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # Hyperparameter tuning for Naive Bayes using GridSearchCV (for category prediction)
# param_grid = {'alpha': np.logspace(-3, 1, 10)}
# grid_search_category = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
# grid_search_category.fit(X_train_vec, y_train_category)

# # Best model for category prediction
# best_nb_model_category = grid_search_category.best_estimator_

# # Train a separate model for type prediction (complaint or report)
# type_model = MultinomialNB()
# type_model.fit(X_train_vec, y_train_type)

# # Evaluate both models
# y_pred_category = best_nb_model_category.predict(X_test_vec)
# y_pred_type = type_model.predict(X_test_vec)

# print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
# print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

# print("Classification Report for Category:")
# print(classification_report(y_test_category, y_pred_category))

# print("Classification Report for Type:")
# print(classification_report(y_test_type, y_pred_type))

# # Save both models and the vectorizer
# with open('best_model_category.pkl', 'wb') as category_model_file:
#     pickle.dump(best_nb_model_category, category_model_file)

# with open('best_model_type.pkl', 'wb') as type_model_file:
#     pickle.dump(type_model, type_model_file)

# with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)

# # Example of predicting both category and type for a new description
# new_description = ["More financial aid options should be available."]
# new_description_vec = vectorizer.transform(new_description)
# predicted_category = best_nb_model_category.predict(new_description_vec)[0]
# predicted_type = type_model.predict(new_description_vec)[0]
# print(f"\nPredicted Category for '{new_description[0]}': {predicted_category}")
# print(f"Predicted Type for '{new_description[0]}': {predicted_type}")

# # Vectorize office keywords text data instead of office names
# office_texts = []
# for office, keywords in office_keywords.items():
#     office_text = ' '.join(keywords)  # Combine keywords into a single string
#     office_texts.append(office_text)

# # Transform office keyword texts using the same vectorizer
# office_vectors = vectorizer.transform(office_texts)

# # Calculate cosine similarity between new description vector and office keyword vectors
# similarities = cosine_similarity(new_description_vec, office_vectors).flatten()
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

# Convert data to DataFrame
df = pd.DataFrame(data)

# Keywords for each office
office_keywords = {
     "VP Administration and Finance": [
        "tuition", "fee", "billing", "financial aid", "parking", "security", "wifi", "budget", "audit", "expenses",
        "funding", "grants", "scholarships", "accounting", "revenue", "payroll", "investments", "assets", "liabilities", 
        "financial reports", "costs", "financial planning", "fiscal", "investment portfolio", "insurance", "taxes", 
        "cost control", "audit reports", "procurement", "contract management", "salaries", "benefits", "cost analysis", 
        "financial compliance", "risk management", "budget planning", "expense reporting", "cash flow", "debt management",
        "financial forecasting", "banking", "treasury", "expenditure", "pricing", "asset management", "financial systems", 
        "capital budgeting", "purchase orders", "reconciliation", "account statements", "financial audits", "fund allocation", 
        "financial policies", "resource allocation", "profit and loss", "financial strategy", "account receivable", 
        "account payable", "spending", "financial oversight", "investment strategy", "revenue streams", "financial controls", 
        "financial reporting", "cost management", "overhead", "financial records", "investment analysis", "financial metrics", 
        "spending analysis", "budget review", "cost efficiency", "asset allocation", "financial goals", "audit trails", 
        "operating budget", "financial risk", "fund management", "revenue analysis", "financial governance", "fiscal management", 
        "financial integrity", "capital management", "payroll management", "expense tracking", "financial stability", 
        "financial oversight", "budget adjustments", "fundraising", "financial administration", "budget allocation", 
        "strategic planning", "compliance", "financial performance"
    ],
    "VP Academic Affairs": [
        "library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", 
        "advisors", "curriculum", "grades", "scheduling", "transcripts", "accreditation", "course development", "research",
        "academic policies", "student records", "faculty development", "course catalogs", "enrollment", "academic advising",
        "course schedules", "degree programs", "student assessment", "academic standards", "course materials", "lectures",
        "seminars", "workshops", "academic integrity", "student progress", "academic support", "research grants", "theses",
        "dissertations", "academic publications", "classroom management", "department meetings", "student evaluations",
        "faculty reviews", "academic conferences", "study abroad", "internships", "academic planning", "scholarly activities",
        "academic counseling", "graduate programs", "undergraduate programs", "academic achievements", "learning outcomes",
        "faculty recruitment", "student engagement", "academic workshops", "faculty committees", "course requirements",
        "academic schedules", "course registration", "academic research", "student performance", "academic standards",
        "course offerings", "academic resources", "faculty training", "academic curriculum", "student participation",
        "academic services", "degree requirements", "class participation", "research activities", "academic support services",
        "faculty meetings", "academic committees", "course evaluations", "class schedules", "academic resources", "faculty roles",
        "graduate studies", "student feedback", "academic progress", "research initiatives", "academic planning", "learning objectives",
        "academic planning", "faculty mentorship", "course administration", "academic excellence", "faculty performance"
    ],
    "VP Students and External Affairs": [
        "dormitories", "food", "cafeteria", "sports", "career services", "maintenance", "housing", "student activities",
        "external relations", "outreach", "events", "clubs", "student organizations", "student wellness", "community service",
        "campus life", "student engagement", "external partnerships", "internships", "job placement", "career counseling",
        "student support", "alumni relations", "public relations", "community outreach", "student events", "cultural activities",
        "student advocacy", "recreational activities", "student programs", "external communications", "campus events", "dorm life",
        "student housing", "academic support", "student success", "external affairs", "campus facilities", "student leadership",
        "community involvement", "student volunteering", "student services", "external partnerships", "career development",
        "student initiatives", "student resources", "external events", "dormitory management", "student relations", 
        "event planning", "student activities funding", "student health", "academic events", "extracurricular activities",
        "community engagement", "student satisfaction", "student feedback", "campus safety", "student retention", "service learning",
        "student welfare", "external collaborations", "social activities", "student networks", "housing policies", "career fairs",
        "student mentoring", "campus organizations", "community relations", "student culture", "support services", "student life",
        "event coordination", "student housing policies", "student participation", "career guidance", "campus activities",
        "external communications", "student development", "student outreach", "student networking", "academic support services",
        "campus events coordination", "student engagement activities", "community outreach programs", "student advocacy programs",
        "career development services", "student success programs", "campus resource management", "student feedback systems",
        "external engagement", "student community programs", "campus involvement", "student services administration"
    ],
    "GAD Office": [
        "catcalling", "wolf whistling", "sexual", "gender jokes", "sexual names", "unwanted invitation", "discrimination",
        "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
        "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing",
        "taunting", "gossiping lies", "gender-based", "bullying", "verbal harassment", "non-verbal harassment",
        "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
        "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action", "smacking lips", "underwear",
        "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harassment",
        "aggression", "abuse", "abusive", "abused", "sexual favor", "groping", "grabbing", "breast", "intentionally", "private part",
        "unwanted hugging", "consistent messaging", "buttocks", "genital", "online sexual harassment", "blackmailing", "emotional threats",
        "cyber stalking", "incessant messaging", "unauthorized recording", "impersonating", "negative", "manipulating",
        "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
        "threatening", "threatened", "harassing", "harassed", "pinching", "coercion", "exploitation", "harassment policies",
        "consent", "retaliation", "harassment reporting", "sensitivity training", "awareness", "legal action", "support services",
        "confidentiality", "victim support", "empowerment", "safety measures", "anti-harassment", "equality", "safe spaces",
        "harassment prevention", "victim advocacy", "educational programs", "supportive environment", "inclusive practices",
        "harassment complaints", "intervention", "prevention strategies", "legal protections", "harassment laws", "reporting mechanisms"
    ]
}

# Urgency levels based on certain keywords
urgency_keywords = {
    'high': ['security', 'threat', 'abuse', 'assault', 'harassment', 'urgent', 'immediate', 'critical'],
    'low': ['suggestion', 'improvement', 'request', 'feedback', 'low priority']
}

# Function to determine urgency level
def determine_urgency(description):
    description = description.lower()
    for urgency, keywords in urgency_keywords.items():
        if any(keyword in description for keyword in keywords):
            return urgency
    return 'low'  # Default urgency if no keywords match

# Enhanced text preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# Preprocess text and determine urgency
df['description'] = df['description'].apply(preprocess_text)
df['urgency'] = df['description'].apply(determine_urgency)

# Create a list to hold additional data generated from keywords
additional_data = []

# Generate additional descriptions and reports from keywords for each category
for office, keywords in office_keywords.items():
    for keyword in keywords:
        additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint', 'urgency': determine_urgency(keyword)})
        additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report', 'urgency': determine_urgency(keyword)})

# Convert additional data into a DataFrame
df_additional = pd.DataFrame(additional_data)

# Combine original data with additional generated data
df_combined = pd.concat([df, df_additional], ignore_index=True)

# Split data into training and test sets for category, type, and urgency
X_train, X_test, y_train_category, y_test_category, y_train_type, y_test_type, y_train_urgency, y_test_urgency = train_test_split(
    df_combined['description'], df_combined['category'], df_combined['type'], df_combined['urgency'], test_size=0.25, random_state=42
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

# Train separate models for type and urgency prediction
type_model = MultinomialNB()
type_model.fit(X_train_vec, y_train_type)

urgency_model = MultinomialNB()
urgency_model.fit(X_train_vec, y_train_urgency)

# Evaluate models
y_pred_category = best_nb_model_category.predict(X_test_vec)
y_pred_type = type_model.predict(X_test_vec)
y_pred_urgency = urgency_model.predict(X_test_vec)

print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")
print(f"Urgency Prediction Accuracy: {accuracy_score(y_test_urgency, y_pred_urgency):.2f}")

print("Classification Report for Category:")
print(classification_report(y_test_category, y_pred_category))

print("Classification Report for Type:")
print(classification_report(y_test_type, y_pred_type))

print("Classification Report for Urgency:")
print(classification_report(y_test_urgency, y_pred_urgency))

# Save models and vectorizer
with open('best_model_category.pkl', 'wb') as category_model_file:
    pickle.dump(best_nb_model_category, category_model_file)

with open('best_model_type.pkl', 'wb') as type_model_file:
    pickle.dump(type_model, type_model_file)

with open('best_model_urgency.pkl', 'wb') as urgency_model_file:
    pickle.dump(urgency_model, urgency_model_file)

with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Example prediction
new_description = ["There should be more programs to promote gender equality on campus"]
new_description_vec = vectorizer.transform(new_description)
predicted_category = best_nb_model_category.predict(new_description_vec)[0]
predicted_type = type_model.predict(new_description_vec)[0]
predicted_urgency = urgency_model.predict(new_description_vec)[0]

print(f"\nPredicted Category for '{new_description[0]}': {predicted_category}")
print(f"Predicted Type for '{new_description[0]}': {predicted_type}")
print(f"Predicted Urgency Level for '{new_description[0]}': {predicted_urgency}")
