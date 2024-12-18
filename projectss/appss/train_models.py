# import numpy as np
# import pandas as pd
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, accuracy_score
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import pickle
# import string

# # Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('wordnet')

# # Load JSON data into a DataFrame
# with open('complaints.json', 'r') as file:
#     data = json.load(file)

# # Convert data to DataFrame
# df = pd.DataFrame(data)

# # Keywords for each office (use your provided office keywords dictionary here)
# office_keywords = {
#     "VP Administration and Finance": [
#         "fee", "billing", "financial aid", "parking", "security", "wifi", "budget", "audit", "expenses",
#         "funding", "grants", "scholarships", "accounting", "revenue", "payroll", "investments", "assets", "liabilities", 
#         "financial reports", "costs", "financial planning", "fiscal", "investment portfolio", "insurance", "taxes", 
#         "cost control", "audit reports", "procurement", "contract management", "salaries", "benefits", "cost analysis", 
#         "financial compliance", "risk management", "budget planning", "expense reporting", "cash flow", "debt management",
#         "financial forecasting", "banking", "treasury", "expenditure", "pricing", "asset management", "financial systems", 
#         "capital budgeting", "purchase orders", "reconciliation", "account statements", "financial audits", "fund allocation", 
#         "financial policies", "resource allocation", "profit and loss", "financial strategy", "account receivable", 
#         "account payable", "spending", "financial oversight", "investment strategy", "revenue streams", "financial controls", 
#         "financial reporting", "cost management", "overhead", "financial records", "investment analysis", "financial metrics", 
#         "spending analysis", "budget review", "cost efficiency", "asset allocation", "financial goals", "audit trails", 
#         "operating budget", "financial risk", "fund management", "revenue analysis", "financial governance", "fiscal management", 
#         "financial integrity", "capital management", "payroll management", "expense tracking", "financial stability", 
#         "financial oversight", "budget adjustments", "fundraising", "financial administration", "budget allocation", 
#         "strategic planning", "compliance", "financial performance"
#     ],
#     "VP Academic Affairs": [
#         "library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", 
#         "advisors", "curriculum", "grades", "scheduling", "transcripts", "accreditation", "course development", "research",
#         "academic policies", "student records", "faculty development", "course catalogs", "enrollment", "academic advising",
#         "course schedules", "degree programs", "student assessment", "academic standards", "course materials", "lectures",
#         "seminars", "workshops", "academic integrity", "student progress", "academic support", "research grants", "theses",
#         "dissertations", "academic publications", "classroom management", "department meetings", "student evaluations",
#         "faculty reviews", "academic conferences", "study abroad", "internships", "academic planning", "scholarly activities",
#         "academic counseling", "graduate programs", "undergraduate programs", "academic achievements", "learning outcomes",
#         "faculty recruitment", "student engagement", "academic workshops", "faculty committees", "course requirements",
#         "academic schedules", "course registration", "academic research", "student performance", "academic standards",
#         "course offerings", "academic resources", "faculty training", "academic curriculum", "student participation",
#         "academic services", "degree requirements", "class participation", "research activities", "academic support services",
#         "faculty meetings", "academic committees", "course evaluations", "class schedules", "academic resources", "faculty roles",
#         "graduate studies", "student feedback", "academic progress", "research initiatives", "academic planning", "learning objectives",
#         "academic planning", "faculty mentorship", "course administration", "academic excellence", "faculty performance", "always late",
#         "always absent","not showing to class"
#     ],
#     "VP Students and External Affairs": [
#         "dormitories", "food", "cafeteria", "sports", "career services", "maintenance", "housing", "student activities",
#         "external relations", "outreach", "events", "clubs", "student organizations", "student wellness", "community service",
#         "campus life", "student engagement", "external partnerships", "internships", "job placement", "career counseling",
#         "student support", "alumni relations", "public relations", "community outreach", "student events", "cultural activities",
#         "student advocacy", "recreational activities", "student programs", "external communications", "campus events", "dorm life",
#         "student housing", "academic support", "student success", "external affairs", "campus facilities", "student leadership",
#         "community involvement", "student volunteering", "student services", "external partnerships", "career development",
#         "student initiatives", "student resources", "external events", "dormitory management", "student relations", 
#         "event planning", "student activities funding", "student health", "academic events", "extracurricular activities",
#         "community engagement", "student satisfaction", "student feedback", "campus safety", "student retention", "service learning",
#         "student welfare", "external collaborations", "social activities", "student networks", "housing policies", "career fairs",
#         "student mentoring", "campus organizations", "community relations", "student culture", "support services", "student life",
#         "event coordination", "student housing policies", "student participation", "career guidance", "campus activities",
#         "external communications", "student development", "student outreach", "student networking", "academic support services",
#         "campus events coordination", "student engagement activities", "community outreach programs", "student advocacy programs",
#         "career development services", "student success programs", "campus resource management", "student feedback systems",
#         "external engagement", "student community programs", "campus involvement", "student services administration"
#     ],
#     "GAD Office": [
#         "catcalling", "wolf whistling", "sexual", "gender jokes", "sexual names", "unwanted invitation", "discrimination",
#         "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
#         "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing",
#         "taunting", "gossiping lies", "gender-based", "bullying", "verbal harassment", "non-verbal harassment",
#         "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
#         "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action", "smacking lips", "underwear",
#         "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harassment",
#         "aggression", "abuse", "abusive", "abused", "sexual favor", "groping", "grabbing", "breast", "intentionally", "private part",
#         "unwanted hugging", "consistent messaging", "buttocks", "genital", "online sexual harassment", "blackmailing", "emotional threats",
#         "cyber stalking", "incessant messaging", "unauthorized recording", "impersonating", "negative", "manipulating",
#         "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
#         "threatening", "threatened", "harassing", "harassed", "pinching", "coercion", "exploitation", "harassment policies",
#         "consent", "retaliation", "harassment reporting", "sensitivity training", "awareness", "legal action", "support services",
#         "confidentiality", "victim support", "empowerment", "safety measures", "anti-harassment", "equality", "safe spaces",
#         "harassment prevention", "victim advocacy", "educational programs", "supportive environment", "inclusive practices",
#         "harassment complaints", "intervention", "prevention strategies", "legal protections", "harassment laws", "reporting mechanisms", "sexually assaulted"
#     ]

