import os, sys, io
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from dotenv import load_dotenv
from analyzer import match_resume, skills_in, parse_pdf, safe_error
from streamlit.testing.v1 import AppTest
r = match_resume('Python SQL developer building data pipelines and Git projects.', 'Seeking Python SQL Docker developer for data pipelines.')
assert r['missing'] == ['Docker'] and 'Python' in r['matched']
assert 'Java' not in skills_in('JavaScript engineer')
from pypdf import PdfWriter
w = PdfWriter(); w.add_blank_page(width=612, height=792)
b = io.BytesIO(); w.write(b)
try: parse_pdf(b.getvalue()); raise AssertionError('blank PDF accepted')
except ValueError: pass
at = AppTest.from_file('app.py').run()
assert not at.exception
at.text_area[0].set_value('Python SQL developer building data pipelines with Git and testing.')
at.text_area[1].set_value('Seeking Python SQL Docker developer for data pipelines and testing.')
at.button[0].click().run()
assert not at.exception and 'Docker' in at.session_state['report']
at.button[1].click().run()
assert at.warning and not at.exception
print('PASS: matching, skill boundaries, blank PDF, UI matching and consent')
load_dotenv('.env')
if not os.getenv('GEMINI_API_KEY'):
    print('SKIP: live API check (no local API key configured)')
    sys.exit(0)
from google import genai
from google.genai import types
try:
    with genai.Client(api_key=os.environ['GEMINI_API_KEY'], http_options=types.HttpOptions(timeout=20000)) as client:
        response = client.models.generate_content(model=os.getenv('GEMINI_MODEL'), contents='Reply with OK only.')
        print('GEMINI_VALID' if response.text else 'GEMINI_EMPTY_RESPONSE')
except Exception as exc:
    print('GEMINI_CHECK:', getattr(exc, 'code', None), safe_error(exc))
    details = getattr(exc, 'details', None)
    if isinstance(details, dict):
        error = details.get('error', {})
        print('GEMINI_STATUS:', error.get('status', 'unknown'))
        for item in error.get('details', []):
            if isinstance(item, dict) and item.get('reason'):
                print('GEMINI_REASON:', item['reason'])
