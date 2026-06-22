import json
import pickle
import pandas as pd
import numpy as np
import os

class CareerChatbot:
    def __init__(self, questions_path="questions.json", career_info_path="career_info.json", model_path="model.pkl", features_path="model_features.json"):
        # Load questions, career details, model and features order
        self.questions = self._load_json(questions_path)
        self.career_info = self._load_json(career_info_path)
        self.features = self._load_json(features_path)
        self.model = self._load_model(model_path)
        
    def _load_json(self, path):
        if not os.path.exists(path):
            print(f"Warning: JSON file not found at {path}")
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {path}: {e}")
            return {}
            
    def _load_model(self, path):
        if not os.path.exists(path):
            print(f"Warning: Serialized model not found at {path}. Chatbot will use rule-based fallback.")
            return None
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading model from {path}: {e}")
            return None

    def reload_model(self, model_path="model.pkl", features_path="model_features.json"):
        """Reload the model and features lists after retraining."""
        self.model = self._load_model(model_path)
        self.features = self._load_json(features_path)

    def get_initial_state(self):
        """Initialise a fresh user state session."""
        # Setup trait scores initialized to 0
        if self.features:
            trait_scores = {feat: 0.0 for feat in self.features}
        else:
            trait_scores = {
                "trait_coding_logic": 0.0,
                "trait_visual_creativity": 0.0,
                "trait_math_analytical": 0.0,
                "trait_leadership_strategy": 0.0,
                "trait_physical_mechanical": 0.0,
                "trait_empathy_caregiving": 0.0,
                "trait_writing_argument": 0.0,
                "trait_teaching_mentoring": 0.0,
                "trait_scientific_inquiry": 0.0,
                "trait_risk_operations": 0.0
            }
            
        return {
            "current_question_id": "q1",
            "answers_history": [],
            "trait_scores": trait_scores,
            "question_count": 0,
            "completed": False
        }

    def process_answer(self, state, option_index):
        """Update scores and progress state based on chosen option."""
        current_q_id = state["current_question_id"]
        if current_q_id not in self.questions:
            state["completed"] = True
            return state

        question_data = self.questions[current_q_id]
        options = question_data.get("options", [])
        
        if option_index < 0 or option_index >= len(options):
            raise ValueError(f"Invalid option index {option_index} for question {current_q_id}")
            
        option = options[option_index]

        # 1. Apply trait score adjustments
        effects = option.get("effects", {})
        for trait, val in effects.items():
            if trait in state["trait_scores"]:
                state["trait_scores"][trait] += val

        # 2. Record historical answer details
        state["answers_history"].append({
            "question_id": current_q_id,
            "question_text": question_data["text"],
            "selected_option_text": option["text"]
        })

        # 3. Update counter
        state["question_count"] += 1

        # 4. Route path
        next_q_id = option.get("next_question")
        
        # Enforce exactly 10 questions limit
        if next_q_id is None or state["question_count"] >= 10:
            state["current_question_id"] = None
            state["completed"] = True
        else:
            state["current_question_id"] = next_q_id

        return state

    def predict_careers(self, trait_scores):
        """Run ML prediction on aggregated scores and return sorted categories."""
        if self.model is None or not self.features:
            # Rule-based fallback mapping if model file is missing
            print("Running rule-based fallback predictions...")
            trait_to_career = {
                "trait_coding_logic": "Developer",
                "trait_visual_creativity": "Designer",
                "trait_math_analytical": "Analyst",
                "trait_leadership_strategy": "Manager",
                "trait_physical_mechanical": "Engineer",
                "trait_empathy_caregiving": "Healthcare Professional",
                "trait_writing_argument": "Lawyer",
                "trait_teaching_mentoring": "Educator",
                "trait_scientific_inquiry": "Researcher",
                "trait_risk_operations": "Manager"
            }
            
            sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
            predictions = []
            seen = set()
            for trait, score in sorted_traits:
                career = trait_to_career.get(trait)
                if career and career not in seen:
                    predictions.append((career, 0.4 if len(predictions) == 0 else 0.2))
                    seen.add(career)
            
            # Fill to ensure 3 predictions
            for cat in self.career_info.keys():
                if cat not in seen:
                    predictions.append((cat, 0.05))
                    seen.add(cat)
                    if len(predictions) >= 3:
                        break
            return predictions[:3]

        # Prepare 10-dimensional input vector matching features list order
        input_data = {feat: [trait_scores.get(feat, 0.0)] for feat in self.features}
        X_input = pd.DataFrame(input_data)

        # Get probabilities for all classes
        probabilities = self.model.predict_proba(X_input)[0]
        classes = self.model.classes_

        # Sort classes based on confidence probability descending
        career_predictions = list(zip(classes, probabilities))
        career_predictions.sort(key=lambda x: x[1], reverse=True)
        
        return career_predictions

    def get_career_details(self, career_name):
        """Get full dictionary metadata (roles, skills, path) for a career."""
        return self.career_info.get(career_name, {
            "description": "Information not available.",
            "roles": [],
            "skills": [],
            "alternatives": [],
            "learning_path": []
        })
