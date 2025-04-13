# app.py
from flask import Flask, render_template, request
import os
import fitz  # PyMuPDF
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Setup Gemini
genai.configure(api_key='AIzaSyDwVZ8jkfWjyXWwgJ60HzH1t9rO8AT_jAU')

model = genai.GenerativeModel('gemini-1.5-pro')

def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text
import re
def parse_resume_analysis(text):

    return result



def analyze_resume_with_gemini(resume_text, job_desc):
    prompt = f"""
    Job Description: {job_desc}
    Resume: {resume_text}
    
    1. Match Score (0 to 100):
    2. List of Matching Skills:
    3. List of Missing Skills:
    4. Suggest free online resources for missing skills:
    5. One-line feedback:
    """
    response = model.generate_content(prompt)
    text=response.text
    result = {}

    # Match Score
    match_score = re.search(r"Match Score \(0 to 100\): (\d+)", text)
    result['match_score'] = match_score.group(1) if match_score else None

    # Matching Skills
    match_skills = re.search(r"List of Matching Skills:\s*(.+?)\n\n", text, re.DOTALL)
    if match_skills:
        result['matching_skills'] = [skill.strip() for skill in match_skills.group(1).split(',')]
    else:
        result['matching_skills'] = []

    # Missing Skills
    missing_skills = re.search(r"List of Missing Skills:\s*(.+?)\n\n", text, re.DOTALL)
    if missing_skills:
        lines = [line.strip("* ").strip() for line in missing_skills.group(1).strip().split("\n") if line.strip()]
        result['missing_skills'] = lines
    else:
        result['missing_skills'] = []

    # Resources
    resources = re.search(r"Suggest free online resources for missing skills:\s*(.+?)\n\n", text, re.DOTALL)
    if resources:
        lines = [line.strip("* ").strip() for line in resources.group(1).strip().split("\n") if line.strip()]
        result['resources'] = lines
    else:
        result['resources'] = []

    # Feedback
    feedback = re.search(r"One-line feedback:\s*(.+)", text)
    result['feedback'] = feedback.group(1).strip() if feedback else None

    
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    job_desc = request.form['job_description']
    resumes = request.files.getlist('resumes')
    
    results = []
    for resume in resumes:
        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(path)
        resume_text = extract_text_from_pdf(path)
        analysis = analyze_resume_with_gemini(resume_text, job_desc)
        results.append({'filename': resume.filename, 'analysis': analysis})
    
    return render_template('results.html', results=results)
import google.generativeai as genai

# Initialize the model (replace 'gemini-v1' with the model you want to use)
models = genai.GenerativeModel("gemini-v1")

print(models)
if __name__ == '__main__':
    app.run(debug=True)
# Fetch available models

