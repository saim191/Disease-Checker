from typing import List

symptom_data = {
    "headache": {
        "description": "A headache is pain in any region of the head.",
        "medicines": [
            {"medicine": "Paracetamol", "dosage": "500mg every 4-6 hours", "warnings": "Do not exceed 4g per day"},
            {"medicine": "Ibuprofen", "dosage": "400mg every 6-8 hours", "warnings": "Take after food, avoid in ulcers"},
        ],
    },
    "fever": {
        "description": "A fever is a temporary increase in your body temperature.",
        "medicines": [
            {"medicine": "Paracetamol", "dosage": "500mg every 4-6 hours", "warnings": "Safe when taken in recommended doses"},
            {"medicine": "Ibuprofen", "dosage": "400mg every 6-8 hours", "warnings": "May cause stomach upset"},
        ],
    },
    "cold": {
        "description": "A common cold is a viral infection of your nose and throat.",
        "medicines": [
            {"medicine": "Cetirizine", "dosage": "10mg once a day", "warnings": "May cause drowsiness"},
            {"medicine": "Paracetamol", "dosage": "500mg every 4-6 hours", "warnings": "Monitor for liver function"},
        ],
    },
    "cough": {
        "description": "A cough is a reflex action to clear your airways.",
        "medicines": [
            {"medicine": "Dextromethorphan", "dosage": "10-20mg every 4 hours", "warnings": "Do not mix with alcohol"},
            {"medicine": "Guaifenesin", "dosage": "200-400mg every 4 hours", "warnings": "Drink water to help loosen mucus"},
        ],
    },
    "sore throat": {
        "description": "Sore throat is pain or irritation in the throat.",
        "medicines": [
            {"medicine": "Lozenges", "dosage": "As needed", "warnings": "Do not exceed recommended amount"},
            {"medicine": "Warm saline gargles", "dosage": "3 times a day", "warnings": "Use warm water"},
        ],
    },
}

disease_map = {
    frozenset(["fever", "cough", "cold"]): "Common Cold or Flu",
    frozenset(["headache", "fever"]): "Viral Fever",
    frozenset(["sore throat", "cough"]): "Throat Infection",
    frozenset(["cold", "sore throat", "fever"]): "Upper Respiratory Infection",
    frozenset(["headache"]): "Tension Headache",
    frozenset(["fever"]): "Mild Infection",
}

general_disclaimer = (
    "\n⚠️ The above suggestions are for informational purposes only.\n"
    "Always consult a healthcare professional before taking any medication."
)

def identify_symptoms(inputs: List[str]) -> List[str]:
    found_symptoms = []
    for symptom in symptom_data:
        for user_input in inputs:
            if symptom in user_input.lower():
                if symptom not in found_symptoms:
                    found_symptoms.append(symptom)
    return found_symptoms

def possible_disease(symptoms: List[str]) -> str:
    input_set = set(symptoms)
    for key in disease_map:
        if key.issubset(input_set):
            return disease_map[key]
    return "Could not determine a specific illness. It may be a general infection."

def generate_diagnosis(symptoms: List[str]) -> str:
    if not symptoms:
        return "❗ No known symptoms identified.\nPlease enter valid common symptoms."

    diagnosis = f"Based on your symptoms ({', '.join(symptoms)}), the possible condition is: "
    diagnosis += f"**{possible_disease(symptoms)}**\n\n"

    for symptom in symptoms:
        data = symptom_data[symptom]
        diagnosis += f"{symptom.upper()}:\n{data['description']}\nRecommended medicines:\n"
        for med in data["medicines"]:
            diagnosis += f"- {med['medicine']}, Dosage: {med['dosage']}, Warning: {med['warnings']}\n"
        diagnosis += "\n"

    diagnosis += general_disclaimer
    return diagnosis

def main():
    print("👋 Welcome to Symptom Cure Buddy!")
    print("I'll ask you a few questions about your symptoms.\n")

    primary = input("👉 Enter your *primary* symptom: ").strip()
    secondary = input("👉 Enter your *secondary* symptom (or press Enter to skip): ").strip()
    other = input("👉 Any other symptoms? (separated by commas, or press Enter to skip): ").strip()

    symptom_inputs = [primary]
    if secondary:
        symptom_inputs.append(secondary)
    if other:
        symptom_inputs.extend([s.strip() for s in other.split(",") if s.strip()])

    matched_symptoms = identify_symptoms(symptom_inputs)
    print("\n🔍 Analyzing symptoms...\n")
    print(generate_diagnosis(matched_symptoms))

if __name__ == "__main__":
    main()
