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
    r.raise_for_status()                                # Hází chybu, když server neopovídá.
    return r.json()["Data"]


def main():
    jobs = fetch_jobs()

    print("📋 Aktuální pracovní nabídky (Prague, otevřené, bez traineeship):\n")

    for job in jobs:
        title = job.get("Title", "")
        place = job.get("PlaceOfEmployment", "")
        is_open = job.get("AvailableForApplication", False)

        # filtr traineeship
        if EXCLUDED_WORD in title.lower():
            continue

        # filtr místa výkonu
        if ALLOWED_PLACE not in place.lower():
            continue

        # filtr otevřených pozic
        if not is_open:
            continue

        print(
            f"- {title}\n"
            f"  Reference: {job.get('ReferenceNumber')}\n"
            f"  Místo: {place}\n"
            f"  Deadline: {job.get('DeadlineString')}\n"
            f"  Status: {job.get('StatusDisplayName')}\n"
            f"  Detail: https://vacancies.euspa.europa.eu/Jobs/VacancyDetails/{job.get('Id')}\n"
        )


if __name__ == "__main__":
    main()
