# Resume Matcher

A command-line tool that compares your resume against a job description and tells you how well they match, which skills you're missing, and which keywords to look at. Think of it as a mini ATS (applicant tracking system) checker you can run offline.

## Why I built it
Recruiters and ATS software often filter resumes by keywords. This tool shows the gap between your resume and a specific job posting before you apply.

## Features
- Match score (0-100%) with a simple verdict
- Detects 40+ skills with aliases (`JS` = JavaScript, `DSA` = Data Structures, `k8s` = Kubernetes)
- Handles tricky names like `C++`, `C#`, `Node.js`, `CI/CD`
- Finds the most repeated keywords in the job description that your resume lacks
- Reads `.txt`, `.md`, and `.pdf` files
- `--json` output for use in other scripts
- No required dependencies (`pypdf` only for PDFs)

## Usage
```bash
python main.py samples/resume.txt samples/job_description.txt
```

Example output:
```
Match score: 43.1%  [#########-----------]
Verdict:     Weak match - big gaps
(skills 61.5% | keywords 0.0%)

Matched skills (8)
  algorithms, data structures, flask, git, python, rest api, sql, testing

Missing skills (5)
  agile, ci/cd, communication, django, docker
...
```

Other options:
```bash
python main.py my_resume.pdf job.txt --json     # machine-readable output
python main.py my_resume.txt job.txt --top 25   # check more JD keywords
```

## How the score works
- **Skills score (70%)**: share of the job's required skills found in your resume
- **Keyword score (30%)**: share of the job's most repeated non-skill words found in your resume

It's a rough guide, not a real ATS. Only add skills to your resume if you actually have them.

## Project structure
```
resume-matcher/
├── main.py
├── matcher/
│   ├── skills.py     # skills + aliases (edit to add your own)
│   ├── text.py       # file reading + tokenizing
│   ├── analyzer.py   # extraction + scoring
│   └── cli.py        # command line interface
├── samples/
├── tests/
└── requirements.txt
```

## Run tests
```bash
pip install -r requirements.txt
pytest
```

## Ideas to extend
- Export a PDF/HTML report
- Weight skills (must-have vs nice-to-have)
- Use TF-IDF or embeddings for smarter keyword matching
- Add a small web UI

## License
MIT
