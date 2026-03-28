# quizforge
QuizForge is a fully client-side, single-file HTML application (v1.0, March 2026) that converts PDF study materials into interactive multiple-choice quizzes. The entire system—including a built-in 386-question CISSP exam bank—runs entirely in the browser with no server dependencies, no installation, and no account requirements.

## Validate embedded CISSP_DATA
When updating the built-in CISSP question bank in `index.html`, run the validator before committing:

```bash
python3 tests/validate_cissp_data.py
```

The validator enforces:
- each item includes `id`, `question`, `options.A/B/C/D`, and `answer`
- `answer` is one of `A|B|C|D`
- IDs are unique and strictly increasing
- question text does not contain import artifacts such as `QUESTION NO:` or `Answer: Explanation:`
