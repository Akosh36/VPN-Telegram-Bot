"""
App package

This package hosts the modularized code for the Telegram VPN bot.
Sections are organized into subpackages:
- handlers: command and message handlers
- keyboards: inline and reply keyboard builders
- services: core business logic (e.g., VPN link generation)
- data: persistence and storage helpers
- utils: general-purpose utilities

Current release preserves the original main.py behavior while providing
a clear topology for incremental migration of code into modules.
"""
