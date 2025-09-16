# Patient_form

Patient_form is a lightweight and efficient application designed to simplify the creation and management of patient prescription forms through a FastAPI backend and streamlit frontend. It provides a streamlined way for doctors to generate and manage prescriptions digitally.

---

## Table of Contents

- [About](#about)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Contributing](#contributing)  

---

## About
This project aims to make patient prescription forms easier to generate and manage by leveraging FastAPI's fast and modern web framework capabilities for the backend, paired with Streamlit for building a user-friendly and interactive frontend. It focuses on providing doctors a simple and efficient interface coupled with a powerful API for handling prescriptions.

---

## Features

- Fast and asynchronous API powered by FastAPI  
- Easy to create, update, and manage patient prescription forms  
- Lightweight and minimal dependencies  
- Designed for easy integration and extension  

---

## Tech Stack

| Technology | Description                          |
|------------|------------------------------------|
| Python     | Core programming language           |
| FastAPI    | High-performance web framework for APIs |
| Streamlit  | Frontend framework for interactive UI |
| Uvicorn    | ASGI server for running FastAPI apps |

---

## Installation

To run Patient_form locally, follow these instructions:

1. Clone the repository:
git clone https://github.com/Krishna-Mantri/Patient_form.git

2. Navigate to the project directory:
cd Patient_form

3. Create and activate a virtual environment:

    python -m venv venv

    source venv/bin/activate
   
    On Windows use: venv\Scripts\activate

5. Install the required dependencies:
pip install -r requirements.txt

6. Run the FastAPI server:
  uvicorn main:app --reload


---

## Usage

1. Start the FastAPI backend server:
uvicorn main:app --reload

2. In a separate terminal, start the Streamlit frontend app:
streamlit run app.py

3. Use the Streamlit app UI to create and manage patient prescription forms. The Streamlit frontend sends API requests to the FastAPI backend, creating a seamless user experience.

4. Optionally, visit `http://127.0.0.1:8000/docs` to explore the interactive API documentation with Swagger UI.

---

## Contributing

Contributions, issues, and feature requests are welcome. Please feel free to fork the repository and submit pull requests for improvements or additional features.

---