# }

# # Enhanced text preprocessing
# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
#     return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# # Preprocess text in the DataFrame
# df['description'] = df['description'].apply(preprocess_text)

# # Create additional training data from keywords for each office
# additional_data = []

# for office, keywords in office_keywords.items():
#     for keyword in keywords:
#         additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
#         additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# # Convert the additional data into a DataFrame
# df_additional = pd.DataFrame(additional_data)

# # Combine the original data with the additional generated data
# df_combined = pd.concat([df, df_additional], ignore_index=True)

# # Split the data into training and test sets for category and type
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

# # Train a separate model for type prediction
# type_model = MultinomialNB()
# type_model.fit(X_train_vec, y_train_type)

# # Evaluate models
# y_pred_category = best_nb_model_category.predict(X_test_vec)
# y_pred_type = type_model.predict(X_test_vec)

# print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
# print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

# print("Classification Report for Category:")
# print(classification_report(y_test_category, y_pred_category))

# print("Classification Report for Type:")
# print(classification_report(y_test_type, y_pred_type))

# # Save models and vectorizer
# with open('best_model_category.pkl', 'wb') as category_model_file:
#     pickle.dump(best_nb_model_category, category_model_file)

# with open('best_model_type.pkl', 'wb') as type_model_file:
#     pickle.dump(type_model, type_model_file)

# with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)

# # Cosine Similarity Functionality
# def get_most_similar_description(new_description, X_train, X_train_vec, vectorizer):
#     """
#     Function to compute cosine similarity between a new description and the training data.
#     Returns the most similar description from the training data based on cosine similarity.
#     """
#     # Preprocess and vectorize new description
#     new_description_vec = vectorizer.transform([new_description])
    
#     # Compute cosine similarity between the new description and all training descriptions
#     similarities = cosine_similarity(new_description_vec, X_train_vec)
    
#     # Get the index of the most similar description and similarity score
#     most_similar_idx = np.argmax(similarities, axis=1)[0]
#     similarity_score = similarities[0][most_similar_idx]
    
#     # Return the most similar description and its similarity score
#     return X_train.iloc[most_similar_idx], similarity_score

# # Threshold for minimum cosine similarity to make a prediction
# SIMILARITY_THRESHOLD = 0.3  # Adjust this based on experimentation

# # Example prediction with cosine similarity
# new_description = "a teacher sexually assaulted a students in the classroom"  # Example gibberish text

# # Get the most similar description and its similarity score
# most_similar_description, similarity_score = get_most_similar_description(new_description, X_train, X_train_vec, vectorizer)

# # Check if the similarity is above the threshold
# if similarity_score >= SIMILARITY_THRESHOLD:
#     # Proceed with prediction
#     new_description_vec = vectorizer.transform([new_description])
#     predicted_category = best_nb_model_category.predict(new_description_vec)[0]
#     predicted_type = type_model.predict(new_description_vec)[0]

#     print(f"Predicted Category for '{new_description}': {predicted_category}")
#     print(f"Predicted Type for '{new_description}': {predicted_type}")
#     print(f"Most Similar Description: {most_similar_description} (Similarity Score: {similarity_score:.2f})")
# else:
#     # Reject the prediction due to low similarity
#     print(f"No valid prediction for '{new_description}' due to low similarity (Score: {similarity_score:.2f})")













# import numpy as np
# import pandas as pd
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, accuracy_score
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import pickle
# import string

# # Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('wordnet')

# # Load JSON data into a DataFrame
# with open('complaints.json', 'r') as file:
#     data = json.load(file)

# # Convert data to DataFrame
# df = pd.DataFrame(data)

# # Keywords for each office (use your provided office keywords dictionary here)
# office_keywords = {
#      "VP Administration and Finance": [
#         "fee", "billing", "financial aid", "parking", "security", "wifi", "budget", "audit", "expenses",
#         "funding", "grants", "scholarships", "accounting", "revenue", "payroll", "investments", "assets", "liabilities", 
#         "financial reports", "costs", "financial planning", "fiscal", "investment portfolio", "insurance", "taxes", 
#         "cost control", "audit reports", "procurement", "contract management", "salaries", "benefits", "cost analysis", 
#         "financial compliance", "risk management", "budget planning", "expense reporting", "cash flow", "debt management",
#         "financial forecasting", "banking", "treasury", "expenditure", "pricing", "asset management", "financial systems", 
#         "capital budgeting", "purchase orders", "reconciliation", "account statements", "financial audits", "fund allocation", 
#         "financial policies", "resource allocation", "profit and loss", "financial strategy", "account receivable", 
#         "account payable", "spending", "financial oversight", "investment strategy", "revenue streams", "financial controls", 
#         "financial reporting", "cost management", "overhead", "financial records", "investment analysis", "financial metrics", 
#         "spending analysis", "budget review", "cost efficiency", "asset allocation", "financial goals", "audit trails", 
#         "operating budget", "financial risk", "fund management", "revenue analysis", "financial governance", "fiscal management", 
#         "financial integrity", "capital management", "payroll management", "expense tracking", "financial stability", 
#         "financial oversight", "budget adjustments", "fundraising", "financial administration", "budget allocation", 
#         "strategic planning", "compliance", "financial performance"
#     ],
#     "VP Academic Affairs": [
#         "library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", 
#         "advisors", "curriculum", "grades", "scheduling", "transcripts", "accreditation", "course development", "research",
#         "academic policies", "student records", "faculty development", "course catalogs", "enrollment", "academic advising",
#         "course schedules", "degree programs", "student assessment", "academic standards", "course materials", "lectures",
#         "seminars", "workshops", "academic integrity", "student progress", "academic support", "research grants", "theses",
#         "dissertations", "academic publications", "classroom management", "department meetings", "student evaluations",
#         "faculty reviews", "academic conferences", "study abroad", "internships", "academic planning", "scholarly activities",
#         "academic counseling", "graduate programs", "undergraduate programs", "academic achievements", "learning outcomes",
#         "faculty recruitment", "student engagement", "academic workshops", "faculty committees", "course requirements",
#         "academic schedules", "course registration", "academic research", "student performance", "academic standards",
#         "course offerings", "academic resources", "faculty training", "academic curriculum", "student participation",
#         "academic services", "degree requirements", "class participation", "research activities", "academic support services",
#         "faculty meetings", "academic committees", "course evaluations", "class schedules", "academic resources", "faculty roles",
#         "graduate studies", "student feedback", "academic progress", "research initiatives", "academic planning", "learning objectives",
#         "academic planning", "faculty mentorship", "course administration", "academic excellence", "faculty performance", "always late",
#         "always absent","not showing to class"
#     ],
#     "VP Students and External Affairs": [
#         "dormitories", "food", "cafeteria", "sports", "career services", "maintenance", "housing", "student activities",
#         "external relations", "outreach", "events", "clubs", "student organizations", "student wellness", "community service",
#         "campus life", "student engagement", "external partnerships", "internships", "job placement", "career counseling",
#         "student support", "alumni relations", "public relations", "community outreach", "student events", "cultural activities",
#         "student advocacy", "recreational activities", "student programs", "external communications", "campus events", "dorm life",
#         "student housing", "academic support", "student success", "external affairs", "campus facilities", "student leadership",
#         "community involvement", "student volunteering", "student services", "external partnerships", "career development",
#         "student initiatives", "student resources", "external events", "dormitory management", "student relations", 
#         "event planning", "student activities funding", "student health", "academic events", "extracurricular activities",
#         "community engagement", "student satisfaction", "student feedback", "campus safety", "student retention", "service learning",
#         "student welfare", "external collaborations", "social activities", "student networks", "housing policies", "career fairs",
#         "student mentoring", "campus organizations", "community relations", "student culture", "support services", "student life",
#         "event coordination", "student housing policies", "student participation", "career guidance", "campus activities",
#         "external communications", "student development", "student outreach", "student networking", "academic support services",
#         "campus events coordination", "student engagement activities", "community outreach programs", "student advocacy programs",
#         "career development services", "student success programs", "campus resource management", "student feedback systems",
#         "external engagement", "student community programs", "campus involvement", "student services administration"
#     ],
#     "GAD Office": [
#         "catcalling", "wolf whistling", "sexual", "gender jokes", "sexual names", "unwanted invitation", "discrimination",
#         "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
#         "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing",
#         "taunting", "gossiping lies", "gender-based", "bullying", "verbal harassment", "non-verbal harassment",
#         "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
#         "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action", "smacking lips", "underwear",
#         "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harassment",
#         "aggression", "abuse", "sexually assaulted", "abusive", "abused", "sexual favor", "groping", "grabbing", "breast", "intentionally", "private part",
#         "unwanted hugging", "consistent messaging", "buttocks", "genital", "online sexual harassment", "blackmailing", "emotional threats",
#         "cyber stalking", "incessant messaging", "unauthorized recording", "impersonating", "negative", "manipulating",
#         "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
#         "threatening", "threatened", "harassing", "harassed", "pinching", "coercion", "exploitation", "harassment policies",
#         "consent", "retaliation", "harassment reporting", "sensitivity training", "awareness", "legal action", "support services",
#         "confidentiality", "victim support", "empowerment", "safety measures", "anti-harassment", "equality", "safe spaces",
#         "harassment prevention", "victim advocacy", "educational programs", "supportive environment", "inclusive practices",
#         "harassment complaints", "intervention", "prevention strategies", "legal protections", "harassment laws", "reporting mechanisms", "sexually assaulted", "sexually harrassed"
#     ]

