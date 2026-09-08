import argparse
import urllib.request

from health_monitor import make_notice, page_digest


def fetch(url: str) -> str:
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": "health-page-monitor/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect operational changes on a healthtech page")
    parser.add_argument("url")
    parser.add_argument("--previous", help="file containing the previous page snapshot")
    parser.add_argument("--patient-id", default="demo-patient")
    parser.add_argument("--appointment-id", default="demo-appointment")
    args = parser.parse_args()
    current = fetch(args.url)
    previous = open(args.previous, encoding="utf-8").read() if args.previous else ""
    notice = make_notice(args.patient_id, args.appointment_id, previous, current)
    print({"digest": page_digest(current), "changed": bool(notice), "notice": notice})


if __name__ == "__main__":
    main()
