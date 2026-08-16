# ADR-0005: Catalog data as bundled package data

- **Status**: Accepted
- **Date**: 2026-08-15
- **Owner**: Architecture

## Context

The sourcing agent needs a searchable supplier catalog. A database would be
operationally heavy for a gateway that is intentionally standalone and
cloud-upload ready.

## Decision

- The catalog ships as `src/alloba/data/products.json` (55 verified products),
  packaged via `[tool.setuptools.package-data] alloba = ["data/*.json"]`.
- `Catalog` loads it through `importlib.resources.files("alloba")` with an
  optional explicit path override (used by tests and future data sources).
- Catalog metadata (`size`, categories, regions) is served by
  `GET /v1/sourcing/catalog`.

## Consequences

- Zero-dependency runtime catalog, reproducible everywhere.
- Product data changes are code changes (versioned, reviewed).
- A database-backed catalog would supersede this ADR and update the architecture.

## Compliance

- `src/alloba/catalog.py`, `pyproject.toml`, `tests/test_catalog.py`
  (asserts `catalog.size == 55`).