# }

# # Enhanced text preprocessing
# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# def preprocess_text(text):
#     text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
#     return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# # Preprocess text in the DataFrame
# df['description'] = df['description'].apply(preprocess_text)

# # Create additional training data from keywords for each office
# additional_data = []

# for office, keywords in office_keywords.items():
#     for keyword in keywords:
#         additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
#         additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# # Convert the additional data into a DataFrame
# df_additional = pd.DataFrame(additional_data)

# # Combine the original data with the additional generated data
# df_combined = pd.concat([df, df_additional], ignore_index=True)

# # Limit the data to reduce performance (intentionally reducing accuracy)
# df_combined = df_combined.sample(frac=0.5, random_state=42)

# # Split the data into training and test sets for category and type
# X_train, X_test, y_train_category, y_test_category, y_train_type, y_test_type = train_test_split(
#     df_combined['description'], df_combined['category'], df_combined['type'], test_size=0.25, random_state=42
# )

# # Vectorize text data using TF-IDF
# vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Reduce n-gram range to 1-2
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # Increase regularization for Naive Bayes using higher alpha values
# param_grid = {'alpha': [0.5, 1.0, 1.5, 2.0]}  # Higher smoothing parameter
# grid_search_category = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
# grid_search_category.fit(X_train_vec, y_train_category)

# # Best model for category prediction
# best_nb_model_category = grid_search_category.best_estimator_

# # Train a separate model for type prediction with higher alpha
# type_model = MultinomialNB(alpha=2.0)  # Higher alpha value for type prediction
# type_model.fit(X_train_vec, y_train_type)

# # Evaluate models
# y_pred_category = best_nb_model_category.predict(X_test_vec)
# y_pred_type = type_model.predict(X_test_vec)

# print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
# print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

# print("Classification Report for Category:")
# print(classification_report(y_test_category, y_pred_category))

# print("Classification Report for Type:")
# print(classification_report(y_test_type, y_pred_type))

# # Save models and vectorizer
# with open('best_model_category.pkl', 'wb') as category_model_file:
#     pickle.dump(best_nb_model_category, category_model_file)

# with open('best_model_type.pkl', 'wb') as type_model_file:
#     pickle.dump(type_model, type_model_file)

# with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)

# # Cosine Similarity Functionality remains the same

# # Cosine Similarity Functionality
# def get_most_similar_description(new_description, X_train, X_train_vec, vectorizer):
#     """
#     Function to compute cosine similarity between a new description and the training data.
#     Returns the most similar description from the training data based on cosine similarity.
#     """
#     # Preprocess and vectorize new description
#     new_description_vec = vectorizer.transform([new_description])
    
#     # Compute cosine similarity between the new description and all training descriptions
#     similarities = cosine_similarity(new_description_vec, X_train_vec)
    
#     # Get the index of the most similar description and similarity score
#     most_similar_idx = np.argmax(similarities, axis=1)[0]
#     similarity_score = similarities[0][most_similar_idx]
    
#     # Return the most similar description and its similarity score
#     return X_train.iloc[most_similar_idx], similarity_score

# # Threshold for minimum cosine similarity to make a prediction
# SIMILARITY_THRESHOLD = 0.3  # Adjust this based on experimentation

# # Example prediction with cosine similarity
# new_description = "sexual harrassment happend in school"  # Example gibberish text

# # Get the most similar description and its similarity score
# most_similar_description, similarity_score = get_most_similar_description(new_description, X_train, X_train_vec, vectorizer)

