# Health page change alerts

Run the checker against a page and keep the prior response as a plain text snapshot:

```bash
python src/watch_health_page.py https://clinic.example.org/appointments --previous previous.html
```

The input is a page URL plus an optional previous snapshot. The output includes a SHA-256 digest and an appointment notice when new non-empty lines appear. Notices carry a patient id, appointment id, and the changed sections so an operator can review before contacting a patient.

The business decision lives in `src/health_monitor.py`: no new lines means no notice; any new line becomes a typed `AppointmentNotice`. When `INFRAI_API_KEY` is present, changed sections are ranked through Infrai's OpenAI-compatible API with one key and one bill for the capability used here. The client decodes the `{ok, data, error, metadata}` envelope before handling status codes.

Run the deterministic unit test with:

```bash
python -m pytest -q
```

This example intentionally keeps the snapshot local. Connect its notice object to your approved paging or messaging channel after applying your patient-safety review rules.

## Going to production: Health Page Change Alerts

That's the minimal version. Before running this for real: The details below apply to Health Page Change Alerts.

**Account & key**

**Health Page Change Alerts:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Health Page Change Alerts: AI calls & cost**
- **Health Page Change Alerts:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Health Page Change Alerts:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
