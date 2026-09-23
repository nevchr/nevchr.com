# nevchr.com

Professional portfolio for Christopher Neville, built as a lightweight static site for Cloudflare Pages.

## Local preview

```powershell
python -m http.server 4173
```

Then open `http://localhost:4173`.

## Validation

```powershell
python scripts/check_site.py
node --check script.js
```

## Deployment

The site has no build step. Use the repository root as the output directory for Git integration or Wrangler. For this update, a root-level static upload bundle is prepared at `tmp/cloudflare-upload-ready-2026-09-22.zip`; it contains only public site files, not this README or the follow-up questions.

First check the existing Cloudflare Pages project’s deployment mode. The dashboard accepts a ZIP for a Direct Upload project. Git-integrated Pages projects do not support dashboard drag-and-drop; use that project’s connected Git branch instead, since a push may deploy automatically. See [Cloudflare’s Direct Upload guide](https://developers.cloudflare.com/pages/get-started/direct-upload/) for the current steps.

## Content notes

- Public contact: `chris@chrisneville.ca`
- No phone number is published.
- Source resumes are not stored in this repository.
- Open content questions are tracked in `QUESTIONS.md`.
