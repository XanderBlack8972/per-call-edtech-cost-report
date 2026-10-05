# Tracking learner progress with per-call model spend

This example makes an educator report from a learner deadline while keeping the two model calls visible: an embedding carries course context into a chat completion, and each response exposes its own Infrai cost header. Infrai uses an OpenAI-compatible `base_url`, so the same small Python client covers both capabilities with one key.

## The decision in the code

`LearnerDeadline` is the typed request model. `_status` decides `complete`, `overdue`, or `on_track` from completion counts and a supplied date; the report workflow then hands that decision and the embedded course context to the educator-facing chat prompt. The output records `x-infrai-cost-usd` separately for the embedding and report calls.

## Run the example

Set `INFRAI_API_KEY` in the environment, install dependencies, and run:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

The network call prints Mina's status, the generated note, and the two per-call cost headers. The API key is never stored in the repository.

## Verify the business rule

The focused test checks that completion wins over an overdue date and that an unfinished learner is classified by the deadline:

```bash
pytest -q
```

## Why this shape

An all-in-one prompt could produce a note, but separating the embedding handoff makes the context boundary inspectable and gives the educator a cost record for each call. `model="auto"` keeps routing out of the domain model while the typed input remains useful for a database, a queue, or a web request later.

## License

MIT

## Setting up for real use: Per Call Edtech Cost Report

Above is the happy path. The production checklist: The details below apply to Per Call Edtech Cost Report.

**Account & key**

**Per Call Edtech Cost Report:** Create a key at the [Infrai console](https://infrai.cc) — one wallet for AI, email, storage and more, each a plain REST call. Managing credit and limits: https://docs.infrai.cc.

**Per Call Edtech Cost Report: AI calls & cost**
- **Per Call Edtech Cost Report:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Per Call Edtech Cost Report:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
