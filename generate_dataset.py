import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples per category
samples_per_category = 500

# Supported career categories
categories = [
    "Developer",
    "Designer",
    "Analyst",
    "Manager",
    "Engineer",
    "Healthcare Professional",
    "Lawyer",
    "Educator",
    "Researcher",
    "Sports Professional"
]

# Core trait dimensions (features)
traits = [
    "trait_coding_logic",
    "trait_visual_creativity",
    "trait_math_analytical",
    "trait_leadership_strategy",
    "trait_physical_mechanical",
    "trait_empathy_caregiving",
    "trait_writing_argument",
    "trait_teaching_mentoring",
    "trait_scientific_inquiry",
    "trait_risk_operations"
]

# Define base profile means for each career category (out of 10 points)
profile_means = {
    "Developer": {
        "trait_coding_logic": 7.5,
        "trait_math_analytical": 5.5,
        "trait_visual_creativity": 2.5,
        "trait_leadership_strategy": 1.5,
        "trait_physical_mechanical": 1.0,
        "trait_empathy_caregiving": 1.0,
        "trait_writing_argument": 2.0,
        "trait_teaching_mentoring": 1.5,
        "trait_scientific_inquiry": 3.0,
        "trait_risk_operations": 2.0
    },
    "Designer": {
        "trait_coding_logic": 2.0,
        "trait_math_analytical": 2.0,
        "trait_visual_creativity": 8.0,
        "trait_leadership_strategy": 2.0,
        "trait_physical_mechanical": 1.5,
        "trait_empathy_caregiving": 1.5,
        "trait_writing_argument": 2.5,
        "trait_teaching_mentoring": 2.0,
        "trait_scientific_inquiry": 2.0,
        "trait_risk_operations": 1.5
    },
    "Analyst": {
        "trait_coding_logic": 4.5,
        "trait_math_analytical": 7.5,
        "trait_visual_creativity": 2.0,
        "trait_leadership_strategy": 2.5,
        "trait_physical_mechanical": 1.0,
        "trait_empathy_caregiving": 1.5,
        "trait_writing_argument": 3.0,
        "trait_teaching_mentoring": 2.0,
        "trait_scientific_inquiry": 3.5,
        "trait_risk_operations": 4.5
    },
    "Manager": {
        "trait_coding_logic": 1.5,
        "trait_math_analytical": 3.5,
        "trait_visual_creativity": 2.0,
        "trait_leadership_strategy": 7.5,
        "trait_physical_mechanical": 1.0,
        "trait_empathy_caregiving": 2.0,
        "trait_writing_argument": 4.0,
        "trait_teaching_mentoring": 4.5,
        "trait_scientific_inquiry": 2.0,
        "trait_risk_operations": 6.5
    },
    "Engineer": {
        "trait_coding_logic": 3.5,
        "trait_math_analytical": 6.0,
        "trait_visual_creativity": 2.5,
        "trait_leadership_strategy": 2.5,
        "trait_physical_mechanical": 7.5,
        "trait_empathy_caregiving": 1.0,
        "trait_writing_argument": 2.0,
        "trait_teaching_mentoring": 2.0,
        "trait_scientific_inquiry": 3.5,
        "trait_risk_operations": 3.0
    },
    "Healthcare Professional": {
        "trait_coding_logic": 1.0,
        "trait_math_analytical": 3.0,
        "trait_visual_creativity": 1.5,
        "trait_leadership_strategy": 3.0,
        "trait_physical_mechanical": 2.0,
        "trait_empathy_caregiving": 8.0,
        "trait_writing_argument": 2.5,
        "trait_teaching_mentoring": 4.0,
        "trait_scientific_inquiry": 6.0,
        "trait_risk_operations": 2.5
    },
    "Lawyer": {
        "trait_coding_logic": 1.5,
        "trait_math_analytical": 3.0,
        "trait_visual_creativity": 1.5,
        "trait_leadership_strategy": 6.0,
        "trait_physical_mechanical": 1.0,
        "trait_empathy_caregiving": 2.5,
        "trait_writing_argument": 8.0,
        "trait_teaching_mentoring": 3.5,
        "trait_scientific_inquiry": 4.5,
        "trait_risk_operations": 5.0
    },
    "Educator": {
        "trait_coding_logic": 1.5,
        "trait_math_analytical": 2.5,
        "trait_visual_creativity": 2.5,
        "trait_leadership_strategy": 4.0,
        "trait_physical_mechanical": 1.5,
        "trait_empathy_caregiving": 6.0,
        "trait_writing_argument": 4.5,
        "trait_teaching_mentoring": 8.0,
        "trait_scientific_inquiry": 3.0,
        "trait_risk_operations": 2.5
    },
    "Researcher": {
        "trait_coding_logic": 3.5,
        "trait_math_analytical": 5.0,
        "trait_visual_creativity": 2.0,
        "trait_leadership_strategy": 2.0,
        "trait_physical_mechanical": 1.5,
        "trait_empathy_caregiving": 2.5,
        "trait_writing_argument": 5.5,
        "trait_teaching_mentoring": 3.5,
        "trait_scientific_inquiry": 8.0,
        "trait_risk_operations": 3.0
    },
    "Sports Professional": {
        "trait_coding_logic": 1.0,
        "trait_math_analytical": 2.0,
        "trait_visual_creativity": 2.0,
        "trait_leadership_strategy": 4.5,
        "trait_physical_mechanical": 8.0,
        "trait_empathy_caregiving": 3.0,
        "trait_writing_argument": 2.0,
        "trait_teaching_mentoring": 4.5,
        "trait_scientific_inquiry": 2.0,
        "trait_risk_operations": 2.5
    }
}

# Standard deviation for generating random variation
std_dev = 0.9

dataset_rows = []

# Generate random samples for each career category
for category in categories:
    means = profile_means[category]
    for _ in range(samples_per_category):
        row = {}
        for trait in traits:
            # Sample from normal distribution around the trait mean
            val = np.random.normal(means[trait], std_dev)
            # Clip value to be between 0.0 and 15.0 to represent realistic accumulation
            row[trait] = max(0.0, round(val, 2))
        row["career_category"] = category
        dataset_rows.append(row)

# Create DataFrame
df = pd.DataFrame(dataset_rows)

# Shuffle the dataset
df = df.sample(frac=1).reset_index(drop=True)

# Save to CSV
csv_filename = "careers_dataset.csv"
df.to_csv(csv_filename, index=False)
print(f"Generated {len(df)} samples and saved successfully to {csv_filename}.")
print("\nDataset overview (first 5 rows):")
print(df.head())
