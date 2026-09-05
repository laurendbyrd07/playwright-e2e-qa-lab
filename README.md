# playwright-e2e-qa-lab

![CI](https://github.com/laurendbyrd07/playwright-e2e-qa-lab/actions/workflows/ci.yml/badge.svg)

> Modern E2E automation in active development — Playwright (Python), realistic user workflows, cross-browser CI.
> Target application: [SauceDemo](https://www.saucedemo.com), a stable public e-commerce practice app with built-in failure personas.

---

## Honest Positioning

This lab represents **active skill-building in modern UI/E2E automation** — portfolio engineering, not production experience. It is intentionally more sophisticated than my foundational Selenium project ([TestMate](https://github.com/laurendbyrd07/TestMate)): same QA thinking, modern tooling.

## Why Playwright, Why SauceDemo

Playwright's design changes what a suite *is*: auto-waiting removes hand-rolled wait management, the storage-state pattern makes authentication reusable, traces make failures debuggable after the fact, and one CLI flag runs the same suite across three browser engines.

SauceDemo is chosen over a throwaway login demo because it has **real multi-step workflows** (browse → cart → checkout → confirmation), **stateful behavior** (cart badge, cart contents across pages), **financial calculations** worth verifying from first principles, and **built-in failure personas** — including a `problem_user` with visually broken pages — which let the suite demonstrate *failure detection*, not just happy paths.

## Architecture

```text
playwright-e2e-qa-lab/
├── conftest.py          # storage-state auth pattern (login once per session, reuse)
├── config.py            # environment-driven base URL
├── pages/               # page objects (locators + behavior, no test logic)
├── testdata/            # personas + expected catalog (data separated from logic)
├── tests/               # one file per workflow area
└── .github/workflows/   # lint + cross-browser matrix CI
```

### Decisions worth explaining in an interview

- **Storage-state authentication.** Login happens **once per session** (`conftest.py`); the cookie/localStorage state is saved and injected into a fresh context per test. Fast *and* isolated — cart contents can't leak between tests.
- **Auto-waiting as the wait strategy.** No explicit waits anywhere; Playwright's locator engine plus `expect()` polling is the strategy. (Contrast: TestMate manages waits explicitly, because Selenium requires it — knowing *why* they differ is the point of building both.)
- **Data-backed assertions.** Sorting tests assert the actual price/name *sequences* against the expected catalog — not just "the dropdown changed." The checkout test recalculates subtotal/tax/total from displayed line items with `Decimal` math.
- **Failure-detection test.** `problem_user` (a persona with broken images) is used to prove the visual check catches real failures — the same assertion that passes for the standard user fails here, by the target app's design.
- **Stable selectors.** `[data-test=...]` attributes exclusively — never generated CSS or text-matching where an attribute exists.
- **Test data separation.** Personas and the expected catalog live in `testdata/`, so app changes are one-file updates.

## Coverage

| Workflow | File | Highlights |
|----------|------|-----------|
| Authentication | `tests/test_login.py` | valid login; locked-out user; invalid credentials; logout kills the session (direct navigation to a protected page bounces to login) |
| Inventory | `tests/test_inventory.py` | catalog integrity (names + prices); 4 sort orders verified against expected data; image rendering check; known-defect detection via `problem_user` |
| Cart | `tests/test_cart.py` | badge counts, cart contents, removal updates badge, continue-shopping navigation |
| Checkout | `tests/test_checkout.py` | per-field form validation errors in sequence; full purchase flow with **first-principles order math** (line items → subtotal → tax → total) and confirmation |

## Running Locally

```bash
pip install -r requirements.txt
playwright install chromium           # or: chromium firefox webkit
pytest                                # default browser (chromium)
pytest --browser firefox              # cross-browser
pytest -m smoke                       # quick pass
pytest --headed                       # watch it run
pytest --tracing retain-on-failure    # traces saved for failed tests only
```

## CI

GitHub Actions runs on every push/PR: Ruff lint, then the full suite on a **chromium / firefox / webkit matrix**, with screenshots, video, and Playwright **traces** retained on failure and uploaded as artifacts. The badge above reflects real cross-browser executions.

## Debugging & Failure Evidence

- `pytest --tracing retain-on-failure` → open the trace: `playwright show-trace test-results/<test>/trace.zip` (DOM snapshots, network, screenshots — full post-mortem).
- `--screenshot only-on-failure` / `--video retain-on-failure` for quick visual evidence.
- `PWDEBUG=1 pytest -k <test>` for the Playwright Inspector (step-through).

## Limitations

- **Demo target.** SauceDemo is a stable practice app — checkout has no real payment rail, no quantity controls, and no real backend state.
- **No API-assisted setup.** SauceDemo exposes no public API, so data setup is UI-driven (deliberately simple: a fixture adds two known items). In a real environment, API-assisted state setup would be preferable.
- **`performance_glitch_user` documented but not exercised** — a latency persona is interesting, but CI wall-clock flakiness is not.
- **No visual-regression snapshots yet** (`toHaveScreenshot`); the image check here validates *load* correctness, not pixel rendering.
- **Serial execution.** No sharding/parallelization yet — the suite is small; that would be premature complexity.

## Future Improvements

1. Visual regression with `toHaveScreenshot()` per breakpoint.
2. API-assisted setup/teardown against a target with a real API.
3. A second target app to exercise environment-agnostic configuration.
4. Retry/quarantine policy for genuinely flaky external dependencies.

---

*Part of a QA portfolio progression: manual QA & API foundations → UI automation fundamentals (TestMate, Selenium) → **modern E2E automation (this lab, Playwright — active skill-building)** → API contract testing → AI system testing → risk-based quality engineering.*
