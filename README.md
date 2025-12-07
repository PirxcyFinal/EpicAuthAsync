# EpicAuth-Async

[![PyPI version](https://badge.fury.io/py/EpicAuthAsync.svg)](https://badge.fury.io/py/EpicAuthAsync)
[![Python versions](https://img.shields.io/pypi/pyversions/EpicAuthAsync.svg)](https://pypi.org/project/EpicAuthAsync/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An asynchronous, lightweight Python library for interacting with Epic Games Store (EGS) and Epic Online Services (EOS) authentication endpoints.**

Originally built for personal use on a Discord Bot, this library has been open-sourced to help the community easily manage Epic Games sessions, OAuth tokens, and client data.
Thanks to Jaren for the Client API and LeleDerGrasshalmi for the documentation of all of this :)

---

## Features

-   **Fully Asynchronous:** Built on top of `aiohttp` for non-blocking performance.
-   **Client Management:** Automatically fetches and maps known Epic clients from `egs.jaren.wtf`.
-   **Comprehensive OAuth Support:** Handles multiple grant types including:
    -   `authorization_code`
    -   `client_credentials`
    -   `device_auth` / `device_code`
    -   `exchange_code`
    -   `password`
-   **Session Control:** Verify tokens, kill sessions, and inspect continuation tokens.
-   **Type Safe:** Includes full typing definitions and Pydantic models for responses (`TokenResponse`, `ExchangeCodeResponse`, etc.).

---

## Installation

Install directly from PyPI:

```bash
pip install EpicAuthAsync
```

## AI Prompt?

Checkout the AI Prompt [here](./AI_PROMPT.txt) :)
