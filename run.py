"""
Entrypoint script.

This keeps the existing behavior by calling main.main() so that:
- current workflows remain intact
- we can progressively migrate logic from main.py into app/* modules

Usage:
  pipenv run python run.py
"""

from __future__ import annotations

import asyncio
import logging


def _get_main_callable():
    try:
        # Import from the legacy monolithic file
        from main import main as legacy_main  # type: ignore
        return legacy_main
    except Exception as exc:  # pragma: no cover
        logging.exception("Failed to import main.main(): %s", exc)
        raise


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    main_callable = _get_main_callable()
    # Support both async def main() and def main()
    if asyncio.iscoroutinefunction(main_callable):
        asyncio.run(main_callable())
    else:
        main_callable()