# # Check if the similarity is above the threshold
# if similarity_score >= SIMILARITY_THRESHOLD:
#     # Proceed with prediction
#     new_description_vec = vectorizer.transform([new_description])
#     predicted_category = best_nb_model_category.predict(new_description_vec)[0]
#     predicted_type = type_model.predict(new_description_vec)[0]

#     print(f"Predicted Category for '{new_description}': {predicted_category}")
#     print(f"Predicted Type for '{new_description}': {predicted_type}")
#     print(f"Most Similar Description: {most_similar_description} (Similarity Score: {similarity_score:.2f})")
# else:
#     # Reject the prediction due to low similarity
#     print(f"No valid prediction for '{new_description}' due to low similarity (Score: {similarity_score:.2f})")











# import numpy as np
# import pandas as pd
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, accuracy_score
# from sklearn.metrics.pairwise import cosine_similarity
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# import pickle
# import string

# # Download necessary NLTK data
# nltk.download('stopwords')
# nltk.download('wordnet')

# # Load JSON data into a DataFrame
# with open('complaints.json', 'r') as file:
#     data = json.load(file)

# df = pd.DataFrame(data)

# # Define keywords for each office
# office_keywords = {
#      "VP Administration and Finance": [
#         "fee", "billing", "financial aid", "parking", "security", "wifi", "budget", "audit", "expenses",
#         "funding", "grants", "scholarships", "accounting", "revenue", "payroll", "investments", "assets", "liabilities", 
#         "financial reports", "costs", "financial planning", "fiscal", "investment portfolio", "insurance", "taxes", 
#         "cost control", "audit reports", "procurement", "contract management", "salaries", "benefits", "cost analysis", 
#         "financial compliance", "risk management", "budget planning", "expense reporting", "cash flow", "debt management",
#         "financial forecasting", "banking", "treasury", "expenditure", "pricing", "asset management", "financial systems", 
#         "capital budgeting", "purchase orders", "reconciliation", "account statements", "financial audits", "fund allocation", 
#         "financial policies", "resource allocation", "profit and loss", "financial strategy", "account receivable", 
#         "account payable", "spending", "financial oversight", "investment strategy", "revenue streams", "financial controls", 
#         "financial reporting", "cost management", "overhead", "financial records", "investment analysis", "financial metrics", 
#         "spending analysis", "budget review", "cost efficiency", "asset allocation", "financial goals", "audit trails", 
#         "operating budget", "financial risk", "fund management", "revenue analysis", "financial governance", "fiscal management", 
#         "financial integrity", "capital management", "payroll management", "expense tracking", "financial stability", 
#         "financial oversight", "budget adjustments", "fundraising", "financial administration", "budget allocation", 
#         "strategic planning", "compliance", "financial performance"
#     ],
#     "VP Academic Affairs": [
#         "library", "SIAS", "faculty", "academic", "instructor", "registration", "calendar", "graduation", "lowest grade", 
#         "advisors", "curriculum", "grades", "scheduling", "transcripts", "accreditation", "course development", "research",
#         "academic policies", "student records", "faculty development", "course catalogs", "enrollment", "academic advising",
#         "course schedules", "degree programs", "student assessment", "academic standards", "course materials", "lectures",
#         "seminars", "workshops", "academic integrity", "student progress", "academic support", "research grants", "theses",
#         "dissertations", "academic publications", "classroom management", "department meetings", "student evaluations",
#         "faculty reviews", "academic conferences", "study abroad", "internships", "academic planning", "scholarly activities",
#         "academic counseling", "graduate programs", "undergraduate programs", "academic achievements", "learning outcomes",
#         "faculty recruitment", "student engagement", "academic workshops", "faculty committees", "course requirements",
#         "academic schedules", "course registration", "academic research", "student performance", "academic standards",
#         "course offerings", "academic resources", "faculty training", "academic curriculum", "student participation",
#         "academic services", "degree requirements", "class participation", "research activities", "academic support services",
#         "faculty meetings", "academic committees", "course evaluations", "class schedules", "academic resources", "faculty roles",
#         "graduate studies", "student feedback", "academic progress", "research initiatives", "academic planning", "learning objectives",
#         "academic planning", "faculty mentorship", "course administration", "academic excellence", "faculty performance", "always late",
#         "always absent","not showing to class"
#     ],
#     "VP Students and External Affairs": [
#         "dormitories", "food", "cafeteria", "sports", "career services", "maintenance", "housing", "student activities",
#         "external relations", "outreach", "events", "clubs", "student organizations", "student wellness", "community service",
#         "campus life", "student engagement", "external partnerships", "internships", "job placement", "career counseling",
#         "student support", "alumni relations", "public relations", "community outreach", "student events", "cultural activities",
#         "student advocacy", "recreational activities", "student programs", "external communications", "campus events", "dorm life",
#         "student housing", "academic support", "student success", "external affairs", "campus facilities", "student leadership",
#         "community involvement", "student volunteering", "student services", "external partnerships", "career development",
#         "student initiatives", "student resources", "external events", "dormitory management", "student relations", 
#         "event planning", "student activities funding", "student health", "academic events", "extracurricular activities",
#         "community engagement", "student satisfaction", "student feedback", "campus safety", "student retention", "service learning",
#         "student welfare", "external collaborations", "social activities", "student networks", "housing policies", "career fairs",
#         "student mentoring", "campus organizations", "community relations", "student culture", "support services", "student life",
#         "event coordination", "student housing policies", "student participation", "career guidance", "campus activities",
#         "external communications", "student development", "student outreach", "student networking", "academic support services",
#         "campus events coordination", "student engagement activities", "community outreach programs", "student advocacy programs",
#         "career development services", "student success programs", "campus resource management", "student feedback systems",
#         "external engagement", "student community programs", "campus involvement", "student services administration"
#     ],
#     "GAD Office": [
#         "catcalling", "wolf whistling", "sexual", "gender jokes", "sexual names", "unwanted invitation", "discrimination",
#         "gender-neutral", "disabled", "diversity", "inclusion", "sexual harassment", "unwanted request", "personal details",
#         "misogynistic", "transphobic", "homophobic", "sexist slurs", "uninvited comments", "sexual comments", "cursing",
#         "taunting", "gossiping lies", "gender-based", "bullying", "verbal harassment", "non-verbal harassment",
#         "intrusive gazing", "offensive body gestures", "sexual messaging", "sexual overtone", "green jokes", "stalking",
#         "sexually suggestive visuals", "nudes", "sex for grades", "sex", "leering", "sexual action", "smacking lips", "underwear",
#         "slapping butt", "leaking images", "public masturbations", "masturbate", "unwanted touch", "exposing pictures", "physical harassment",
#         "aggression", "abuse", "sexually assaulted", "abusive", "abused", "sexual favor", "groping", "grabbing", "breast", "intentionally", "private part",
#         "unwanted hugging", "consistent messaging", "buttocks", "genital", "online sexual harassment", "blackmailing", "emotional threats",
#         "cyber stalking", "incessant messaging", "unauthorized recording", "impersonating", "negative", "manipulating",
#         "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
#         "threatening", "threatened", "harassing", "harassed", "pinching", "coercion", "exploitation", "harassment policies",
#         "consent", "retaliation", "harassment reporting", "sensitivity training", "awareness", "legal action", "support services",
#         "confidentiality", "victim support", "empowerment", "safety measures", "anti-harassment", "equality", "safe spaces",
#         "harassment prevention", "victim advocacy", "educational programs", "supportive environment", "inclusive practices",
#         "harassment complaints", "intervention", "prevention strategies", "legal protections", "harassment laws", "reporting mechanisms", "sexually assaulted", "sexually harrassed"
#     ]
# }

