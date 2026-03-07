# CLAUDE.md

This file provides context and conventions for AI assistants (e.g., Claude Code) working in this repository.

---

## Repository Overview

- **Repository:** `zeluisao/stef`
- **Status:** Newly initialized — no source code committed yet
- **Branch convention:** Feature branches use the pattern `claude/<description>-<session-id>`

---

## Repository Structure

This repository is currently empty. Update this section as the project grows:

```
stef/
├── CLAUDE.md          # This file
└── (project files TBD)
```

---

## Development Workflow

### Branching

- Default/main branch: check `git remote show origin` for the upstream default
- AI-assisted work branches follow the pattern: `claude/<task>-<session-id>`
- Never force-push to `main` or `master`

### Making Changes

1. Work on the designated feature branch
2. Commit with clear, descriptive messages
3. Push with `git push -u origin <branch-name>`

### Commit Messages

Write commits in the imperative mood, describing _what_ the commit does and _why_:

```
Add user authentication module

Implements JWT-based auth to support the login/logout flow
described in issue #12.
```

---

## AI Assistant Conventions

### General Rules

- **Read before editing:** Always read a file fully before modifying it
- **Minimal changes:** Only change what is directly requested; avoid unrelated refactors
- **No speculative features:** Don't add error handling, logging, or abstractions for hypothetical future needs
- **Security first:** Never introduce command injection, SQL injection, XSS, or other OWASP Top 10 vulnerabilities
- **No secrets in code:** Never commit credentials, API keys, or `.env` files

### File Management

- Prefer editing existing files over creating new ones
- Do not create `*.md` documentation files unless explicitly asked
- Delete unused code entirely rather than commenting it out

### Code Style

*(Update this section once a language/framework is chosen)*

- Follow the conventions already present in the codebase
- Do not add docstrings, comments, or type annotations to code you didn't change
- Keep solutions simple — three similar lines is better than a premature abstraction

---

## Testing

*(Update once a test framework is set up)*

To run tests:
```bash
# placeholder — update when tests are configured
```

All changes should pass existing tests. Do not skip or delete tests to make a build pass.

---

## Build & Run

*(Update once a build system is configured)*

```bash
# placeholder — update when build steps are defined
```

---

## Environment & Configuration

*(Update once environment variables or config files are established)*

- Store secrets in `.env` (never commit this file)
- Add `.env` to `.gitignore`

---

## Dependencies

*(Update when dependencies are added)*

---

## Notes for Future Updates to This File

When the project gains real content, update this file to include:

1. **Actual directory structure** with descriptions of each major directory
2. **Language & framework** details and version requirements
3. **Lint/format commands** (`eslint`, `prettier`, `ruff`, etc.)
4. **Test commands** and how to run subsets of tests
5. **Build commands** and environment variable requirements
6. **Database setup** if applicable
7. **API conventions** (REST, GraphQL, etc.)
8. **Deployment process**
9. **Codebase-specific patterns** to follow or avoid
