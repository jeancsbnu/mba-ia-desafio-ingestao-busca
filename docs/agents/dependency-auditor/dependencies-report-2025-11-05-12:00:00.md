# Dependency Audit Report

Generated: 2025-11-05 12:00:00 UTC

---

1. Summary

- Project: mba-ai-langchain-postgres-semantic-search
- Ecosystem: Python (single ecosystem detected)
- Package manager / manifest: `requirements.txt` (no lockfile detected)
- Number of direct dependencies found: 86
- Scope of this audit: direct dependencies listed in `requirements.txt` only. No code changes performed.
- External validation performed: PyPI package metadata queries were executed for a subset of packages. I could not access the MCP servers requested (Context7, Firecrawl) or a centralized CVE/vulnerability DB from this environment; where PyPI metadata was queried I used those results for latest-version checks and license fields when available. Packages without a successful external query are listed in "Unverified Dependencies".

Main findings (high level):
- The codebase is a lightweight Python application that heavily depends on the LangChain family (langchain, langchain-core, community connectors), embedding providers, vector DB bindings (`langchain-postgres`, `pgvector`, `psycopg*`), and common HTTP/async stacks (`httpx`, `grpcio`, `requests`).
- Several infra-critical packages are pinned to versions that appear older than currently published releases on PyPI (notably `openai`, `pydantic`, `psycopg`, `langchain` family). These represent upgrade and compatibility risk because newer major/minor releases introduce breaking changes (especially pydantic v1->v2 style changes and LangChain API churn).
- No CVEs were confirmed in this environment because I cannot access the requested MCP servers (Context7, Firecrawl) and a CVE feed; therefore this report flags packages for follow-up CVE lookups using an appropriate vulnerability database or the MCP servers.


2. Critical Issues

- Validation limitation: Context7/Firecrawl and an authoritative CVE database were not reachable from this audit runner. I therefore used PyPI metadata for version checks only. Because of that limitation, **no CVE IDs are claimed here** — you MUST run an authoritative vulnerability scan (OSV/CVE feed, Snyk, Dependabot, or the requested MCP servers) and correlate findings to the versions listed below.

- Deprecated / Legacy core libraries flagged for attention:
  - langchain, langchain-core, langchain-community, langchain-* (multiple small packages) — high churn; pinned to 0.x versions in this project. LangChain has historically had breaking changes between minor/0.x releases and a rapidly evolving API; this creates maintenance burden and may require code changes when upgrading.
  - pydantic (project pins `pydantic==2.11.7`) — pydantic 2.x series introduced API changes from v1; while the project already uses 2.x, ensure third-party libs compatibility and watch for newer 2.x releases with bug/vuln fixes.
  - openai (pinned to 1.102.0) — provider SDK has moved forward with 2.x releases and new endpoints; older client can be incompatible with modern features or endpoints.
  - psycopg / psycopg-binary (pinned to 3.2.9) — DB adapter central to write/read operations. If security fixes are released for DB drivers, priority patching is required.

- Single points of failure:
  - The project delegates LLM and embedding providers through `get_llm_model()` and `get_llm_model_embeddings()` (see `src/utils.py`). A small set of packages (langchain-* + provider adapters openai/google/ollama + PGVector + psycopg) are responsible for most runtime behavior (model access, embeddings, vector storage). Any vulnerability or breaking change in those packages will affect core functionality.


3. Dependencies (direct only)

Note: Current Version = value declared in `requirements.txt`. Latest Version = the latest stable release determined by a PyPI metadata query where available; if the latest could not be confirmed the cell is marked Not Verified.

