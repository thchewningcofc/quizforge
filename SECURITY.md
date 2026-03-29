# Security Policy

## Supported Versions

This project is a single-page static application. Security fixes are applied on `main`.

## Reporting a Vulnerability

If you find a security issue, please open a **private security advisory** in GitHub (preferred) or email the maintainer directly.

Please include:
- Reproduction steps
- Impact assessment
- Suggested remediation (if available)

## Public Repo Hardening Notes

- Do **not** commit API keys, `.env` files, certificates, or private keys.
- QuizForge stores deck data in `localStorage` and stores API keys in `sessionStorage` only (cleared when browser tab closes).
- Keep the CSP in `index.html` and `_headers` in sync.
- Prefer HTTPS hosting and keep security headers enabled.
