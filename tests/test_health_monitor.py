from src.health_monitor import changed_sections, make_notice


def test_changed_appointment_sections_create_patient_safe_notice(monkeypatch):
    monkeypatch.delenv("INFRAI_API_KEY", raising=False)
    previous = "Clinic hours: 08:00-17:00\nBring photo ID"
    current = "Clinic hours: 09:00-17:00\nBring photo ID"
    assert changed_sections(previous, current) == ["Clinic hours: 09:00-17:00"]
    notice = make_notice("p-17", "a-42", previous, current)
    assert notice is not None
    assert notice.patient_id == "p-17"
    assert notice.changed_sections == ["Clinic hours: 09:00-17:00"]