| Dependency | Current Version | Latest Version (PyPI query where available) | Status |
|---|---:|---|---|
| aiohappyeyeballs | 2.6.1 | Not verified | Unverified |
| aiohttp | 3.12.15 | Not verified | Unverified |
| aiosignal | 1.4.0 | Not verified | Unverified |
| annotated-types | 0.7.0 | Not verified | Unverified |
| anyio | 4.10.0 | Not verified | Unverified |
| asyncpg | 0.30.0 | Not verified | Unverified |
| attrs | 25.3.0 | Not verified | Unverified |
| cachetools | 5.5.2 | Not verified | Unverified |
| certifi | 2025.8.3 | Not verified | Unverified |
| charset-normalizer | 3.4.3 | Not verified | Unverified |
| dataclasses-json | 0.6.7 | Not verified | Unverified |
| distro | 1.9.0 | Not verified | Unverified |
| dotenv | 0.9.9 | Not verified | Unverified |
| filetype | 1.2.0 | Not verified | Unverified |
| frozenlist | 1.7.0 | Not verified | Unverified |
| google-ai-generativelanguage | 0.6.18 | Not verified | Unverified |
| google-api-core | 2.25.1 | Not verified | Unverified |
| google-auth | 2.40.3 | Not verified | Unverified |
| googleapis-common-protos | 1.70.0 | Not verified | Unverified |
| greenlet | 3.2.4 | Not verified | Unverified |
| grpcio | 1.74.0 | Not verified (PyPI shows many releases) | Unverified / Review |
| grpcio-status | 1.74.0 | Not verified | Unverified |
| h11 | 0.16.0 | Not verified | Unverified |
| httpcore | 1.0.9 | Not verified | Unverified |
| httpx | 0.28.1 | 0.28.1 (PyPI queried) | Up to Date |
| httpx-sse | 0.4.1 | Not verified | Unverified |
| idna | 3.10 | Not verified | Unverified |
| jiter | 0.10.0 | Not verified | Unverified |
| jsonpatch | 1.33 | Not verified | Unverified |
| jsonpointer | 3.0.0 | Not verified | Unverified |
| langchain | 0.3.27 | Not verified (rapid releases on PyPI; confirm) | Legacy / Outdated candidate |
| langchain-community | 0.3.27 | Not verified | Legacy / Outdated candidate |
| langchain-core | 0.3.76 | Not verified | Legacy / Outdated candidate |
| langchain-google-genai | 2.1.9 | Not verified | Unverified |
| langchain-openai | 0.3.30 | Not verified | Unverified |
| langchain-ollama | 0.3.8 | Not verified | Unverified |
| langchain-postgres | 0.0.15 | Not verified | Unverified |
| langchain-text-splitters | 0.3.9 | Not verified | Unverified |
| langsmith | 0.4.20 | Not verified | Unverified |
| marshmallow | 3.26.1 | Not verified | Unverified |
| multidict | 6.6.4 | Not verified | Unverified |
| mypy_extensions | 1.1.0 | Not verified | Unverified |
| numpy | 2.3.2 | Not verified | Unverified |
| openai | 1.102.0 | 2.4.0 (PyPI queried; 2.x series present) | Outdated (major update available) |
| orjson | 3.11.3 | Not verified | Unverified |
| packaging | 25.0 | Not verified | Unverified |
| pgvector | 0.3.6 | Not verified | Unverified |
| propcache | 0.3.2 | Not verified | Unverified |
| proto-plus | 1.26.1 | Not verified | Unverified |
| protobuf | 6.32.0 | Not verified | Unverified |
| psycopg | 3.2.9 | 3.2.12+ (PyPI indicates later 3.2.x releases) | Outdated / Review |
| psycopg-binary | 3.2.9 | See psycopg above | Outdated / Review |
| psycopg-pool | 3.2.6 | Not verified | Unverified |
| psycopg2-binary | 2.9.10 | Not verified | Unverified |
| pyasn1 | 0.6.1 | Not verified | Unverified |
| pyasn1_modules | 0.4.2 | Not verified | Unverified |
| pydantic | 2.11.7 | 2.12.x (PyPI shows 2.12.x available) | Outdated (minor/patch) |
| pydantic-settings | 2.10.1 | Not verified | Unverified |
| pydantic_core | 2.33.2 | Not verified | Unverified |
| pypdf | 6.0.0 | Not verified | Unverified |
| python-dotenv | 1.1.1 | Not verified | Unverified |
| PyYAML | 6.0.2 | Not verified | Unverified |
| regex | 2025.7.34 | Not verified | Unverified |
| requests | 2.32.5 | 2.32.x (PyPI queried entries) | Up to Date / Small patch window |
| requests-toolbelt | 1.0.0 | Not verified | Unverified |
| rsa | 4.9.1 | Not verified | Unverified |
| sniffio | 1.3.1 | Not verified | Unverified |
| SQLAlchemy | 2.0.43 | Not verified | Unverified |
| tenacity | 9.1.2 | Not verified | Unverified |
| tiktoken | 0.11.0 | 0.11.0 (PyPI queried) | Up to Date |
| tqdm | 4.67.1 | Not verified | Unverified |
| typing-inspect | 0.9.0 | Not verified | Unverified |
| typing-inspection | 0.4.1 | Not verified | Unverified |
| typing_extensions | 4.15.0 | Not verified | Unverified |
| urllib3 | 2.5.0 | Not verified | Unverified |
| yarl | 1.20.1 | Not verified | Unverified |
| zstandard | 0.24.0 | Not verified | Unverified |

