import pandas as pd

df1 = pd.read_csv('AyurAI/Formulation_Recommender/Formulation-Indications.csv')

formulations_lst = list(df1['Name of Medicine'])

original_list = list(df1['Main Indications'])

processed_list = []

for item in original_list:
    # Remove spaces and newline characters, convert to lowercase
    processed_item = ''.join(item.split()).lower()
    processed_list.append(processed_item)

# List of lists of symptoms
list_of_symptoms = processed_list

# Flatten the list of lists and split the symptoms using commas and spaces
flat_symptoms = [symptom.replace(',', ' ').split() for symptoms in list_of_symptoms for symptom in symptoms.split(',')]

# Get unique symptoms as a list
unique_symptoms = list(set(symptom for sublist in flat_symptoms for symptom in sublist))

data = {
    "Formulation": formulations_lst,
    "Symptoms": processed_list,
}

symptoms = pd.read_csv('AyurAI/Formulation_Recommender/ayurvedic_symptoms_desc.csv')

symptoms['Symptom'] = symptoms['Symptom'].str.lower()

def symptoms_desc(symptom_name):
    row = symptoms[symptoms['Symptom'] == symptom_name.lower()]
#     print(row)
    if not row.empty:
        description = row.iloc[0]['Description']
        print(f'Description of "{symptom_name}": {description}')
    else:
        print(f'Symptom "{symptom_name}" not found in the DataFrame.')

def symptoms_lst_desc(user_symptoms):
    for item in user_symptoms:
#         print(item)
        symptoms_desc(item)

import difflib

# Your list of correct words (assuming you have a list called unique_symptoms)
correct_words = unique_symptoms

def correct_symptoms(symptoms):
    corrected_symptoms = []
    for symptom in symptoms:
        corrected_symptom = difflib.get_close_matches(symptom, correct_words, n=1, cutoff=0.6)
        if corrected_symptom:
            corrected_symptoms.append(corrected_symptom[0])
        else:
            corrected_symptoms.append(symptom)
    return corrected_symptoms

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = {
    "Formulation": formulations_lst,
    "Symptoms": processed_list,
}

# User symptoms
user_input = input("Enter a list of symptoms separated by spaces: ")

input_symptoms = user_input.split()
user_symptoms = correct_symptoms(input_symptoms)
print(f"Did you mean: {', '.join(user_symptoms)}")

symptoms_lst_desc(user_symptoms)
user_symptoms_str = " ".join(user_symptoms)  # Convert user symptoms to a single string

# Create a DataFrame
df = pd.DataFrame(data)

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the symptom text data into numerical features
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Symptoms'])

# Transform user symptoms into TF-IDF format
user_symptoms_tfidf = tfidf_vectorizer.transform([user_symptoms_str])

# Calculate cosine similarity between user's symptoms and all formulations
similarities = cosine_similarity(user_symptoms_tfidf, tfidf_matrix)

# Set a threshold for similarity score (adjust as needed)
similarity_threshold = 0.5  # You can adjust this value

# Find all formulations with similarity scores above the threshold
matching_indices = [i for i, sim in enumerate(similarities[0]) if sim > similarity_threshold]

if not matching_indices:
    print("No matching formulations found for the provided symptoms.")
else:
    closest_formulations = df.iloc[matching_indices]["Formulation"]
    print("Closest Formulations:")
    print(closest_formulations.tolist())

# Create a boolean mask to filter rows where the second column matches any element in closest_formulations
mask = df1.iloc[:, 0].isin(closest_formulations)

# Use the mask to select the rows that match the condition
filtered_df = df1[mask]

# Iterate through the filtered DataFrame and print each row separately
for index, row in filtered_df.iterrows():
    print(row)