# quizforge
QuizForge is a fully client-side, single-file HTML application (v1.0, March 2026) that converts PDF study materials into interactive multiple-choice quizzes. The entire system—including a built-in 386-question CISSP exam bank—runs entirely in the browser with no server dependencies, no installation, and no account requirements.

## Run from GitHub (GitHub Pages)

You can host and run QuizForge directly from your GitHub repo with GitHub Pages:

1. Fork or create a repository and push these files (`index.html`, `_headers`, and `README.md`).
2. In GitHub, open **Settings → Pages**.
3. Under **Build and deployment**:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` (or your default branch)
   - **Folder**: `/ (root)`
4. Click **Save** and wait for deployment to complete.
5. Open your published URL (`https://<your-username>.github.io/<repo-name>/`).

### Important hosting note
GitHub Pages does **not** use Netlify-style `_headers` files, so CSP headers in `_headers` will not be applied there. QuizForge still runs on GitHub Pages because `index.html` includes a CSP `<meta>` policy for browser-enforced protection.

If you later host on Netlify/Cloudflare Pages/etc., keep `_headers` aligned with the `index.html` CSP meta policy.

## Local run (no install)

Because this is a client-side app, you can also run it locally by opening `index.html` in your browser.

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
