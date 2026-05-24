# Jenkins Static Analysis Pipeline

This project can run deterministic CI checks without invoking LLM, MCP, or RAG workflows.

## What Jenkins Runs

The `Jenkinsfile` runs:

1. Checkout repository.
2. Create Python virtual environment.
3. Install `requirements.txt`.
4. Install `requirements-dev.txt`.
5. Check formatting with `black --check .`.
6. Run lint checks with `ruff check .`.
7. Run Bandit security scan and archive the report.
8. Check Docker/containerlab readiness with `scripts/check_lab_ready.py`.
9. Run pytest:

```bash
pytest -v tests generated_scripts --junitxml=reports/pytest-report.xml
```

10. Optionally run SonarQube when `RUN_SONAR=true`.

## Jenkins Requirements

The Jenkins agent needs:

- Python 3.10
- Docker CLI access
- Access to the already-running `clab-ringlab-*` containers
- Sonar scanner only if `RUN_SONAR=true`

## SonarQube Setup

To enable SonarQube:

1. Install Jenkins SonarQube Scanner plugin.
2. Configure a SonarQube server in Jenkins named `SonarQube`.
3. Ensure `sonar-scanner` is available on the Jenkins agent.
4. Run the Jenkins job with `RUN_SONAR=true`.

## What Jenkins Does Not Run

Jenkins does not run:

- `python llm_runner.py`
- `python mcp_server/server.py`
- `python rag/build_index.py`

Those remain manual capabilities.
