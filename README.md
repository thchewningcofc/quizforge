# quizforge
QuizForge is a fully client-side, single-file HTML application (v1.0, March 2026) that converts PDF study materials into interactive multiple-choice quizzes. The entire system—including a built-in 386-question CISSP exam bank—runs entirely in the browser with no server dependencies, no installation, and no account requirements.

## CSP maintenance
Keep the deployed Content Security Policy in `_headers` as the source of truth (hosting-level enforcement). If `index.html` includes a CSP `<meta http-equiv="Content-Security-Policy">`, it must match `_headers` to avoid policy drift between local previews and production.
