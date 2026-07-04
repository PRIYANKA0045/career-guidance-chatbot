# 🎯 AI Career Guidance Chatbot 
Live Demo:- "https://ai-powered-career-guidance-chatbot.streamlit.app/"

An AI-powered Career Guidance System that helps students and job seekers discover suitable career paths based on their interests, skills, and preferences.

The chatbot uses adaptive questioning and a Random Forest Machine Learning model to analyze user responses and provide personalized career recommendations.

---

## 🚀 Features

- Interactive chatbot-style questionnaire
- Adaptive career assessment
- Random Forest-based career prediction
- Career category recommendation
- Specific job role suggestions
- Skill development recommendations
- Streamlit-based user interface
- JSON-based question bank for easy scalability

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red?logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-blue?logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-blue?logo=numpy)
![Git](https://img.shields.io/badge/Git-Version%20Control-orange?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)
---

## 📂 Project Structure

```text
AI-Career-Guidance-System/
│
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
│
├── __pycache__/                    # Python cache files
│
├── app.py                          # Main Streamlit application
├── chatbot_logic.py                # Adaptive questioning logic
├── train_model.py                  # Model training script
├── generate_dataset.py             # Dataset generation utility
├── verify_questions.py             # Question validation script
│
├── careers_dataset.csv             # Career training dataset
├── questions.json                  # Adaptive question bank
├── career_info.json                # Career recommendations & skills
├── model_features.json             # Feature mapping for ML model
├── model.pkl                       # Trained Random Forest model
│
├── requirements.txt                # Project dependencies
├── README.md                       # Project documentation
│
└── assets/                         # Images, GIFs, screenshots (optional)
```

### Key Components

- **app.py** → Handles the Streamlit user interface and user interactions.
- **chatbot_logic.py** → Controls adaptive question flow and response processing.
- **train_model.py** → Trains the Random Forest classifier using career datasets.
- **questions.json** → Stores dynamic career assessment questions.
- **career_info.json** → Contains career categories, job roles, required skills, and learning paths.
- **model.pkl** → Saved machine learning model used for predictions.
- **careers_dataset.csv** → Training dataset for career classification.
---

## ⚙️ How It Works

1. User starts the chatbot.
2. System asks up to 10 career-related questions.
3. User responses are converted into numerical features.
4. Random Forest model analyzes the responses.
5. System predicts the most suitable career category.
6. Recommended careers and required skills are displayed.

---

## 🎯 Career Categories

The system can recommend career categories such as:

- Developer
- Designer
- Analyst
- Engineer
- Manager
- Healthcare Professional
- Lawyer
- Educator
- Researcher
- Sports Professional

---

## 📊 Example Output

### Recommended Career Category

Developer

### Suggested Career Roles

- Software Engineer
- Full Stack Developer
- Mobile App Developer

### Recommended Skills

- Python
- JavaScript
- Data Structures & Algorithms
- Git & GitHub

---

## 🔮 Future Enhancements

- NLP-based conversational chatbot
- Personality assessment integration
- Resume analysis
- Course recommendations
- Real-time job market analysis
- User profiles and progress tracking

---

## 👨‍💻 Author

Priyanka Sharma

Engineering Student | AI & Data Analytics Enthusiast
