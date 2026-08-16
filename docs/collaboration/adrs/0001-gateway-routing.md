# ADR-0001: Gateway routing — explicit routes first, transparent proxy for the rest

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Architecture

## Context

Alloba must be the single API entry point for clients while the platform
backend (ispaces Commerce) remains the system of record for business data.
Clients should not care whether a route is handled locally or by the backend.

## Decision

- Local capabilities are exposed under `/v1/gateway` and `/v1/sourcing`.
- Every other path is forwarded transparently to `ALLOBA_BACKEND_URL` via a
  catch-all proxy that preserves method, query, body, headers and status.
- Local routers are registered before the catch-all so they always win.
- Backend unreachability returns a JSON 502, never a hung connection.

## Consequences

- Clients have one origin to configure; backend swap requires no client change.
- The gateway is a single point of failure and must be observed (health check).
- Proxy limits and timeouts are required (60 s) to avoid resource leaks.

## Compliance

- `src/alloba/main.py` (router order + catch-all), `src/alloba/proxy.py`.
- Covered by `tests/test_gateway.py` (proxy forward, 502, 404 passthrough).
