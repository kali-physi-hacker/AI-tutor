Security Notes

- JWT-based auth: access token in memory; refresh token via httpOnly cookie.
- Passwords hashed with bcrypt via Passlib.
- Input validation via Pydantic; strict types.
- Code execution disabled in MVP to avoid RCE.
- File uploads: PDF/MD only; stored locally in `storage/documents/`; parsed PDFs via `pypdf` (text only) to avoid embedded scripts.
- Rate-limiting, audit logging, and Sentry/OTel hooks recommended for production.
