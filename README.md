# AI Resume Analyzer

## Windows setup

```powershell
git clone https://github.com/kamarajgokul2-lab/Internship_project.git
cd Internship_project
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
Copy-Item .env.example .env
notepad .env
.\launch.ps1
```

Add your own API key to `.env`, save it, and open http://localhost:8501 after launching. Local matching also works without an API key. If PowerShell blocks the launch script, run `.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501`.

The project-specific `.venv` keeps dependencies isolated. Set `GEMINI_API_KEY` in `.env` and optionally `GEMINI_MODEL` (default `gemini-flash-latest`). Restart after changing configuration. Never commit `.env`. The repository contains only an empty configuration example.

Upload a text-based PDF or paste resume text, add a job description, and analyze locally. Opt in to sending the text to Google for Gemini feedback and interview questions. Uploaded PDFs are processed in memory; reports remain in the browser session unless downloaded. Resume text sent to Gemini is limited to 25,000 characters and job text to 15,000.

Workflow: PDF extraction → keyword skill detection → TF-IDF cosine similarity → optional Gemini coaching → downloadable report.

Similarity is not an ATS score or hiring probability. Skills use a fixed vocabulary; absence in text does not prove lack of ability. Scanned PDFs need OCR; encrypted PDFs must be unlocked. Gemini requires a valid Google AI Studio key, access to the selected model, network access, and sufficient quota.

Demo: paste a Python/SQL resume and a Python/SQL/Docker job description. Compare local results, explain missing Docker evidence, then request AI coaching with consent. Future enhancements: OCR, broader skill taxonomy, multilingual matching, and structured AI responses.

## Validation

Run `.\.venv\Scripts\python.exe verify.py` for matching, skill boundary, blank PDF, Streamlit workflow, and consent checks. It also makes a small API request when a key is configured. No key or raw API errors are printed.

Local workflow checks and server health passed during development. Google accepted the configured development key, but generation returned temporary 503/504 service errors. Successful live AI coaching has not yet been verified.
