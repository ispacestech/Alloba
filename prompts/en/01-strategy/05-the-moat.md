# The Moat: building trust without money

To win the B2B sourcing global market, you do not need to be cheaper — you need
to be **trustable**.

## The "Bootstrap Security" protocol

Since a dedicated SOC team is unaffordable initially:

- **Automated scanning**: deploy open-source scanners (e.g. Trivy for
  containers) into the CI/CD pipeline on every commit. This prevents
  vulnerabilities from being deployed and reduces manual security work to near
  zero.
- **Data minimization by design**: configure the ECP knowledge engine to store
  only essential compliance data locally and hash everything else before
  sending it out for AI processing. Sensitive (encrypted) vs public logs are
  stored differently automatically via scripts, not manual admin work.
- **Open-source governance**: publish the audit-log schema on GitHub under a
  license. Open, compliant tooling makes buyers trust that nothing is hidden in
  black-box AI code. This replaces expensive vendor security audits for early
  customers who value transparency over closed ecosystems.

## Application to Alloba

- CI runs `ruff` + `pytest` on every PR (see `.github/workflows/ci.yml`).
- The FAISS store is safe-serialized (no pickle) and the audit models are
  public (`src/alloba/models.py`).
- Compliance answers always cite sources — transparency as a product feature.
