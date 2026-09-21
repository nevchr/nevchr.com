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

The site has no build step. Configure Cloudflare Pages with the repository root as the output directory, or deploy the directory directly with Wrangler.

## Content notes

- Public contact: `chris@chrisneville.ca`
- No phone number is published.
- Source resumes are not stored in this repository.
- Open content questions are tracked in `QUESTIONS.md`.
