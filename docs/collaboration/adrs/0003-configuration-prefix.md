# ADR-0003: Configuration via pydantic-settings with an `ALLOBA_` prefix

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Architecture

## Context

The gateway has many knobs (backend URL, RAG paths, Ollama endpoint, agent
mode, CORS allow-list). The workspace rule requires project-specific variables
to carry a project prefix so they never collide across shared compose files.

## Decision

- All settings live in `Settings` (pydantic-settings) with
  `model_config = {"env_prefix": "ALLOBA_"}`.
- `.env.example` documents every variable; `.env` is git-ignored.
- `ALLOBA_ALLOWED_ORIGINS` defaults to a bounded allow-list, never `*`.
- Shared infrastructure variables that appear in multiple compose files keep
  their bare names (`OLLAMA_BASE_URL`), per workspace convention.

## Consequences

- Fail-fast startup on invalid values (pydantic validation).
- Consistent naming for cloud deployments and CI.
- The old `AFROMART_` prefix is retired during the rebrand; nothing reads it.

## Compliance

- `src/alloba/config.py`, `.env.example`, `docker-compose.yml`, READMEs.
