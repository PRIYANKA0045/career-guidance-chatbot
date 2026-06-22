import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_model():
    # 1. Load the dataset
    try:
        df = pd.read_csv("careers_dataset.csv")
    except Exception as e:
        print(f"Error loading careers_dataset.csv: {e}")
        print("Please ensure generate_dataset.py has run successfully.")
        return

    print(f"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

    # 2. Separate features and target
    # The last column is the career_category target, and the first 10 columns are the traits.
    feature_cols = [col for col in df.columns if col.startswith("trait_")]
    target_col = "career_category"

    X = df[feature_cols]
    y = df[target_col]

    print("\nFeatures used for training:")
    for i, col in enumerate(feature_cols, 1):
        print(f"  {i}. {col}")

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\nTraining set size: {X_train.shape[0]} samples")
    print(f"Testing set size: {X_test.shape[0]} samples")

    # 4. Initialize and train the Random Forest Classifier
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_split=5,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 5. Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n[MODEL EVALUATION] Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save the trained model and feature list
    model_filename = "model.pkl"
    with open(model_filename, "wb") as f:
        pickle.dump(model, f)
    print(f"Successfully saved trained model to {model_filename}.")

    # Save feature names order to a JSON file for prediction alignment
    features_filename = "model_features.json"
    with open(features_filename, "w") as f:
        json.dump(feature_cols, f, indent=2)
    print(f"Successfully saved feature metadata to {features_filename}.")

if __name__ == "__main__":
    train_model()
