def clean_opportunities(jobs):
    cleaned = []
    seen = set()

    for job in jobs:
        title = job.get("title", "").strip()
        url = job.get("url", "").strip()

        if not title or not url:
            continue

        key = (title.lower(), url)
        if key in seen:
            continue

        seen.add(key)
        cleaned.append(job)

    return cleaned
