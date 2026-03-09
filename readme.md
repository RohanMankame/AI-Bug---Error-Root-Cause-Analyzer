# AI Bug & Error Root Cause Analyzer

A tool that allows users to paste error messages, stack traces, build failures, logs, and instantly receive a clear explanation of the issue.

It finds the root cause, recommended fixes, and preventive best practices.
It leverages natural language understanding and reasoning to analyze error
context. The tool acts as a virtual senior engineer, reducing debugging time,
improving productivity, and minimizing dependency on subject matter experts.

## Features

* Pre‑processing step: the backend scans the input with regular expressions
  to detect the programming language, platform and principal error/message.
  This metadata is sent along with the raw text to the LLM so that queries are
  better focused.
* Streamlit UI for entering errors, viewing root cause, recommendations,
  metadata, and requesting a re‑evaluation.
* POST `/api/analyze` – run initial analysis on supplied error text.
* POST `/api/reevaluate` – ask follow‑up questions or challenge the result.
* Swagger UI at `/api/docs` (served by the backend).


## Getting started

### Prerequisites

* Python 3.10+ (Windows, Linux or macOS)
* `pip` and preferably a virtual environment.


### Run locally
#### Backend
1. Go to backend folder `cd backend`
2. Create/activate a venv:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate    # Windows
   # source .venv/bin/activate  # macOS/Linux
3. Install requirements `pip install -r requirements.txt`
4. run backend `python run.py`

#### Frontend
1. Go to frontend folder `cd frontend`
2. Run frontend `streamlit run streamlit_app.py`



