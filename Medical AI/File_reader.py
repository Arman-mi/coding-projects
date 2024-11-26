import pandas as pd



keyword_synonyms = {
    'chest pain': ['hurt chest', 'pain in chest', 'chest ache'],
    'shortness of breath': ['trouble breathing', 'difficulty breathing'],
    'dizziness': ['lightheaded', 'feeling faint'],
    'slurred speech': ['difficulty speaking', 'trouble talking'],
    'numbness in limbs': ['numb in arms', 'numbness in arm', 'loss of feeling in limbs'],
    'confusion': ['feeling disoriented', 'feeling lost'],
    'wheezing': ['whistling sound when breathing'],
    'coughing': ['persistent cough', 'dry cough']
}

symptom_db = {
    'Heart Attack': {
        'system': 'Cardiovascular',
        'symptoms': 'Chest pain, shortness of breath, irregular pulse',
        'blood_pressure': 'High',
        'heart_rate': 'Irregular and weak',
        'skin_color': 'Pale and clammy'
    },
    'Stroke': {
        'system': 'Neurological',
        'symptoms': 'Slurred speech, weakness on one side, confusion',
        'blood_pressure': 'High',
        'heart_rate': 'Normal but weak',
        'skin_color': 'Normal'
    },
    'Asthma Attack': {
        'system': 'Pulmonary',
        'symptoms': 'Wheezing, shortness of breath, chest tightness',
        'blood_pressure': 'Normal',
        'heart_rate': 'Elevated',
        'skin_color': 'Slightly cyanotic around the lips'
    },
    'Appendicitis': {
        'system': 'GI/GU',
        'symptoms': 'Sharp abdominal pain, especially on right side, fever',
        'blood_pressure': 'Normal',
        'heart_rate': 'Elevated',
        'skin_color': 'Normal but may appear flushed'
    },
    'Allergic Reaction': {
        'system': 'Integumentary',
        'symptoms': 'Rash, itching, swelling, hives',
        'blood_pressure': 'Normal',
        'heart_rate': 'Elevated',
        'skin_color': 'Red and swollen around affected area'
    },
    'Anxiety Attack': {
        'system': 'Psychological',
        'symptoms': 'Rapid heartbeat, excessive worry, dizziness, shortness of breath',
        'blood_pressure': 'Normal',
        'heart_rate': 'Elevated',
        'skin_color': 'Pale'
    },
    'Fracture': {
        'system': 'Musculoskeletal',
        'symptoms': 'Severe pain at injury site, swelling, inability to move affected area',
        'blood_pressure': 'Normal',
        'heart_rate': 'Elevated due to pain',
        'skin_color': 'Bruising around the injury site'
    },
    'Ectopic Pregnancy': {
        'system': 'Reproductive',
        'symptoms': 'Severe abdominal pain, dizziness, shoulder pain',
        'blood_pressure': 'Low',
        'heart_rate': 'Elevated',
        'skin_color': 'Pale, with cold sweats'
    }
}


