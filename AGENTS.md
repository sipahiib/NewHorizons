# Repository Guidelines

## Project Structure & Module Organization

This repository is currently a blank project scaffold. As code is introduced, keep the top level limited to configuration, documentation, and entry-point files. Place application code in `src/`, automated tests in `tests/`, and static resources such as images or fixtures in `assets/`. Mirror source paths in the test tree; for example, tests for `src/news/parser.*` should live under `tests/news/`. Store generated output in `dist/` or `build/` and exclude it from version control.

## Build, Test, and Development Commands

No build system or package manager has been configured yet. When adding one, expose a small, predictable command set and document it in `README.md`. Prefer conventional commands such as:

- `npm run dev` — start the local development environment.
- `npm run build` — create a production build.
- `npm test` — run the complete automated test suite.
- `npm run lint` — check formatting and static-analysis rules.

Do not commit dependencies or generated build artifacts. Update this section when the actual toolchain is selected.

## Coding Style & Naming Conventions

Follow the formatter and linter configured for the chosen language; checked-in configuration is authoritative. Until then, use spaces rather than tabs, UTF-8 text, and a final newline. Choose descriptive names: `camelCase` for variables and functions, `PascalCase` for classes or components, and `kebab-case` for filenames unless the framework requires otherwise. Keep modules focused and avoid unrelated refactors in feature changes.

## Testing Guidelines

Add tests with every bug fix and behavior change. Name tests after observable behavior, such as `parser-rejects-empty-title.test.*`. Keep unit tests deterministic and isolate network calls with fixtures or mocks. Contributors should run the full test and lint commands before opening a pull request. Once coverage tooling exists, document the expected threshold here.

## Commit & Pull Request Guidelines

Because this directory has no Git history, no repository-specific commit convention can be inferred. Use concise, imperative subjects such as `Add article parsing validation`, keeping each commit focused. Pull requests should explain the purpose and approach, list verification performed, and link related issues. Include screenshots or sample output for user-visible changes, and call out configuration changes or migration steps explicitly.

## Security & Configuration

Never commit credentials, API keys, or local environment files. Provide sanitized examples in `.env.example`, document required variables, and validate untrusted external content at system boundaries.
