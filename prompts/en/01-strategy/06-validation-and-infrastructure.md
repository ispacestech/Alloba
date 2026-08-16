# Phase 1: Validation & Infrastructure (months 0-3) — cost focus

Goal: prove demand without writing code or spending money.

| Automation area | Tooling / stack strategy (free tier / serverless) | AI agent role | Action step |
| --- | --- | --- | --- |
| Platform MVP (e-commerce & LLM audit) | Hosting: Vercel or Cloudflare Pages. DB: Supabase Free Tier. AI backend: HuggingFace Inference API (open-source models via GGUF quantization for local/offline safety) + serverless functions. Payments: Stripe Connect / Flutterwave sandbox mode only until live revenue triggers the fee model. | LLM agent (code assistant) | Use AI to write, debug and deploy code itself (Cursor/Windsurf IDEs). No dev hire yet; you are the architect/manager of the agent's output. |
| Sales & marketing (lead gen for buyers/vendors) | LinkedIn free account; email automation Brevo/SendGrid free tier; content generator: AI script that scrapes competitor news (legally) and posts summaries to a company blog. | Growth agent (outreach bot) | "Find 10 procurement officers in Germany who use SAP Ariba" -> generate a personalized outreach email based on support-tier prompts, sent via a free auto-responder (Zapier). |
| Operations (customer support) | Chatbot flow builder (Voiceflow/Tidio free); knowledge base: publicly accessible regulations PDF stored in the RAG system to train the bot immediately. | Helpdesk agent | "Track my order" pulls from the logistics API; "What is your fee?" reads the knowledge engine. Complex queries escalate to an AI-drafted email with a summary attached. |
| Validation | Self-service vendor onboarding form in the browser (ECP portal). | — | System checks the data, flags gaps, and feeds the knowledge graph. |

No ads budget: organic viral loop targeting procurement forums where buyers post
pain points.
