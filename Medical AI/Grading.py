from BERT_pipeline import classify_intent
class pointCheker:
    def __init__(self, point):
        self.point = point
        self.asked = False
        self.Question ={"points": self.point, 'asked':self.asked}
    def did_ask(self):
        self.Question['asked'] = True
    def get_points(self):
        return self.Question["points"]



grading_section = {'PPE Precautions' : pointCheker(1),
                  'Scene Safety': pointCheker(1),
                  'Mechanism of injury':pointCheker(1),
                  'Number of patients':pointCheker(1),
                  'Additional EMS assistance':pointCheker(1),
                  'Spine stabilization': pointCheker(1),
                  'chief complaint' :pointCheker(1),
                  'determines responsiveness': pointCheker(1),
                  'System Identification': pointCheker(4),
                  'Condition Guess': pointCheker(5)
                  }
user_performance = {
    "points" : 0,
    "critical fail" : False
}



def process_question(question, system, condition_data):
    """Process the question using BERT for intent classification."""
    intent = classify_intent(question)

    if intent == "Check for PPE precautions":
        if not grading_section['PPE Precautions'].asked:
            grading_section['PPE Precautions'].did_ask()
            user_performance['points'] += grading_section['PPE Precautions'].get_points()
        return "Yes, PPE precautions are in place."
    elif intent == "Ask about blood pressure":
        return f"The patient's blood pressure is {condition_data['blood_pressure']}."

    elif intent == "Ask about heart rate" or intent == "Ask about pulse":
        return f"The patient's heart rate is {condition_data['heart_rate']}."

    elif intent == "Ask about respiratory rate":
        return "The patient's respiratory rate is elevated."

    elif intent == "Vital Signs":
        if "blood pressure" in question:
            return f"The patient's blood pressure is {condition_data['blood_pressure']}."
        elif "heart rate" in question or "pulse" in question:
            return f"The patient's heart rate is {condition_data['heart_rate']}."
        elif "respiratory rate" in question or "breathing" in question:
            return "The patient's respiratory rate is elevated."

    elif intent == "System Identification":
        if question.lower() == system.lower():
            if not grading_section['System Identification'].asked:
                grading_section['System Identification'].did_ask()
                user_performance['points'] += grading_section['System Identification'].get_points()
            return f"Correct! This condition affects the {system} system."
    # Final Diagnosis
    elif intent == "Final Diagnosis":
        return "Please provide your final diagnosis for the patient's condition at the end of the assessment."

    # Scene Safety
    elif intent == "Scene Safety":
        if not grading_section.get('Scene Safety'):
            grading_section['Scene Safety'] = pointCheker(1)
        if not grading_section['Scene Safety'].asked:
            grading_section['Scene Safety'].did_ask()
            user_performance['points'] += grading_section['Scene Safety'].get_points()
        return "The scene is safe."

    # Number of Patients
    elif intent == "Number of patients":
        if not grading_section.get('Number of patients'):
            grading_section['Number of patients'] = pointCheker(1)
        if not grading_section['Number of patients'].asked:
            grading_section['Number of patients'].did_ask()
            user_performance['points'] += grading_section['Number of patients'].get_points()
        return "There is one patient."

    # Additional EMS
    elif intent == "additional ems":
        if not grading_section.get('Additional EMS assistance'):
            grading_section['Additional EMS assistance'] = pointCheker(1)
        if not grading_section['Additional EMS assistance'].asked:
            grading_section["Additional EMS assistance"].did_ask()
            user_performance['points'] += grading_section['Additional EMS assistance'].get_points()
        return "Additional EMS assistance has been requested."

    # Spine Stabilization
    elif intent == "Spine Stabilization":
        if not grading_section.get('Spine Stabilization'):
            grading_section['Spine Stabilization'] = pointCheker(1)
        if not grading_section['Spine Stabilization'].asked:
            grading_section['Spine Stabilization'].did_ask()
            user_performance['points'] += grading_section['Spine Stabilization'].get_points()
        return "Spine stabilization has been considered."

    # Chief Complaint
    elif intent == "chief complaint":
        if not grading_section.get('chief complaint'):
            grading_section['chief complaint'] = pointCheker(1)
        if not grading_section['chief complaint'].asked:
            grading_section['chief complaint'].did_ask()
            user_performance['points'] += grading_section['chief complaint'].get_points()
        return f"The patient's chief complaint is: {condition_data['symptoms']}."

    # Responsiveness
    elif intent == "responsiveness":
        if not grading_section.get('determines responsiveness'):
            grading_section['determines responsiveness'] = pointCheker(1)
        if not grading_section['determines responsiveness'].asked:
            grading_section['determines responsiveness'].did_ask()
            user_performance['points'] += grading_section['determines responsiveness'].get_points()
        return "The patient is responsive and alert."        








    return "I don't understand the question."