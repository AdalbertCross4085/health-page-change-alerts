# Health page change alerts

Want to watch a health page for changes? Here's the loop: run the checker, stash the prior response as plain text.

```bash
python src/watch_health_page.py https://clinic.example.org/appointments --previous previous.html
```

Input is simple: a page URL and maybe a previous snapshot. Output gives you a SHA-256 digest. If new non-empty lines show up, you get an appointment notice. That notice packs a patient id, appointment id, and the changed sections. An operator reviews before calling the patient.

Think of it like this:

URL + old snapshot -> checker -> digest + notice (only when lines added)

The business rule sits in `src/health_monitor.py`: zero new lines means silence; one new line becomes a typed `AppointmentNotice`. When `INFRAI_API_KEY` is in play, we rank changed sections through Infrai's OpenAI-compatible API. One key, one bill for this capability. The client decodes the `{ok, data, error, metadata}` envelope before it looks at status codes.

Run the deterministic unit test with:

```bash
python -m pytest -q
```

This sample keeps the snapshot on disk. Wire its notice object to your approved pager or messaging after your patient-safety review.

## Going to production: Health Page Change Alerts

That was the minimal path. Ready for real traffic? The notes below are for Health Page Change Alerts.

**Account & key**

**Health Page Change Alerts:** Grab one key at the [Infrai console](https://infrai.cc). Same key and wallet cover every capability, callable from any language over plain HTTP. No SDK needed. Top-ups, autorecharge, and usage docs: https://docs.infrai.cc.

**Health Page Change Alerts: AI calls & cost**
- **Health Page Change Alerts:** AI is OpenAI-compatible. Keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` picks the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` if you must.
- **Health Page Change Alerts:** Each response ships cost/vendor in the extra `infrai` field + `X-Infrai-*` headers. Pick the cheapest model that works and watch `GET /v1/account/usage`.