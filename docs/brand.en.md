# Alloba — Brand Identity

Alloba sits inside the **ispaces** brand family. The master brand is **ispaces**
("Ethics by design.") with its product brand **AfroMART** (ispaces Commerce,
"Trade that grows Africa."). Alloba is the gateway and sourcing product of this
family — its identity inherits the same values, voice and visual tokens.

Source of truth: `../brand/brand-guidelines.md` and the SVG marks in `brand/`.

## Values

- **Ethics by design** — guardrails before features, auditability by default.
- **Trade that grows Africa** — commerce as an engine of pan-African growth.
- **Plain, calm, principled** — no hype, no noise, commitments stated as
  commitments.

## Voice

- Communicate like a confident engineer, not a marketer.
- State what the system does, what it does not do, and what the human decides.
- Answers cite sources; the assistant identifies itself as AI (see
  `kb/docs/01_Ethical_AI_Guardrails.md`).

## Visual tokens

| Token | Value | Usage |
| --- | --- | --- |
| Primary | `#4F46E5` | Primary actions, links, active states |
| Secondary | `#0EA5E9` | Supporting actions, information |
| Accent | `#F59E0B` | Highlights, calls to action |
| Success | `#10B981` | Confirmation, health |
| Error | `#EF4444` | Errors, destructive actions |
| Surface | `#1E293B` | Dark surfaces, panels |
| Text | `#F8FAFC` | Text on dark surfaces |
| AfroMART tile | `#007A6E` | AfroMART-specific identity |

## Naming

- **Product**: Alloba (gateway + agentic sourcing).
- **Service labels**: `service: "alloba"`, image `alloba/gateway:<version>`.
- **Env prefix**: `ALLOBA_` for project-specific variables.
- **Brand hierarchy**: ispaces (master) → AfroMART / ispaces Commerce (marketplace
  product) → Alloba (gateway product). Alloba never contradicts the master brand.

## Marks

- `brand/ispaces-mark.svg` — master brand mark.
- `brand/afromart-mark.svg` — AfroMART product mark.
- Alloba does not ship its own standalone mark yet; product surfaces use the
  AfroMART mark with an "Alloba" wordmark label.

## Usage rules

- Keep the two-colour contrast for accessibility (WCAG AA on primary text).
- Never recolor marks outside the token palette.
- Always label AI-generated content (briefs, compliance answers).
