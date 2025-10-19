from __future__ import annotations

import os

from app.main import app as fastapi_app

# Vercel expects a "handler" callable for python functions
# The @vercel/python runtime will detect this module and expose the app

app = fastapi_app