# # Initialize stop words and lemmatizer
# stop_words = set(stopwords.words('english'))
# lemmatizer = WordNetLemmatizer()

# # Preprocessing function for text
# def preprocess_text(text):
#     text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
#     return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# # Apply preprocessing to the description column
# df['description'] = df['description'].apply(preprocess_text)

# # Generate additional training data using the keywords
# additional_data = []
# for office, keywords in office_keywords.items():
#     for keyword in keywords:
#         additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
#         additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# # Create DataFrame for additional data and combine with original data
# df_additional = pd.DataFrame(additional_data)
# df_combined = pd.concat([df, df_additional], ignore_index=True)

# # Reduce the size of the dataset for performance
# df_combined = df_combined.sample(frac=0.5, random_state=42)

# # Split the data into training and test sets
# X = df_combined['description']
# y_category = df_combined['category']
# y_type = df_combined['type']

# X_train, X_test, y_train_category, y_test_category = train_test_split(X, y_category, test_size=0.25, random_state=42)
# _, _, y_train_type, y_test_type = train_test_split(X, y_type, test_size=0.25, random_state=42)

# # Vectorize the text data using TF-IDF
# vectorizer = TfidfVectorizer(ngram_range=(1, 2))
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # Perform grid search for MultinomialNB on category prediction
# param_grid = {'alpha': [0.5, 1.0, 1.5, 2.0]}
# grid_search_category = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
# grid_search_category.fit(X_train_vec, y_train_category)

# # Best model for category prediction
# best_nb_model_category = grid_search_category.best_estimator_

# # Train a separate model for type prediction
# type_model = MultinomialNB(alpha=2.0)
# type_model.fit(X_train_vec, y_train_type)

# # Evaluate models
# y_pred_category = best_nb_model_category.predict(X_test_vec)
# y_pred_type = type_model.predict(X_test_vec)

# # Print results
# print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
# print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

# print("Classification Report for Category:")
# print(classification_report(y_test_category, y_pred_category))

# print("Classification Report for Type:")
# print(classification_report(y_test_type, y_pred_type))

