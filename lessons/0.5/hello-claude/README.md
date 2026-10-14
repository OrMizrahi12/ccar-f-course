# hello-claude

A small workbench for making your first calls to the Claude API from Python.

`first_call.py` sends one message to `claude-haiku-5-5` and prints the reply, the stop reason, the token counts, and the request ID.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your API key. Copy the example file, then paste your key after the `=`:

   ```bash
   cp .env.example .env
   ```

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

   Get a key from the [Anthropic Console](https://console.anthropic.com/). `.env` is in `.gitignore`, so it won't be committed.

## Run

```bash
python first_call.py
```

You should see a one-sentence answer about API keys, followed by the stop reason, token counts, and request ID.
