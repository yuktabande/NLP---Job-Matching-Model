# NLP-Based Resume Parser and Job Matching System

## Overview
This project is an **AI-driven Resume Parser and Job Matching System** that utilizes **Natural Language Processing (NLP)** to analyze resumes and job descriptions, extracting relevant information and ranking resumes based on their suitability for a given job. The system also incorporates a **soft skills analysis feature** to enhance job-resume matching beyond technical qualifications.

## Features
- **Resume Parsing**: Extracts structured information (e.g., name, contact, skills, experience, education) from resumes.
- **Job Description Analysis**: Identifies key requirements, skills, and responsibilities.
- **Job-Resume Matching**: Uses **TF-IDF** to compare resumes with job descriptions.
- **Soft Skills Analysis**: Identifies behavioral traits and communication skills mentioned in resumes.
- **Frontend Interface**: Upload job descriptions and multiple resumes for analysis.
- **Ranking System**: Outputs the best-matched resumes based on a similarity score.

## Tech Stack
- **Backend**: Python, Flask
- **Frontend**: React.js 
- **NLP Libraries**: SpaCy, NLTK
- **File Handling**: PyMuPDF (fitz), pdfplumber (for PDF parsing)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yuktabande/NLP---Job-Matching-Model.git
   cd resume-parser-matching
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. **Upload** a job description.
2. **Upload multiple resumes** (PDF format preferred).
3. Click **Analyze** to process the resumes.
4. View ranked resumes based on their **matching score**.
5. Optionally, analyze **soft skills** extracted from resumes.

## Future Enhancements
- **Support for multiple resume formats** (DOCX, TXT, etc.).
- **Advanced Machine Learning models** for improved matching.
- **Integration with LinkedIn and job boards** for automated resume retrieval.
- **User authentication system** for recruiters and job seekers.

## Contact
For inquiries, reach out to **yuktaabande@gmail.com** or open an issue in the repository.

