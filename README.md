 Prescription Processing Engine

 Project Overview

The Prescription Processing Engine is an AI-powered application that analyzes prescription details entered by the user. It extracts important information such as medicine details, dosage, frequency, and precautions through a simple Streamlit interface.

 Features

* User-friendly Streamlit interface
* Prescription analysis
* Medicine information extraction
* Dosage and frequency identification
* Basic precautions display
* AI-ready architecture using LangChain and OpenAI

 Tech Stack

* Python
* Streamlit
* LangChain
* OpenAI API
* python-dotenv

 Project Structure

```
prescription-processing-engine/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── test.py
│── utils/
│   └── prescription_processor.py
```

How to run

1. Install Python 3.8 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app with Streamlit:
   ```bash
   streamlit run app.py
   ```
4. Open the URL shown in the terminal (usually `http://localhost:8501`).

 Sample Input

Paracetamol 650mg twice a day for 3 days for fever

Sample Output

* Medicine: Paracetamol 650mg
* Dosage: Twice a day
* Duration: 3 days
* Condition: Fever
* Precautions: Follow doctor's instructions.

 Future Enhancements

* OCR support for handwritten prescriptions
* Real-time AI analysis
* Drug interaction detection
* PDF report generation

Developed by

**Janani v**
