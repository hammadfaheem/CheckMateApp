# CheckMateApp

**CheckMateApp** is an intelligent, automated assignment evaluation system designed to streamline grading using AI. It leverages natural language processing to compare student answers against a teacher's rubric and generates consistent and structured evaluation reports.

## 🚀 Features

- 🧠 AI-powered student answer evaluation
- 📄 Rubric-based grading mechanism
- 📥 Bulk and single submission support
- 🖥️ Streamlit interface for ease of use
- 🧪 API testing and modular agent architecture

## 📁 Project Structure

```
CheckMateApp/
│
├── app/                    # Streamlit UI components
│   ├── Home.py
│   ├── navigation.py
│   └── assets/
│       ├── 2_Single_submission.py
│       └── 3_Bulk_Submission.py
│
├── agents/                 # Intelligent agents for formatting, evaluation, etc.
│   ├── evaluator_agent.py
│   ├── rubric_agent.py
│   └── format_agent.py
│
├── api_testing/            # Notebooks for testing
│   └── Untitled.ipynb
│
├── utils.py                # Shared utility functions
├── app.py                  # Entry point for the application
├── sample_input.py         # Example inputs for testing
├── README.md               # Project documentation
├── .gitignore
└── CheckMate FYP.docx      # Full project report
```

## 🛠️ Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/CheckMateApp.git
   cd CheckMateApp
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

> **Note:** If `requirements.txt` is missing, manually install libraries like `streamlit`, `openai`, etc., based on your code.

## ▶️ Usage

To launch the Streamlit application:

```bash
streamlit run app/Home.py
```

The app will open in your browser, where you can:

- Upload a rubric and student submissions
- View automated scoring and analysis
- Download results in structured format

## 🧠 How It Works

- The **Rubric Agent** interprets the teacher's marking guide.
- The **Evaluator Agent** compares student answers with the rubric.
- The **Format Agent** ensures the output is clean and structured.

## 📄 License

This project is for academic and educational purposes.

## 👥 Credits

Developed as part of a Final Year Project (FYP) by Hammad and team.