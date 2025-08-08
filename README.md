# Telegram VPN Bot

A Telegram bot that provides VPN service functionality, including:
- Multiple server locations (Russia, America, Germany, Singapore)
- VMess and VLESS link generation
- Account management
- Promo code system
- Referral system

## New Project Topology

To make the codebase easier to read and extend, the project is now structured into clear sections:

- app/
  - config.py — central configuration (env-based), paths, feature flags
  - data/ — data access and storage helpers (JSON/DB adapters)
  - handlers/ — bot command/message handlers
  - keyboards/ — inline and reply keyboard builders
  - services/ — core business logic (e.g., VPN link generation)
  - utils/ — general-purpose utilities
- main.py — legacy monolithic implementation (still works)
- run.py — entrypoint that calls main.main() without changing behavior
- Pipfile — pipenv environment
- requirements.txt — pinned dependencies (if used in CI)

This change introduces folders for each section while keeping the existing `main.py`
intact to avoid breaking changes. You can progressively move functions from `main.py`
into the appropriate modules under `app/`.

### Suggested Migration Plan

- Move user data functions into `app/data/` (e.g., `storage.py`).
- Move VPN link generation into `app/services/vpn_generator.py`.
- Move keyboard builders into `app/keyboards/` (split per keyboard).
- Move handlers into `app/handlers/` (split per command/feature).
- Centralize settings in `app/config.py` and import from there.

Refactor incrementally:
1. Copy a function from `main.py` to the right module.
2. Replace its usage in `main.py` with an import from the new module.
3. Test after each small change.

## Setup

### Prerequisites
- Python 3.12.3
- pipenv

### Installation

1. Clone the repository
2. Create and activate the environment:
   - pipenv install --dev
   - pipenv shell
3. Set environment variables as needed (e.g., `BOT_TOKEN`)
4. Run the bot:
   - pipenv run python run.py

## Notes

- `run.py` preserves current behavior by delegating to `main.main()`.
- New code should import configuration from `app/config.py`.
- Data files default to `var/users.json` (see `app/config.py`), but legacy `main.py` still uses its own settings until migrated.