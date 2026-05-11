# Contributing to AegisAI

> **"Security is a team sport."**  
> Thank you for considering a contribution to AegisAI. Every bug report, documentation fix, or new module makes the framework stronger for everyone.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Before You Start](#before-you-start)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Code](#submitting-code)
- [Development Setup](#development-setup)
- [Project Structure & Module Ownership](#project-structure--module-ownership)
- [Coding Standards](#coding-standards)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [License & Attribution](#license--attribution)

---

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and professional environment. Harassment, discrimination, or bad-faith contributions of any kind will not be tolerated.

If you witness or experience unacceptable behaviour, contact the maintainer directly at **savani.kunjkumar@gmail.com**.

---

## Before You Start

1. **Search existing issues first.** Your bug or idea may already be tracked.
2. **Open an issue before large PRs.** For anything beyond a small fix, start a conversation so we can align on approach before you invest significant time.
3. **Read the README.** Understand the project's architecture, phased roadmap, and goals before contributing.
4. **Respect the research-first ethos.** AegisAI prioritises correctness, explainability, and security over velocity.

---

## How to Contribute

### Reporting Bugs

Open a [GitHub Issue](https://github.com/savanikunjkumar/AegisAI/issues/new) and include:

```
**Environment**
- OS:
- Python version:
- AegisAI version / commit hash:
- Relevant dependencies (pip freeze excerpt):

**Steps to reproduce**
1.
2.
3.

**Expected behaviour**

**Actual behaviour**

**Logs / stack trace** (paste inside a code block)
```

Label your issue with `bug`. Add `security` if the bug has security implications — those are triaged first.

---

### Suggesting Features

Open a [GitHub Issue](https://github.com/savanikunjkumar/AegisAI/issues/new) with the label `enhancement` and include:

```
**Problem this solves**

**Proposed solution**

**Alternatives considered**

**Which phase / module does this affect?**
```

For research-heavy proposals (new adversarial defense methods, new explainability integrations, etc.), link to any relevant papers or prior art.

---

### Submitting Code

AegisAI accepts contributions in these categories:

| Category | Examples |
|----------|---------|
| **Bug fixes** | Incorrect retrieval logic, broken ingestion scripts |
| **New integrations** | Additional vector stores, LLM providers, guardrail libraries |
| **Adversarial defense modules** | New poisoning/evasion detection algorithms |
| **Explainability** | Additional SHAP/LIME/Captum use cases |
| **Docs & examples** | Usage guides, architecture notes, notebook tutorials |
| **Tests** | Unit tests, integration tests, edge case coverage |
| **Performance** | Retrieval latency improvements, batching optimisations |

---

## Development Setup

### 1. Fork & clone

```bash
git clone https://github.com/<your-username>/AegisAI.git
cd AegisAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies (including dev extras)

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt   # black, ruff, pytest, pre-commit
```

### 4. Set up pre-commit hooks

```bash
pre-commit install
```

This enforces formatting and linting automatically on every commit.

### 5. Configure environment variables

```bash
cp .env.example .env
# Fill in your API keys for Pinecone, Neo4j, and your LLM provider
```

### 6. Verify the setup

```bash
python -m pytest tests/ -v
```

All tests should pass before you begin working.

---

## Project Structure & Module Ownership

| Module | Purpose | Key files |
|--------|---------|-----------|
| `rag_pipeline/` | Threat data ingestion, vector search, knowledge graph | `ingestion.py`, `pinecone_client.py`, `neo4j_connector.py` |
| `llm_security/` | LLM agent logic and prompt templates | `agent.py`, `prompt_templates.py` |
| `adversarial_defense/` | Dataset poisoning & prompt injection defence | `poisoning_detection.py`, `prompt_guardrails.py` |
| `explainability/` | SHAP and LIME explainers | `shap_explainer.py`, `lime_explainer.py` |
| `docs/` | Architecture documentation | `architecture/*.md` |
| `data/` | **Local only — never committed to Git** | `cve_samples/`, `synthetic_logs/` |

When contributing to a module, keep changes scoped to that module's responsibility. Cross-cutting changes (e.g. shared utilities, config management) should be discussed in an issue first.

---

## Coding Standards

AegisAI enforces consistent style automatically via pre-commit. The rules:

### Formatting — `black`

```bash
black .
```

Line length: **88 characters** (black default).

### Linting — `ruff`

```bash
ruff check .
```

### Type hints

All public functions and methods **must** include type annotations:

```python
# Good
def query(self, text: str, top_k: int = 5) -> list[dict]:
    ...

# Bad
def query(self, text, top_k=5):
    ...
```

### Docstrings

Use Google-style docstrings for all public classes and functions:

```python
def query(self, text: str, top_k: int = 5) -> list[dict]:
    """Query the vector store for semantically similar documents.

    Args:
        text: The natural language query string.
        top_k: Number of top results to return.

    Returns:
        A list of matched document dictionaries with keys
        ``id``, ``score``, and ``metadata``.

    Raises:
        ConnectionError: If the vector store is unreachable.
    """
```

### Security-sensitive code

- Never log raw API keys, credentials, or PII.
- Never hardcode secrets — use environment variables via `python-dotenv`.
- Sanitise all inputs that will be passed to an LLM or database query.
- Any function that touches adversarial inputs must include a docstring noting threat assumptions.

---

## Commit Message Convention

AegisAI follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short summary in present tense>

[optional body]

[optional footer: Closes #123]
```

**Types:**

| Type | When to use |
|------|------------|
| `feat` | New feature or module |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Adding or fixing tests |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `chore` | Build process, dependency updates, tooling |
| `security` | Security-related fix or hardening |

**Examples:**

```bash
feat(rag_pipeline): add Weaviate vector store client
fix(adversarial_defense): correct false positive rate in poisoning detector
docs(architecture): update Neo4j connector design notes
security(llm_security): sanitise prompt inputs before LLM call
test(explainability): add SHAP unit tests for anomaly classifier
```

Keep the summary under 72 characters. Use the body to explain *why*, not *what*.

---

## Pull Request Process

1. **Branch naming:**  
   `feat/<short-description>`, `fix/<short-description>`, `docs/<short-description>`

   ```bash
   git checkout -b feat/weaviate-client
   ```

2. **Keep PRs focused.** One logical change per PR. Large changes are harder to review and slower to merge.

3. **Fill out the PR template** completely — describe the change, link the related issue, and list how you tested it.

4. **All checks must pass:**
   - `black` and `ruff` (pre-commit enforces this)
   - Full `pytest` suite
   - No secrets or large data files committed

5. **Request a review.** Tag `@savanikunjkumar` or leave a comment explaining what you'd like feedback on.

6. **Address review comments** promptly. PRs with no activity for 14 days may be closed.

7. **Squash before merge** if the commit history is noisy. The maintainer may do this during merge.

---

## Testing Guidelines

Tests live in `tests/` and mirror the module structure:

```
tests/
├── test_rag_pipeline.py
├── test_llm_security.py
├── test_adversarial_defense.py
└── test_explainability.py
```

### Running tests

```bash
# All tests
pytest tests/ -v

# Single module
pytest tests/test_adversarial_defense.py -v

# With coverage report
pytest tests/ --cov=. --cov-report=term-missing
```

### What to test

- **Unit tests** for all public functions — mock external services (Pinecone, Neo4j, LLM APIs).
- **Edge cases** — empty inputs, malformed CVE data, adversarial strings.
- **Security assertions** — verify that prompt guardrails block known injection patterns.

### Minimum coverage expectation

New code should maintain or improve the existing coverage level. PRs that significantly reduce coverage will be asked to add tests before merging.

---

## Documentation

Good documentation is as important as good code in a research project.

- **Code-level:** All public APIs must have docstrings (see Coding Standards above).
- **Architecture:** Significant new modules or design changes should be documented in `docs/architecture/`.
- **Usage examples:** Add a usage snippet to the relevant module's docstring or to `docs/`.
- **Changelog:** Summarise your change in `CHANGELOG.md` under `[Unreleased]`.

---

## License & Attribution

By submitting a contribution, you agree that your work will be licensed under the **MIT License** that covers this project.

You must retain the original copyright notice in any files you modify:

```
Copyright (c) 2025 Kunj Savani
```

Do not remove or alter authorship headers. If you make substantial additions to a file, you may add your own name on a new line below the original.

**Plagiarism of this project without attribution violates the MIT License.** If you build on AegisAI in your own work, you must credit the original repository.

---

<div align="center">

**Questions?** Open an issue or reach out directly.

[![Email](https://img.shields.io/badge/Email-savani.kunjkumar%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:savani.kunjkumar@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-savanikunjkumar-181717?style=flat-square&logo=github)](https://github.com/savanikunjkumar)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-kunj--savani-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/kunj-savani-08a38937a)

*Thank you for helping build a safer AI future.*

</div>
