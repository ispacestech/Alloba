# Serverless deployment playbook (Vercel + Supabase)

Full-stack application playbook: integration and security guide for modern
Next.js/React applications using Supabase. This is a reference for the platform
frontend/serverless layer; Alloba itself deploys as a container gateway (see
`docs/infrastructure.en.md`).

## Learning plan

| Phase | Topic | Est. time | Key objectives |
| --- | --- | --- | --- |
| 1 | Supabase infrastructure setup | 45 min | Create project, configure Auth (email/Google), database schema and Row Level Security (RLS). |
| 2 | Next.js client integration | 60 min | Install the Supabase SDK in App or Pages router; configure `useEffect` for secure client data loading. |
| 3 | Security environment config | 45 min | Master `.env.local`, Vercel environment variables, service-role key management (backend vs client). |
| 4 | Architecture visualization | 15 min | Use Mermaid to diagram data flow: Auth provider -> API route -> database. |

## Security rules of thumb

- **Client-side (browser)**: never use the service-role key. Only expose anon
  keys in `.env.local`.
- **Server-side (API routes / edge functions)**: use serverless connection
  strings / service keys injected at deploy time — never hardcoded secrets.
- **Vercel**: `vercel env pull` syncs local dev vars with production safely
  before committing.

Example `.env.local` (never commit):

```bash
# .env.local (DO NOT COMMIT TO GITHUB)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=...           # public key, safe for browser
SUPABASE_SERVICE_ROLE_KEY=...               # server-only, use Vercel secrets panel
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Invalid API key` | Service-role key used in the browser client. | Switch to the anon key; keep service role server-side only. |
| `Connection refused` | Wrong URL or CORS misconfiguration. | Project Settings > API: add allowed origins; enable anon access on RLS policies for dev, then lock down for prod. |
| Empty schema | Migrations not run. | SQL Editor: paste the migration file (e.g. create users table) and refresh. |
| RLS deny (403/561) | RLS enabled but no policy allows the current user. | Authentication > RLS: add policies for `auth.uid()`; restrict private reads to the owner. |
| `.env` not working in Vercel dev | Environment file not pulled. | `vercel env pull` to sync `.env.example` with the secrets panel. |

## Next steps

1. Test the login flow locally before deploying API routes.
2. Move sensitive `SERVICE_ROLE_KEY` values to the Vercel dashboard — never
   commit raw secrets.
3. Paste the Mermaid flow diagram into the repo README for team documentation.
