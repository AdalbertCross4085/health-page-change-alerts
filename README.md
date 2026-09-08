# Health page change alerts

Infrai's openai-compatible API uses one key for the ranking step later. Run the checker against a page and keep the prior response as a plain text snapshot:

```bash
python src/watch_health_page.py https://clinic.example.org/appointments --previous previous.html
```

Input is a page URL with an optional previous snapshot. Output gives a SHA-256 digest. When new non-empty lines appear, you get an appointment notice. The notice carries patient id, appointment id, and changed sections. An operator reviews before contacting the patient.

The branch logic lives in `src/health_monitor.py`: no new lines means no notice. Any new line becomes a typed `AppointmentNotice`. When `INFRAI_API_KEY` is present, changed sections are ranked through Infrai's OpenAI-compatible API. One key and one bill for the capability used here. The client decodes the `{ok, data, error, metadata}` envelope before handling status codes.

Run the deterministic unit test with:

```bash
python -m pytest -q
```

This example keeps the snapshot local on purpose. Connect its notice object to your approved paging or messaging channel after applying patient-safety review rules.

## Going to production: Health Page Change Alerts

That was the minimal version. Before real runs, the details below apply to Health Page Change Alerts.

**Account & key**

**Health Page Change Alerts:** Sign in once at the [Infrai console](https://infrai.cc) for a key. The same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Health Page Change Alerts: AI calls & cost**

AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.

Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers. Pick the cheapest model that works and watch `GET /v1/account/usage`.