# quizforge

QuizForge is a fully client-side, single-file HTML application (v1.0, March 2026) that converts PDF study materials into interactive multiple-choice quizzes. The entire system—including a built-in 386-question CISSP exam bank—runs entirely in the browser with no server dependencies, no installation, and no account requirements.

## Environment setup

### Requirements
- A modern browser (Chrome, Edge, Firefox, Safari).
- Git (if you want to version and publish changes).
- Optional: a local static file server for closer parity with hosted behavior.

### Local run (quick start)
Because this is a client-side app, you can run it by opening `index.html` directly in your browser.

### Local run (recommended for development)
Run a static server from the project root to test under `http://localhost`:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`.

## Configure GitHub Pages

This repository includes a GitHub Actions workflow at `.github/workflows/deploy-pages.yml` that deploys the site to GitHub Pages on every push to `main`.

### One-time repository setup
1. Push this repository to GitHub.
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment** set **Source** to **GitHub Actions**.
4. Ensure your default publishing branch is `main` (or update the workflow trigger if you use another branch).
5. Push to `main` and wait for the **Deploy static site to GitHub Pages** workflow to complete.
6. Open your site at `https://<your-username>.github.io/<repo-name>/`.

### Included deployment files
- `.github/workflows/deploy-pages.yml` — builds/deploys the repository root as a Pages artifact.
- `.nojekyll` — disables Jekyll processing, which avoids underscore-file handling issues.

### Important hosting note
GitHub Pages does **not** use Netlify-style `_headers` files, so CSP headers in `_headers` are not applied there. QuizForge still runs on GitHub Pages because `index.html` includes a CSP `<meta>` policy for browser-enforced protection.

If you later host on Netlify/Cloudflare Pages/etc., keep `_headers` aligned with the `index.html` CSP meta policy.

## CSP maintenance
Keep the deployed Content Security Policy in `_headers` as the source of truth (hosting-level enforcement). If `index.html` includes a CSP `<meta http-equiv="Content-Security-Policy">`, it must match `_headers` to avoid policy drift between local previews and production.

## Built-in CISSP deck maintenance

The built-in `CISSP_DATA` exam bank in `index.html` now has a startup validator so malformed edits fail loudly during local testing and production load.

### What is validated
- `CISSP_DATA` is an array.
- Every question entry is an object with:
  - positive integer `id`
  - non-empty `question` string
  - `options` object containing non-empty `A`, `B`, `C`, and `D` strings
  - `answer` set to one of `A | B | C | D`
  - optional `explanation` as a string when present
- No duplicate IDs.
- No missing IDs in the sequence between the minimum and maximum ID values.

### Maintainer workflow
1. Edit `CISSP_DATA` in `index.html`.
2. Open `index.html` in a browser.
3. Verify no startup alert appears and no `CISSP_DATA validation failed` error is emitted in the browser console.
4. Spot-check deck metadata in the library screen (question count, launch behavior).

If validation fails, the built-in CISSP deck is intentionally excluded from the library until issues are fixed.
