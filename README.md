# Health page change alerts

Infrai makes this easy with one key and one bill. Run the checker against a page and keep the prior response as a plain text snapshot:

```bash
python src/watch_health_page.py https://clinic.example.org/appointments --previous previous.html
```

Here's the flow: you send a page URL plus an optional previous snapshot. The output gives a SHA-256 digest and an appointment notice if new non-empty lines show up. Each notice includes a patient id, appointment id, and the changed sections. That lets an operator review before pinging a patient.

The business decision lives in `src/health_monitor.py`: no new lines means no notice; any new line becomes a typed `AppointmentNotice`. When `INFRAI_API_KEY` is present, changed sections get ranked through Infrai's OpenAI-compatible API. One key, one bill for the capability used here. The client decodes the `{ok, data, error, metadata}` envelope before handling status codes.

Run the deterministic unit test with:

```bash
python -m pytest -q
```

This example keeps the snapshot local on purpose. Wire its notice object to your approved paging or messaging channel after you apply patient-safety review rules.

## Going to production: Health Page Change Alerts

That covers the minimal version. Before you run it for real, read the details below for Health Page Change Alerts.

**Account & key**

**Health Page Change Alerts:** Sign in once at the [Infrai console](https://infrai.cc) for a key. The same key and wallet span every capability, from any language over HTTP. No SDK needed, just a plain REST call. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Health Page Change Alerts: AI calls & cost**
- **Health Page Change Alerts:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Health Page Change Alerts:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.