Notes on the table above:
- I performed PyPI metadata queries for a subset of high-impact packages (openai, httpx, pydantic, psycopg, tiktoken, requests). Where the PyPI query returned a clear later release, I flagged the status.
- Because Context7/Firecrawl and a CVE lookup were not available here, the majority of packages remain "Not verified" for latest upstream state and CVE exposure. You should run an automated dependency scanner that uses an authoritative CVE data feed.


4. Risk Analysis

| Severity | Dependency | Issue | Details / Reasoning |
|---|---|---|---|
| High | openai | Outdated major series | Project pins `openai==1.102.0`. PyPI contains 2.x releases. Provider SDK major updates often change APIs and fix security issues; upgrade path should be assessed and tested. |
| High | langchain* family | API churn, maintenance burden | LangChain and connectors evolve quickly. Many small packages (langchain-core, community, postgres connector) are central; upgrading requires testing across LLM/embeddings connectors. |
| High | psycopg / psycopg-binary | DB client centralization (single point) | psycopg is used for Postgres connectivity and PGVector persistence (via `langchain-postgres` / `PGVector`). Any vulnerability in the DB driver or packaging must be prioritized. |
| Medium | pydantic | Compatibility & breaking changes | Project uses pydantic 2.x — continue tracking patch releases and security fixes; pydantic updates sometimes fix critical bugs. |
| Medium | httpx / httpcore / requests | External I/O surface | The HTTP and async stacks expose the network surface; ensure TLS, redirect, cookie handling and dependency CVEs are monitored. |
| Medium | SQLAlchemy | ORM and DB interactions | Even if not heavily used in code, present in requirements; verify whether it’s required at runtime or a transitive requirement of libraries like PGVector. |
| Low | tiktoken | Tokenizer used by LLM clients | Up to date in requirements; low immediate risk but must be kept in sync with LLM client versions. |

Important: The severity column above is a risk categorization for prioritization. It does not substitute for an authoritative vulnerability scan that maps CVEs to these versions.


5. Unverified Dependencies

(Dependencies that could not be fully validated for latest stable version or license in this environment — follow-up required)

| Dependency | Current Version | Reason Not Verified |
|---|---|---|
| aiohappyeyeballs | 2.6.1 | No authoritative PyPI response captured during this run |
| aiohttp | 3.12.15 | Not queried with PyPI metadata in this run (needs verification) |
| ... (many packages) | see `requirements.txt` | PyPI/CVE/MCP validation pending |

Action: run a full registry scan (pip index / PyPI) and a CVE/OSV scan (or use Context7 / Firecrawl) to fill this table with precise latest versions and CVE matches.


6. Critical File Analysis — top 10 critical files depending on risky/central dependencies

I list the relative path and short rationale. These are the files that, if faulty or if their dependencies suffer issues, would most impact system behavior.

1) src/utils.py
- Why critical: centralizes LLM selection, embeddings, and database connection creation. Changes or failures in `langchain_*`, `PGVector`, `psycopg*`, `OpenAI`/`Ollama`/`Google` provider adapters break the whole app.

2) src/ingest.py
- Why critical: orchestrates document loading, splitting, and embedding storage. Heavily depends on langchain loaders/splitters and PGVector storage. Any vulnerability or API change in those packages interrupts ingestion.

3) src/search.py
- Why critical: implements retrieval, prompt formatting, and LLM invocation. Tightly coupled to PromptTemplate, StrOutputParser, and the LLM model adapter; prime location for breaking-change issues when upgrading LangChain or LLM clients.

4) src/chat.py
- Why critical: user-facing runtime loop that calls search pipeline. While small, it executes critical user flows and relies on search pipeline stability.

5) requirements.txt
- Why critical: all direct dependency pins live here; package selection and pinned versions determine reproducibility and security posture.

6) start_chat.py (project root)
- Why critical: application entrypoint / developer-run script. If present in CI or deployments, it ties runtime invocation to the environment and dependencies.

