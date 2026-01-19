import requests

URL = "https://vacancies.euspa.europa.eu/Home/Index_Binding?showOnly=current"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

EXCLUDED_WORD = "traineeship"
ALLOWED_PLACE = "prague"


def fetch_jobs():
    r = requests.get(URL, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()["Data"]


def main():
    jobs = fetch_jobs()

    lines = []
    lines.append("# 📋 EUSPA – aktuální pracovní nabídky (Prague)\n")

    for job in jobs:
        title = job.get("Title", "")
        place = job.get("PlaceOfEmployment", "")
        is_open = job.get("AvailableForApplication", False)

        if EXCLUDED_WORD in title.lower():
            continue
        if ALLOWED_PLACE not in place.lower():
            continue
        if not is_open:
            continue

        lines.append(f"## {title}")
        lines.append(f"- **Reference:** {job.get('ReferenceNumber')}")
        lines.append(f"- **Místo:** {place}")
        lines.append(f"- **Deadline:** {job.get('DeadlineString')}")
        lines.append(f"- **Status:** {job.get('StatusDisplayName')}")
        lines.append(
            f"- **Detail:** https://vacancies.euspa.europa.eu/Jobs/VacancyDetails/{job.get('Id')}\n"
        )

    with open("jobs.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("jobs.md aktualizován.")


if __name__ == "__main__":
    main()
