import streamlit as st
import pandas as pd
import joblib
from googlesearch import search
import wikipediaapi
import requests
from bs4 import BeautifulSoup


symptoms = ['itching',
 'skin_rash',
 'nodal_skin_eruptions',
 'continuous_sneezing',
 'shivering',
 'chills',
 'joint_pain',
 'stomach_pain',
 'acidity',
 'ulcers_on_tongue',
 'muscle_wasting',
 'vomiting',
 'burning_micturition',
 'spotting_ urination',
 'fatigue',
 'weight_gain',
 'anxiety',
 'cold_hands_and_feets',
 'mood_swings',
 'weight_loss',
 'restlessness',
 'lethargy',
 'patches_in_throat',
 'irregular_sugar_level',
 'cough',
 'high_fever',
 'sunken_eyes',
 'breathlessness',
 'sweating',
 'dehydration',
 'indigestion',
 'headache',
 'yellowish_skin',
 'dark_urine',
 'nausea',
 'loss_of_appetite',
 'pain_behind_the_eyes',
 'back_pain',
 'constipation',
 'abdominal_pain',
 'diarrhoea',
 'mild_fever',
 'yellow_urine',
 'yellowing_of_eyes',
 'acute_liver_failure',
 'fluid_overload',
 'swelling_of_stomach',
 'swelled_lymph_nodes',
 'malaise',
 'blurred_and_distorted_vision',
 'phlegm',
 'throat_irritation',
 'redness_of_eyes',
 'sinus_pressure',
 'runny_nose',
 'congestion',
 'chest_pain',
 'weakness_in_limbs',
 'fast_heart_rate',
 'pain_during_bowel_movements',
 'pain_in_anal_region',
 'bloody_stool',
 'irritation_in_anus',
 'neck_pain',
 'dizziness',
 'cramps',
 'bruising',
 'obesity',
 'swollen_legs',
 'swollen_blood_vessels',
 'puffy_face_and_eyes',
 'enlarged_thyroid',
 'brittle_nails',
 'swollen_extremeties',
 'excessive_hunger',
 'extra_marital_contacts',
 'drying_and_tingling_lips',
 'slurred_speech',
 'knee_pain',
 'hip_joint_pain',
 'muscle_weakness',
 'stiff_neck',
 'swelling_joints',
 'movement_stiffness',
 'spinning_movements',
 'loss_of_balance',
 'unsteadiness',
 'weakness_of_one_body_side',
 'loss_of_smell',
 'bladder_discomfort',
 'foul_smell_of urine',
 'continuous_feel_of_urine',
 'passage_of_gases',
 'internal_itching',
 'toxic_look_(typhos)',
 'depression',
 'irritability',
 'muscle_pain',
 'altered_sensorium',
 'red_spots_over_body',
 'belly_pain',
 'abnormal_menstruation',
 'dischromic _patches',
 'watering_from_eyes',
 'increased_appetite',
 'polyuria',
 'family_history',
 'mucoid_sputum',
 'rusty_sputum',
 'lack_of_concentration',
 'visual_disturbances',
 'receiving_blood_transfusion',
 'receiving_unsterile_injections',
 'coma',
 'stomach_bleeding',
 'distention_of_abdomen',
 'history_of_alcohol_consumption',
 'fluid_overload.1',
 'blood_in_sputum',
 'prominent_veins_on_calf',
 'palpitations',
 'painful_walking',
 'pus_filled_pimples',
 'blackheads',
 'scurring',
 'skin_peeling',
 'silver_like_dusting',
 'small_dents_in_nails',
 'inflammatory_nails',
 'blister',
 'red_sore_around_nose',
 'yellow_crust_ooze']

# Set page title
st.set_page_config(page_title='Disease Prediction', layout='wide')

# Page header
st.title("Disease Prediction")
st.markdown("This is a web app to predict the disease based on the symptoms")

# Load image
# image = "your_image_path.png"
# st.image(image, use_column_width=True)


# Symptom selection
st.subheader("Symptom Selection")
options = st.multiselect('Select Symptoms', symptoms)

# Load the model
model = joblib.load("model.job")

# Function to get prediction
def get_prediction(ina):
    pizza = {}
    for i in symptoms:
        if i not in ina:
            pizza[i] = 0
        else:
            pizza[i] = 1
        
    aha = pd.DataFrame([pizza])
    return model.predict(aha)

# Function to get disease summary from Wikipedia
def get_summary(disease):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(disease)
    if page.exists():
        return page.summary[0:500] + "..."
    else:
        return None
def fetch_images(query, num_images):
    # Perform Google search for images
    search_query = query + " disease"
    search_results = list(search(search_query, num_results=num_images, lang='en'))

    # Scrape image URLs from search results
    image_urls = []
    for result in search_results:
        res = requests.get(result)
        soup = BeautifulSoup(res.text, 'html.parser')
        images = soup.find_all('img')
        for image in images:
            if image['src'].startswith('http'):
                image_urls.append(image['src'])
                if len(image_urls) == num_images:
                    return image_urls

    return image_urls

# Perform prediction
if st.button("Predict"):
    if len(options) == 0:
        st.error("Please select at least one symptom.")
    else:
        st.subheader("Prediction Result")
        result = get_prediction(options)[0]
        st.write("The predicted disease is:", result)

        # Fetch disease summary from Wikipedia
        summary = get_summary(result)
        if summary is not None:
            st.subheader("Disease Summary")
            st.write(summary)
        else:
            st.warning("No summary found for the disease.")

         # Fetch disease information from Google Knowledge Graph API
        query = result + " disease"
        q2 = result + " hospitals near me"
        search_results = list(search(query, num_results=1, lang='en'))
        search_results2 = list(search(q2, num_results=1, lang='en'))
        if search_results:
            st.subheader("Disease Information")
            st.write(f"**Search Result**: [{search_results[0]}]({search_results[0]})")
            st.write(f"**Hospitals**: [{search_results2[0]}]({search_results2[0]})")

          
            
        else:
            st.warning("No additional information found for the disease.")

        