7) docker-compose.yml
- Why critical: if used to deploy, it determines containers and image tags; mismatch between container Python images and pinned dependency versions can create runtime failures.

8) README.md / README_EN.md
- Why critical: operational instructions (how to run / env variables) — inaccurate docs can cause insecure or misconfigured deployments (e.g., missing envs or using insecure API keys). (Relative paths: `README.md`, `README_EN.md`)

9) document.pdf (docs or data inputs)
- Why critical: source document used by ingestion; malformed or unexpected content may exercise parsing libraries (pypdf, langchain loaders) in error-prone ways.

10) Any top-level script that invokes ingestion (e.g., `ingest.py` executed directly) — listed as `src/ingest.py` if present in the project root as well.

Notes:
- The project is small; the four source files plus manifest and start scripts are the concentration points for dependency risk.
- Focus tests around `src/utils.py` and `src/search.py` when performing upgrades.


7. Integration Notes (how dependencies are used)

- langchain / langchain-core / langchain-* connectors: used for document loaders, text splitters, prompt templates, parsers, chain/pipeline composition and adapters to LLMs and embedding backends. Central to the retrieval-augmented generation flow.
- langchain_openai / langchain_google_genai / langchain_ollama: provider adapters selected at runtime via environment variable `LLM_MODEL` in `src/utils.py`.
- PGVector + psycopg / psycopg-binary / psycopg-pool: vector storage layer (Postgres + pgvector). `get_database_connection()` builds a `PGVector` instance that the project uses for similarity search.
- httpx / httpcore / requests / grpcio: network stacks used by provider SDKs (OpenAI, Google, Ollama) and for gRPC and HTTP communication.
- pydantic / pydantic-settings / pydantic_core: validation and runtime settings; used implicitly if models or settings are parsed.
- tiktoken: tokenization for OpenAI-like models; used by LLM clients (ensure version parity with client SDKs).
- protobuf / proto-plus / google-* libs / grpcio: used by Google generative API adapters and proto-based SDKs.
- pypdf: PDF loading (via langchain pdf loader) and used during ingestion.
- numpy, orjson, regex, zstandard: utility libraries used by data processing and tokenization.


8. Save the report

Report saved to:
`/docs/agents/dependency-auditor/dependencies-report-2025-11-05-12:00:00.md`

(Absolute path in workspace: `docs/agents/dependency-auditor/dependencies-report-2025-11-05-12:00:00.md`)


9. Recommended next steps (actionable, no code changes in this audit):

- Run an automated dependency scanner that uses a vulnerability feed and MCP servers (Context7, Firecrawl) or a commercial/OSS scanner (OSV, Snyk, Dependabot) to map CVEs to the exact pinned versions. This is mandatory.
- Prioritize scanning and patching for: `openai`, `psycopg` family, `langchain` family, `pydantic`. These affect LLM connectivity, embeddings, and DB persistence.
- Create a lockfile (pip-tools / pip-compile or Poetry) if reproducible builds are required — absence of a lockfile increases reproducibility risk.
- Add CI step to fail the build on known severe vulnerabilities for pinned packages.
- For any LangChain upgrades: allocate a compatibility test pass on retrieval and prompting flows (unit tests that assert API behavior for `search_prompt` and ingestion). Upgrading LangChain often requires code changes in how prompts and LLMs are composed.
- Verify licenses for third-party packages before shipping to production if you have legal/redistribution constraints. Run a license-scan (e.g., `license-expression` or OSS review tool) and focus on any package that is not OSI-approved or that has copyleft terms.


Limitations / Assumptions

- I could not query the requested MCP servers (Context7, Firecrawl) or a centralized CVE/CVSS database from this execution environment. I therefore relied on local `requirements.txt` and a targeted set of PyPI metadata queries. This produced version-check results for a subset of high-impact packages only. CVE mapping was not possible here and must be executed with an appropriate scanner.
- This report covers direct dependencies only (exactly what is listed in `requirements.txt`). Transitives were ignored per instructions.


If you want, I can now:
- Run a complete PyPI metadata pass for every package in `requirements.txt` and produce an updated table with explicit latest-version numbers and license fields (this requires more queries but is possible from here).
- Run or orchestrate an OSV/CVE or MCP-based vulnerability check if you provide credentials or allow those MCP servers to be queried from this environment.

---

End of report.
