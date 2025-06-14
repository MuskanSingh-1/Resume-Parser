import re
from typing import Dict
import pdfplumber
import docx2txt
import spacy
import tempfile

# Load Spacy model once
nlp = spacy.load("en_core_web_sm")

# Skills database for improved skill detection
SKILLS_DB = [
    'python', 'java', 'sql', 'pandas', 'numpy', 'machine learning', 'data analysis','tensorflow', 'keras', 'power bi', 'communication', 'excel',  
    'tableau', 'html', 'css','c++', 'javascript', 'flask', 'django', 'data structures', 'algorithms', 'artificial intelligence','deep learning', 
    'computer vision', 'natural language processing', 'big data', 'cloud computing', 'cybersecurity', 'blockchain', 'software engineering', 
    'web development', 'mobile app development', 'database management', 'version control (git, github)', 'operating systems', 'networking',
    'api development', 'devops', 'agile methodologies', 'system design', 'embedded systems', 'iot', 'quantum computing', 'bioinformatics', 
    'cryptography', 'parallel computing', 'distributed systems', 'virtual reality', 'augmented reality', 'game development', 'computer graphics',
    'computational mathematics', 'digital signal processing', 'edge computing', 'cloud security', 'penetration testing', 'ethical hacking', 
    'data mining', 'predictive analytics', 'software testing', 'unit testing', 'debugging', 'technical documentation', 'ui/ux design', 
    'human-computer interaction', 'computer architecture', 'compiler design', 'operating system security', 'wireless networks', 'network security', 
    'data governance', 'data warehousing', 'data visualization', 'statistical analysis', 'reinforcement learning', 'explainable ai', 'generative ai',
    'software development life cycle (sdlc)', 'microservices architecture', 'containerization (docker, kubernetes)','cloud platforms (aws, azure, gcp)',
    'edge ai', 'quantum cryptography', 'high-performance computing', 'automated testing', 'software quality assurance', 'concurrency', 
    'multithreading', 'functional programming', 'object-oriented programming', 'event-driven programming', 'graph theory', 'computational biology', 
    'computational chemistry', 'computational physics', 'mathematical modeling', 'simulation', 'robotics', 'speech recognition',
    'computer-aided design (cad)', 'digital forensics', 'cyber law', 'data ethics', 'ai ethics', 'algorithmic bias', 'digital twins', 
    'cloud native development', 'serverless computing', 'edge networking', '5g technology', 'smart contracts', 'nft development', 
    'metaverse development', 'virtual economy', 'digital transformation', 'business intelligence', 'data lakes', 'data pipelines', 'data engineering', 
    'data science', 'knowledge graphs', 'semantic web', 'ontology engineering', 'computational linguistics', 'cognitive computing', 
    'ai-driven automation', 'explainable machine learning', 'ai model optimization', 'federated learning', 'privacy-preserving ai', 
    'zero trust security', 'secure software development', 'threat intelligence', 'incident response', 'cyber risk management', 'cloud-native security',
    'ai-powered cybersecurity', 'digital identity management', 'biometric security', 'quantum machine learning', 'ai for healthcare', 
    'ai for finance', 'ai for education', 'ai for manufacturing', 'ai for retail', 'ai for smart cities', 'ai for autonomous vehicles',
    'ai for space exploration', 'ai for climate science', 'ai for drug discovery', 'ai for personalized medicine', 'ai for agriculture', 
    'ai for supply chain optimization', 'ai for logistics', 'ai for energy management', 'ai for sustainability', 'ai for environmental science', 
    'ai for wildlife conservation', 'ai for oceanography', 'ai for astronomy', 'ai for astrobiology', 'ai for exoplanet research', 'ai for cosmology',
    'ai for theoretical physics', 'ai for particle physics', 'ai for nuclear engineering', 'ai for fusion energy', 'ai for renewable energy', 
    'ai for carbon capture', 'ai for green building', 'ai for circular economy', 'ai for waste management', 'ai for environmental policy', 
    'ai for climate advocacy', 'ai for eco-tourism', 'ai for nature conservation', 'ai for marine conservation', 'ai for hydrology', 'ai for geology', 
    'ai for paleontology', 'ai for archaeological excavation', 'ai for cultural heritage preservation', 'business analysis', 'project management',
    'strategic planning', 'leadership', 'digital marketing', 'seo', 'content marketing', 'social media marketing', 'public speaking', 'editing', 
    'persuasion', 'copywriting', 'critical thinking', 'decision-making', 'research', 'graphic design', 'web design', 'storytelling', 'typography', 
    'photography', 'sales strategy', 'negotiation', 'customer relationship management', 'financial analysis', 'human resources', 'talent acquisition',
    'employee training', 'supply chain management', 'risk management', 'accounting', 'legal research', 'public relations', 'event planning', 
    'market research', 'brand management', 'advertising', 'e-commerce', 'product management', 'networking', 'technical support', 'creative writing', 
    'journalism', 'translation', 'video production', 'audio editing', 'motion graphics', 'illustration', 'animation', 'customer service', 
    'conflict resolution', 'teamwork', 'time management', 'adaptability', 'emotional intelligence', 'problem-solving', 
    'entrepreneurship', 'business development', 'competitive analysis', 'investor relations', 'corporate communications', 'legal compliance', 
    'regulatory affairs', 'healthcare management', 'medical research', 'pharmaceutical sales', 'biotechnology', 'environmental science', 
    'sustainability','renewable energy', 'mechanical engineering', 'electrical engineering', 'civil engineering','construction management', 
    'real estate', 'hospitality management', 'tourism', 'retail management', 'fashion design', 'interior design', 'architecture', 
    'teaching', 'curriculum development', 'instructional design', 'e-learning', 'corporate training', 'coaching', 'mentoring', 'career counseling', 
    'psychology', 'counseling', 'therapy', 'mental health', 'business management',
]