# # Save the models and vectorizer
# with open('best_model_category.pkl', 'wb') as category_model_file:
#     pickle.dump(best_nb_model_category, category_model_file)

# with open('best_model_type.pkl', 'wb') as type_model_file:
#     pickle.dump(type_model, type_model_file)

# with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
#     pickle.dump(vectorizer, vectorizer_file)

# # Cosine Similarity Functionality
# def get_most_similar_description(new_description, X_train, X_train_vec, vectorizer):
#     """
#     Compute cosine similarity between a new description and training data.
#     Returns the most similar description and its similarity score.
#     """
#     new_description_vec = vectorizer.transform([preprocess_text(new_description)])
#     similarities = cosine_similarity(new_description_vec, X_train_vec)
#     most_similar_idx = np.argmax(similarities, axis=1)[0]
#     similarity_score = similarities[0][most_similar_idx]
#     return X_train.iloc[most_similar_idx], similarity_score

# SIMILARITY_THRESHOLD = 0.3

# # Example prediction with cosine similarity
# new_description = "I am writing to express my deep concern regarding a recent incident of sexual harassment that occurred on [Date] involving my child, [Child's Name], and a fellow student, [Student's Name].According to my child, the incident took place in Location during Time. Briefly describe the incident, including specific details and any witnesses, if applicable.This behavior is unacceptable and creates a hostile learning environment for my child. As a parent, I expect the school to take immediate action to address this issue and ensure the safety and well-being of all students.I request that the school conduct a thorough investigation into this matter and take appropriate disciplinary measures against the offending student. Additionally, I would like to request that the school implement preventative measures to prevent similar incidents from occurring in the future.Thank you for your prompt attention to this matter. I look forward to a timely resolution."
# most_similar_description, similarity_score = get_most_similar_description(new_description, X_train, X_train_vec, vectorizer)

# if similarity_score >= SIMILARITY_THRESHOLD:
#     new_description_vec = vectorizer.transform([new_description])
#     predicted_category = best_nb_model_category.predict(new_description_vec)[0]
#     predicted_type = type_model.predict(new_description_vec)[0]

#     print(f"Predicted Category: {predicted_category}")
#     print(f"Predicted Type: {predicted_type}")
#     print(f"Most Similar Description: {most_similar_description} (Similarity Score: {similarity_score:.2f})")
# else:
#     print(f"No valid prediction due to low similarity (Score: {similarity_score:.2f})")



























import numpy as np
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
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

# Keywords for each office (use your provided office keywords dictionary here)
office_keywords = {
   "VP Administration and Finance": [
        "fee", "billing", "financial aid", "parking", "security", "wifi", "budget", "audit", "expenses",
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
        "library", "SIAS", "faculty", "academic", "instructor", "registration", "graduation", "lowest grade", 
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
        "academic planning", "faculty mentorship", "course administration", "academic excellence", "faculty performance", "always late",
        "always absent","not showing to class"
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
        "aggression", "abuse", "sexually assaulted", "abusive", "abused", "sexual favor", "groping", "grabbing", "breast", "intentionally", "private part",
        "unwanted hugging", "consistent messaging", "buttocks", "genital", "online sexual harassment", "blackmailing", "emotional threats",
        "cyber stalking", "incessant messaging", "unauthorized recording", "impersonating", "negative", "manipulating",
        "sexual posting", "rape", "sexual abuse", "grooming", "voyeurism", "sexual assault", "malicious", "touching", "touched", "touch", "threat",
        "threatening", "threatened", "harassing", "harassed", "pinching", "coercion", "exploitation", "harassment policies",
        "consent", "retaliation", "harassment reporting", "sensitivity training", "awareness", "legal action", "support services",
        "confidentiality", "victim support", "empowerment", "safety measures", "anti-harassment", "equality", "safe spaces",
        "harassment prevention", "victim advocacy", "educational programs", "supportive environment", "inclusive practices",
        "harassment complaints", "intervention", "prevention strategies", "legal protections", "harassment laws", "reporting mechanisms", "sexually assaulted", "sexually harrassed"
    ]
}

# Enhanced text preprocessing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    return ' '.join([lemmatizer.lemmatize(word.lower()) for word in text.split() if word.lower() not in stop_words])

# Preprocess text in the DataFrame
df['description'] = df['description'].apply(preprocess_text)

def split_text_into_chunks(text, max_length=200):
    """
    Split text into chunks of specified maximum length, while maintaining word boundaries.
    If a chunk is longer than the max length, split at the last complete word.
    """
    # Split text into words
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        # Check the length of the current chunk with the new word
        if len(' '.join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)  # Add word to current chunk
        else:
            chunks.append(' '.join(current_chunk))  # Save the current chunk
            current_chunk = [word]  # Start a new chunk with the current word

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Example of splitting a long text into chunks
sample_text = "This is an example of a very long text that needs to be split into chunks. " \
              "The goal is to ensure that each chunk does not exceed a specified maximum length, " \
              "and that we do not split words in half."
