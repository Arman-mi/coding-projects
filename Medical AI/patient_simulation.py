import random
#from File_reader import symptom_db
# from BERT_NLP_MODEL import get_nlp_response
from File_reader import symptom_db
from Grading import process_question
# from File_reader import 
from Grading import user_performance, grading_section


def run_patient_simulation():
    
    
    condition, details = random.choice(list(symptom_db.items()))
    system = details['system']
    symptoms = details['symptoms']

    print(f"Patient Symptoms: {symptoms}\n")

    for _ in range(15):
            question = input("Ask the patient a question or guess the affected system: ")
            response = process_question(question, system, details)
            print("AI Response:", response)
    final_guess = input("What is your final diagnosis for the patient's condition? ")
    if final_guess.lower() == condition.lower():
        grading_section['Condition Guess'].did_ask()
        user_performance['points'] += grading_section['Condition Guess'].get_points()
        print("Correct! Your diagnosis matches the patient's condition.")
    else:
        print(f"Incorrect. The correct diagnosis was: {condition}.")

    # Display final score
    print("\nAssessment Complete.")
    print(f"Total Points: {user_performance['points']} / 42")

        







# Run the simulation
run_patient_simulation()