# Extract text from PDF using pdfplumber
def extract_text_from_pdf(file) -> str:
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Extract text from DOCX using docx2txt
def extract_text_from_docx(file) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name
    return docx2txt.process(tmp_path)

# Master extractor: calls individual field extractors
def extract_fields(text: str) -> Dict[str, str]:
    fields = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_section(text, "education"),
        "experience": extract_section(text, "experience"),
        "linkedin_url": extract_links(text)["LinkedIn"],
        "github_url": extract_links(text)["GitHub"],
    }
    return fields

# ------------ Field Extractor Functions ------------

def extract_name(text: str) -> str:
    # Returns first non-empty line — simple heuristic
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines[0] if lines else "N/A"

def extract_email(text: str) -> str:
    match = re.findall(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', text)
    return match[0] if match else "N/A"

def extract_phone(text: str) -> str:
    match = re.findall(r'\+?\d[\d\s\-]{8,}', text)
    return match[0] if match else "N/A"

def extract_skills(text: str) -> str:
    text = text.lower()
    found_skills = list(set([skill for skill in SKILLS_DB if skill in text]))
    return ", ".join(sorted(found_skills)) if found_skills else "N/A"

def extract_section(text: str, section_name: str) -> str:
    lines = text.split('\n')
    content = ""
    capture = False
    for line in lines:
        if section_name.lower() in line.lower():
            capture = True
            continue
        elif capture and (line.strip() == "" or any(x in line.lower() for x in [
            "skills", "projects", "certifications", "languages", "hobbies", "experience", "education"
        ])):
            break
        elif capture:
            content += line + "\n"
    return content.strip() if content else "N/A"

def extract_links(text: str) -> Dict[str, str]:
    linkedin = re.findall(r'(https?://[^\s]+linkedin[^\s]+)', text, re.IGNORECASE)
    github = re.findall(r'(https?://[^\s]+github[^\s]+)', text, re.IGNORECASE)
    return {
        "LinkedIn": linkedin[0] if linkedin else "N/A",
        "GitHub": github[0] if github else "N/A"
    }