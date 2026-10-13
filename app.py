import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from analyzer import parse_pdf, match_resume, gemini_feedback, safe_error

load_dotenv(Path(__file__).with_name('.env'), override=True)
st.set_page_config(page_title='AI Resume Analyzer', page_icon='📄', layout='wide')
st.title('📄 AI Resume Analyzer')
st.caption('Understand your fit, improve your resume, and prepare for interviews.')
with st.sidebar:
    st.header('How it works')
    st.write('1. Upload a text-based PDF or paste your resume.\n2. Add the target job description.\n3. Compare locally or request Gemini coaching.')
    st.caption('Local matching uses keywords and text similarity. It is a guide, not a hiring prediction. Skill detection uses a limited vocabulary and may miss synonyms.')
    st.write('Gemini key configured' if os.getenv('GEMINI_API_KEY') else 'Add a Gemini API key to .env for AI coaching.')
def clear_report():
    st.session_state.pop('report', None)

upload = st.file_uploader('Resume PDF (maximum 5 MB)', type=['pdf'], on_change=clear_report)
resume = ''
if upload:
    if upload.size > 5 * 1024 * 1024:
        st.error('Upload a PDF smaller than 5 MB.')
    else:
        try:
            resume = parse_pdf(upload.getvalue())
            with st.expander('Extracted resume text'):
                st.text(resume)
        except Exception as exc:
            st.error(str(exc) if isinstance(exc, ValueError) else 'Unable to read this PDF. Upload a valid text-based PDF.')
pasted = st.text_area('Or paste resume text', height=180, on_change=clear_report)
resume = pasted.strip() or resume
job = st.text_area('Target job description', height=180, on_change=clear_report)
consent = st.checkbox('Send my resume and job description to Google Gemini for AI feedback.')
local, ai = st.columns(2)
compare = local.button('Analyze job match', use_container_width=True)
coach = ai.button('Get AI feedback & interview questions', use_container_width=True)
if compare or coach:
    st.session_state.pop('report', None)
    if len(resume.strip()) < 30 or len(job.strip()) < 30:
        st.error('Please provide a resume and job description, each with at least 30 characters.')
    else:
        try:
            result = match_resume(resume, job)
            report = f"## Local job match\nText similarity: {result['similarity']}%\n\nMatched skills: {', '.join(result['matched']) or 'None detected'}\n\nSkills not found in resume: {', '.join(result['missing']) or 'None detected'}\n"
            st.session_state['report'] = report
            if coach:
                if not consent:
                    st.warning('Select the consent checkbox to request Gemini feedback. Local results are ready below.')
                elif not os.getenv('GEMINI_API_KEY'):
                    st.error('Set GEMINI_API_KEY in the local .env file.')
                else:
                    with st.spinner('Preparing tailored feedback…'):
                        try:
                            feedback = gemini_feedback(resume, job, os.environ['GEMINI_API_KEY'], os.getenv('GEMINI_MODEL', 'gemini-flash-latest'))
                            st.session_state['report'] += '\n## Gemini coaching\n' + feedback
                        except Exception as exc:
                            st.error(safe_error(exc))
        except ValueError:
            st.error('No meaningful words found. Please provide more complete text.')
if 'report' in st.session_state:
    st.markdown(st.session_state['report'])
    st.download_button('Download report', st.session_state['report'], 'resume_analysis.md', 'text/markdown')

