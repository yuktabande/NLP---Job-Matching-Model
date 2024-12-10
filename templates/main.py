from flask import Flask, request, render_template
import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Predefined list of skills with abbreviations
skills_dict = {
    'Python': ['Python', 'Py'],
    'Java': ['Java'],
    'JavaScript': ['JavaScript', 'JS'],
    'C++': ['C++'],
    'Ruby': ['Ruby'],
    'PHP': ['PHP'],
    'R' :['R'],
    'C#': ['C#'],
    'Django': ['Django'],
    'Flask': ['Flask'],
    'React': ['React','ReactJS','React.js'],
    'Angular': ['Angular'],
    'Spring': ['Spring'],
    'TensorFlow': ['TensorFlow','tf'],
    'MySQL': ['MySQL'],
    'PostgreSQL': ['PostgreSQL'],
    'MongoDB': ['MongoDB'],
    'SQLite': ['SQLite'],
    'Git': ['Git'],
    'Docker': ['Docker'],
    'Kubernetes': ['Kubernetes'],
    'AWS': ['AWS'],
    'Azure': ['Azure'],
    'JIRA': ['JIRA'],
    'Teamwork': ['Teamwork'],
    'Leadership': ['Leadership'],
    'Problem-Solving': ['Problem-Solving'],
    'Data Analysis': ['Data Analysis','Data Analyst'],
    'User Experience Design (UX)': ['User Experience Design (UX)','UX','UI-UX'],
    'Search Engine Optimization (SEO)': ['Search Engine Optimization ','(SEO)'],
}

# Weights for similarity and skill matching
cosine_weight = 0.6  # Weight for cosine similarity
skill_weight = 0.4   # Weight for skill matching

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return ""

def extract_skills(text):
    found_skills = []
    # Check for each skill and its variations
    for skill, variations in skills_dict.items():
        for variation in variations:
            if re.search(r'\b' + re.escape(variation) + r'\b', text, re.IGNORECASE):
                found_skills.append(skill)
                break  # Stop checking after the first match for this skill
    return found_skills

def calculate_skill_score(resume_skills, job_skills):
    return sum([1 for skill in resume_skills if skill in job_skills])

@app.route("/")
def matchresume():
    return render_template('matchresume.html')

@app.route('/matcher', methods=['POST'])
def matcher():
    if request.method == 'POST':
        job_description = request.form['job_description']
        resume_files = request.files.getlist('resumes')

        resumes = []
        resume_skills = []
        for resume_file in resume_files:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(filename)
            text = extract_text(filename)
            resumes.append(text)
            skills = extract_skills(text)
            resume_skills.append(skills)

        if not resumes or not job_description:
            return render_template('matchresume.html', message="Please upload resumes and enter a job description.")

        # Vectorize job description and resumes
        vectorizer = TfidfVectorizer().fit_transform([job_description] + resumes)
        vectors = vectorizer.toarray()

        # Calculate cosine similarities
        job_vector = vectors[0]
        resume_vectors = vectors[1:]
        similarities = cosine_similarity([job_vector], resume_vectors)[0]

        job_skills = extract_skills(job_description)
        skill_scores = [calculate_skill_score(skills, job_skills) for skills in resume_skills]

        # Combine similarity and skill scores with weights
        combined_scores = [(cosine_weight * sim) + (skill_weight * skill) for sim, skill in zip(similarities, skill_scores)]

        # Get top 5 resumes
        top_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)[:5]
        top_resumes = [resume_files[i].filename for i in top_indices]
        combined_scores = [round(combined_scores[i], 2) for i in top_indices]

        return render_template('matchresume.html', message="Top matching resumes:", top_resumes=top_resumes, similarity_scores=combined_scores)

    return render_template('matchresume.html')

if _name_ == '_main_':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)