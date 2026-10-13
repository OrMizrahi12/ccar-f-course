# Expected output: Lesson 0.4, your first call

What `python first_call.py` printed in the lesson, on Claude Haiku 5.5 (`claude-haiku-5-5`), with `anthropic==1.13.0`.

## Run 1: no key in `.env` yet

`.env` still had nothing after `ANTHROPIC_API_KEY=`. Python printed a traceback; its last line starts with:

```text
TypeError: "Could not resolve authentication method. Expected one of api_key, auth_token, or credentials to be set. ...
```

The SDK found no key, so it raised this error on your computer before sending anything. No request reached the API, and nothing was billed.

## Run 2: with the key in `.env`

```text
An API key is a unique string of characters that identifies and authenticates a program or user when accessing an application programming interface, letting the service know who is making a request and whether they're permitted to make it.
stop_reason: end_turn
tokens in: 18 out: 59
request id: req_…
```

How to read it:

| Line | What it means |
|---|---|
| The sentence | The text block of the reply. The script prints every block whose type is `text`. |
| `stop_reason: end_turn` | Claude finished its answer. (`max_tokens` here would mean the reply hit the cap.) |
| `tokens in: 18 out: 59` | The usage: 18 input tokens, 59 output tokens. |
| `request id: req_…` | The request's unique ID (the full value is longer). Keep it if you ever need to report a problem. |

**Cost of this call:** about $0.00003. Claude Haiku 5.5 costs $0.10 per million input tokens and $0.50 per million output tokens (prompts up to 100,000 tokens), so 18 × $0.10 / 1,000,000 + 59 × $0.50 / 1,000,000 = $0.0000313.

## What to compare with yours

Your sentence and your output token count will differ: Claude doesn't answer word for word the same way twice. Check the shape instead:

- one sentence of text, with no error;
- `stop_reason: end_turn`;
- a small number of input and output tokens;
- a request ID that starts with `req_`.