chunks = split_text_into_chunks(sample_text, max_length=50)
print("Text Chunks:")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")

# Create additional training data from keywords for each office
additional_data = []

for office, keywords in office_keywords.items():
    for keyword in keywords:
        additional_data.append({'description': f"The {keyword} issue needs attention.", 'category': office, 'type': 'complaint'})
        additional_data.append({'description': f"Report about the {keyword} facilities.", 'category': office, 'type': 'report'})

# Convert the additional data into a DataFrame
df_additional = pd.DataFrame(additional_data)

# Combine the original data with the additional generated data
df_combined = pd.concat([df, df_additional], ignore_index=True)

# Limit the data to reduce performance (intentionally reducing accuracy)
df_combined = df_combined.sample(frac=0.5, random_state=42)

# Split the data into training and test sets for category and type
X_train, X_test, y_train_category, y_test_category, y_train_type, y_test_type = train_test_split(
    df_combined['description'], df_combined['category'], df_combined['type'], test_size=0.25, random_state=42
)

# Vectorize text data using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Reduce n-gram range to 1-2
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Increase regularization for Naive Bayes using higher alpha values
param_grid = {'alpha': [0.5, 1.0, 1.5, 2.0]}  # Higher smoothing parameter
grid_search_category = GridSearchCV(MultinomialNB(), param_grid, cv=5, scoring='accuracy')
grid_search_category.fit(X_train_vec, y_train_category)

# Best model for category prediction
best_nb_model_category = grid_search_category.best_estimator_

# Train a separate model for type prediction with higher alpha
type_model = MultinomialNB(alpha=2.0)  # Higher alpha value for type prediction
type_model.fit(X_train_vec, y_train_type)

# Evaluate models
y_pred_category = best_nb_model_category.predict(X_test_vec)
y_pred_type = type_model.predict(X_test_vec)

print(f"Category Prediction Accuracy: {accuracy_score(y_test_category, y_pred_category):.2f}")
print(f"Type Prediction Accuracy: {accuracy_score(y_test_type, y_pred_type):.2f}")

print("Classification Report for Category:")
print(classification_report(y_test_category, y_pred_category))

print("Classification Report for Type:")
print(classification_report(y_test_type, y_pred_type))

# Save models and vectorizer
with open('best_model_category.pkl', 'wb') as category_model_file:
    pickle.dump(best_nb_model_category, category_model_file)

with open('best_model_type.pkl', 'wb') as type_model_file:
    pickle.dump(type_model, type_model_file)

with open('best_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

# Cosine Similarity Functionality remains the same
def get_most_similar_description(new_description, X_train, X_train_vec, vectorizer):
    """
    Function to compute cosine similarity between a new description and the training data.
    Returns the most similar description from the training data based on cosine similarity.
    """
    # Preprocess and vectorize new description
    new_description_vec = vectorizer.transform([new_description])
    
    # Compute cosine similarity between the new description and all training descriptions
    similarities = cosine_similarity(new_description_vec, X_train_vec)
    
    # Get the index of the most similar description and similarity score
    most_similar_idx = np.argmax(similarities, axis=1)[0]
    similarity_score = similarities[0][most_similar_idx]
    
    # Return the most similar description and its similarity score
    return X_train.iloc[most_similar_idx], similarity_score

# Threshold for minimum cosine similarity to make a prediction
SIMILARITY_THRESHOLD = 0.2  # Adjust this based on experimentation

# Example prediction with cosine similarity
new_description = "Gibastos ko sa akoa tapad. "  # Example gibberish text

# Get the most similar description and its similarity score
most_similar_description, similarity_score = get_most_similar_description(new_description, X_train, X_train_vec, vectorizer)

# # Check if the similarity is above the threshold
if similarity_score >= SIMILARITY_THRESHOLD:
    # Proceed with prediction
    new_description_vec = vectorizer.transform([new_description])
    predicted_category = best_nb_model_category.predict(new_description_vec)[0]
    predicted_type = type_model.predict(new_description_vec)[0]

    print(f"Predicted Category for '{new_description}': {predicted_category}")
    print(f"Predicted Type for '{new_description}': {predicted_type}")
    print(f"Most Similar Description: {most_similar_description} (Similarity Score: {similarity_score:.2f})")
else:
    # Reject the prediction due to low similarity
    print(f"No valid prediction for '{new_description}' due to low similarity (Score: {similarity_score:.2f})")

# new_description_vec = vectorizer.transform([new_description])
# predicted_category = best_nb_model_category.predict(new_description_vec)[0]
# predicted_type = type_model.predict(new_description_vec)[0]

# print(f"Predicted Category for '{new_description}': {predicted_category}")
# print(f"Predicted Type for '{new_description}': {predicted_type}")