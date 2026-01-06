# app/hunter.py

import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus, urljoin

from app.config import (
    JOB_BOARDS,
    PROFILE,
    PREFERENCES,
    RESEARCH_KEYWORDS,
    ADOPTION_KEYWORDS,
)

from app.storage import save_opportunity

# --------------------------------------------------
# HEADERS
# --------------------------------------------------

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "DNT": "1",
    "Connection": "keep-alive",
}

# --------------------------------------------------
# UTILITIES
# --------------------------------------------------

def random_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))


def detect_signals(description, keywords):
    found = []
    if not description:
        return found

    desc = description.lower()
    for k in keywords:
        if k.lower() in desc:
            found.append(k)
    return found


def fetch_job_description(url, source):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return ""

        soup = BeautifulSoup(r.text, "html.parser")

        # LinkedIn
        if source == "LinkedIn":
            block = soup.find("div", class_="show-more-less-html__markup")
            if block:
                return block.get_text(" ", strip=True)

        # Generic patterns
        for selector in [
            {"class": "job-description"},
            {"class": "description"},
            {"id": "job-description"},
            {"class": "jobsearch-jobDescriptionText"},
        ]:
            block = soup.find("div", selector)
            if block:
                return block.get_text(" ", strip=True)

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs[:10])
        return text if len(text) > 200 else ""

    except Exception as e:
        print(f"  ! Description fetch failed: {e}")
        return ""


def extract_requirements(description):
    req = []
    if not description:
        return req

    d = description.lower()

    skills = {
        "Python": ["python"],
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning"],
        "Computer Vision": ["computer vision", "cv"],
        "NLP": ["nlp", "natural language"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "OpenCV": ["opencv"],
        "Research": ["research"],
    }

    for name, keys in skills.items():
        if any(k in d for k in keys):
            req.append(name)

    if "paid" in d or "salary" in d or "compensation" in d:
        req.append("Paid internship")
    if "unpaid" in d:
        req.append("Unpaid internship")

    return req


# --------------------------------------------------
# LINKEDIN SEARCH
# --------------------------------------------------

def search_linkedin():
    print("[LinkedIn] Searching...")
    jobs = []

    if not JOB_BOARDS["linkedin"]["enabled"]:
        return jobs

    for query in JOB_BOARDS["linkedin"]["search_queries"]:
        params = {
            "keywords": query,
            "location": "Remote",
            "f_E": "2",
            "f_JT": "I",
        }

        url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/"
            "seeMoreJobPostings/search?"
            + "&".join(f"{k}={quote_plus(str(v))}" for k, v in params.items())
        )

        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            cards = soup.find_all("div", class_="base-card")

            for card in cards[:15]:
                title = card.find("h3", class_="base-search-card__title")
                company = card.find("h4", class_="base-search-card__subtitle")
                location = card.find("span", class_="job-search-card__location")
                link = card.find("a", class_="base-card__full-link")

                if not title or not link:
                    continue

                url = link["href"]
                print(f"  > {title.text.strip()[:60]}")

                description = fetch_job_description(url, "LinkedIn")

                job = {
                    "title": title.text.strip(),
                    "company": company.text.strip() if company else "Unknown",
                    "location": location.text.strip() if location else "Remote",
                    "url": url,
                    "source": "LinkedIn",
                    "description": description,
                    "requirements": extract_requirements(description),

                    # 🔬 SIGNALS
                    "research_signals": detect_signals(description, RESEARCH_KEYWORDS),
                    "adoption_signals": detect_signals(description, ADOPTION_KEYWORDS),
                }

                jobs.append(job)
                random_delay(1, 3)

            random_delay()

        except Exception as e:
            print(f"  x LinkedIn error: {e}")

    print(f"[LinkedIn] {len(jobs)} jobs")
    return jobs


# --------------------------------------------------
# RESEARCH & ADOPTION SITES
# --------------------------------------------------

def search_research_sites():
    print("[Research / Adoption] Searching...")
    jobs = []

    SOURCES = [
        {
            "name": "ResearchGate",
            "url": "https://www.researchgate.net/jobs",
            "queries": ["AI intern", "machine learning research"],
        },
        {
            "name": "OpenAI Careers",
            "url": "https://openai.com/careers",
            "queries": ["research", "intern"],
        },
        {
            "name": "HuggingFace Jobs",
            "url": "https://apply.workable.com/huggingface/",
            "queries": ["research", "intern"],
        },
        {
            "name": "Google Research",
            "url": "https://research.google/careers/",
            "queries": ["intern", "research"],
        },
    ]

    for src in SOURCES:
        for q in src["queries"]:
            try:
                url = f"{src['url']}?q={quote_plus(q)}"
                r = requests.get(url, headers=HEADERS, timeout=10)
                if r.status_code != 200:
                    continue

                soup = BeautifulSoup(r.text, "html.parser")
                links = soup.find_all("a", href=True)

                for a in links:
                    text = a.get_text(strip=True)
                    href = a["href"]

                    if len(text) < 20:
                        continue
                    if not any(k in text.lower() for k in ["intern", "research", "fellow"]):
                        continue

                    job = {
                        "title": text[:200],
                        "company": src["name"],
                        "location": "Remote / Research",
                        "url": href if href.startswith("http") else urljoin(src["url"], href),
                        "source": src["name"],
                        "description": "",
                        "requirements": ["Research environment"],
                        "research_signals": ["research"],
                        "adoption_signals": [],
                    }

                    jobs.append(job)
                    print(f"  > {text[:60]}")

                random_delay()

            except Exception as e:
                print(f"  x {src['name']} error: {e}")

    print(f"[Research / Adoption] {len(jobs)} jobs")
    return jobs


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def search_all():
    print("\n" + "=" * 60)
    print("JOB HUNTER – SEARCH START")
    print("=" * 60)

    all_jobs = []
    all_jobs.extend(search_linkedin())
    all_jobs.extend(search_research_sites())

    seen = set()
    unique = []

    for job in all_jobs:
        if job["url"] not in seen:
            seen.add(job["url"])
            unique.append(job)
            save_opportunity(job)

    print("=" * 60)
    print(f"SEARCH COMPLETE — {len(unique)} unique opportunities")
    print("=" * 60)

    return unique


def process_all_opportunities(self):
    """Process all found opportunities through the pipeline"""
    
    # Auto-clean refused opportunities before processing
    from app.storage import remove_refused_from_found
    remove_refused_from_found()
    
    # Rest of the code stays the same...
    jobs = load_found()
    
    if not jobs:
        print("\n[Info] No opportunities to process")
        print("[Action] Run search first (option 1 or 2)")
        return
    
    # ... rest of the method ...


if __name__ == "__main__":
    search_all()
