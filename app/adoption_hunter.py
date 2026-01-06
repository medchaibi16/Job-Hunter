# app/adoption_hunter.py
# Specialized hunter for finding AI adoption/innovation program internships
# Searches for companies, platforms, and research institutions that specifically
# accept student AI project ideas and prototypes

import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus, urljoin

from app.config import PROFILE

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

def random_delay(min_sec=1, max_sec=3):
    """Random delay to avoid detection"""
    time.sleep(random.uniform(min_sec, max_sec))


def fetch_url(url, timeout=15):
    """Safely fetch a URL and return BeautifulSoup object"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        return None
    except Exception as e:
        print(f"  ! Fetch failed for {url[:50]}: {e}")
        return None


# --------------------------------------------------
# AI STARTUP ACCELERATORS & INCUBATORS
# --------------------------------------------------

def search_startup_accelerators():
    """Search for AI startup accelerators that accept interns"""
    print("[Adoption] Searching AI Startup Accelerators...")
    jobs = []

    ACCELERATORS = [
        {
            "name": "Y Combinator",
            "url": "https://www.ycombinator.com/companies",
            "description": "Startup accelerator with many AI companies hiring interns",
            "search_terms": ["AI", "machine learning", "computer vision"]
        },
        {
            "name": "Plug and Play Tech Center",
            "url": "https://www.plugandplaytechcenter.com/",
            "description": "AI/ML focused accelerator",
            "search_terms": ["AI", "innovation"]
        },
        {
            "name": "Techstars",
            "url": "https://www.techstars.com/",
            "description": "Global accelerator for tech companies",
            "search_terms": ["AI", "machine learning"]
        },
        {
            "name": "500 Global",
            "url": "https://500.co/",
            "description": "Venture capital and accelerator",
            "search_terms": ["AI", "startups"]
        },
        {
            "name": "Anterra Capital",
            "url": "https://www.anterracapital.com/",
            "description": "Invests in AI/ML startups",
            "search_terms": ["AI", "machine learning"]
        },
    ]

    for accel in ACCELERATORS:
        try:
            print(f"  → {accel['name']}")
            soup = fetch_url(accel["url"])
            if not soup:
                continue

            # Extract company listings
            links = soup.find_all("a", href=True)
            job_count = 0

            for link in links:
                text = link.get_text(strip=True)
                href = link.get("href", "")

                if not href.startswith("http"):
                    href = urljoin(accel["url"], href)

                # Filter for career/job related links
                if any(word in text.lower() for word in ["career", "job", "intern", "work", "team"]):
                    if len(text) > 5 and len(text) < 200:
                        job = {
                            "title": f"Internship - {accel['name']}",
                            "company": text[:100] if len(text) > 3 else accel["name"],
                            "location": "Remote / Global",
                            "url": href,
                            "source": f"Accelerator: {accel['name']}",
                            "description": accel["description"],
                            "requirements": ["Startup environment", "Innovation focus"],
                            "research_signals": ["startup", "innovation"],
                            "adoption_signals": ["accelerator", "innovation", "startup"],
                        }
                        jobs.append(job)
                        job_count += 1
                        print(f"    ✓ Found: {text[:60]}")

            if job_count == 0:
                # Fallback: create general accelerator job posting
                job = {
                    "title": f"{accel['name']} - AI Internship Programs",
                    "company": accel["name"],
                    "location": "Remote / Global",
                    "url": accel["url"],
                    "source": f"Accelerator: {accel['name']}",
                    "description": accel["description"],
                    "requirements": ["Startup experience", "Innovation mindset"],
                    "research_signals": ["startup", "innovation"],
                    "adoption_signals": ["accelerator", "startup"],
                }
                jobs.append(job)

            random_delay()

        except Exception as e:
            print(f"  x {accel['name']} error: {e}")

    print(f"  [Accelerators] Found {len(jobs)} opportunities\n")
    return jobs


# --------------------------------------------------
# INNOVATION CHALLENGES & HACKATHONS
# --------------------------------------------------

def search_innovation_platforms():
    """Search for innovation challenges and hackathon platforms"""
    print("[Adoption] Searching Innovation Platforms...")
    jobs = []

    PLATFORMS = [
        {
            "name": "Devpost",
            "url": "https://devpost.com/challenges",
            "description": "Hackathons and coding challenges with prizes",
        },
        {
            "name": "IdeaScale",
            "url": "https://www.ideascale.com/",
            "description": "Innovation platform for idea submissions",
        },
        {
            "name": "ChallengePost",
            "url": "https://www.challengepost.com/",
            "description": "Technology challenges and competitions",
        },
        {
            "name": "HackerEarth",
            "url": "https://www.hackerearth.com/challenges/",
            "description": "Coding challenges and hackathons",
        },
        {
            "name": "MLH - Major League Hacking",
            "url": "https://mlh.io/",
            "description": "Official independent hackathon league",
        },
        {
            "name": "GitHub Sponsors",
            "url": "https://github.com/sponsors",
            "description": "Fund open source projects and innovations",
        },
    ]

    for platform in PLATFORMS:
        try:
            print(f"  → {platform['name']}")
            soup = fetch_url(platform["url"])
            if not soup:
                continue

            # Extract challenges/competitions
            links = soup.find_all("a", href=True)
            challenge_count = 0

            for link in links:
                text = link.get_text(strip=True)
                href = link.get("href", "")

                if not href.startswith("http"):
                    href = urljoin(platform["url"], href)

                # Filter for challenge/hackathon keywords
                if any(word in text.lower() for word in ["challenge", "hackathon", "competition", "contest", "innovation"]):
                    if 10 < len(text) < 150:
                        job = {
                            "title": text[:120],
                            "company": platform["name"],
                            "location": "Remote / Online",
                            "url": href,
                            "source": f"Platform: {platform['name']}",
                            "description": platform["description"],
                            "requirements": ["Project submission", "Innovation"],
                            "research_signals": ["innovation"],
                            "adoption_signals": ["hackathon", "challenge", "innovation"],
                        }
                        jobs.append(job)
                        challenge_count += 1
                        print(f"    ✓ Found: {text[:60]}")

            if challenge_count == 0:
                # Fallback
                job = {
                    "title": f"{platform['name']} - Innovation Challenges",
                    "company": platform["name"],
                    "location": "Remote / Online",
                    "url": platform["url"],
                    "source": f"Platform: {platform['name']}",
                    "description": platform["description"],
                    "requirements": ["Project ideas", "Innovation"],
                    "research_signals": ["innovation"],
                    "adoption_signals": ["hackathon", "challenge"],
                }
                jobs.append(job)

            random_delay()

        except Exception as e:
            print(f"  x {platform['name']} error: {e}")

    print(f"  [Platforms] Found {len(jobs)} opportunities\n")
    return jobs


# --------------------------------------------------
# RESEARCH & GRANT PROGRAMS
# --------------------------------------------------

def search_research_grants():
    """Search for AI research grant and funding programs"""
    print("[Adoption] Searching Research Grants & Funding...")
    jobs = []

    GRANT_SOURCES = [
        {
            "name": "NSERC - Natural Sciences and Engineering Research Council",
            "url": "https://www.nserc-crsng.gc.ca/students-etudiants/undergrad-premier-cycle/program-programme_eng.asp",
            "description": "Canadian research funding with student programs",
        },
        {
            "name": "NSF - National Science Foundation",
            "url": "https://www.nsf.gov/funding/",
            "description": "US research funding with REU programs for students",
        },
        {
            "name": "Erasmus+ Internships",
            "url": "https://erasmusplus.ec.europa.eu/",
            "description": "European internship and mobility program (Tunisia eligible!)",
        },
        {
            "name": "Google Research Internships",
            "url": "https://research.google/careers/",
            "description": "Google's research internship program",
        },
        {
            "name": "Meta AI Research",
            "url": "https://www.metacareers.com/jobs/?q=research&department[0]=Research%20%26%20Development",
            "description": "Meta's AI research internships",
        },
        {
            "name": "DeepMind",
            "url": "https://www.deepmind.com/careers",
            "description": "AI research organization with internship programs",
        },
        {
            "name": "OpenAI",
            "url": "https://openai.com/careers/",
            "description": "AI research and deployment organization",
        },
        {
            "name": "OpenIstanbul Fund",
            "url": "https://openistanbul.com/",
            "description": "Fund for tech innovation in Middle East/North Africa",
        },
    ]

    for source in GRANT_SOURCES:
        try:
            print(f"  → {source['name']}")
            soup = fetch_url(source["url"])
            if not soup:
                continue

            # Look for internship/research positions
            text_content = soup.get_text().lower()
            
            if any(word in text_content for word in ["intern", "research", "program", "opportunity", "apply"]):
                # Try to extract job links
                links = soup.find_all("a", href=True)
                found_count = 0

                for link in links:
                    link_text = link.get_text(strip=True)
                    href = link.get("href", "")

                    if not href.startswith("http"):
                        href = urljoin(source["url"], href)

                    if any(word in link_text.lower() for word in ["intern", "researcher", "research", "apply", "join"]):
                        if 5 < len(link_text) < 150:
                            job = {
                                "title": link_text[:120],
                                "company": source["name"],
                                "location": "Remote / Global",
                                "url": href,
                                "source": f"Research: {source['name']}",
                                "description": source["description"],
                                "requirements": ["Research background", "Academic focus"],
                                "research_signals": ["research", "funding"],
                                "adoption_signals": ["research", "internship"],
                            }
                            jobs.append(job)
                            found_count += 1
                            print(f"    ✓ Found: {link_text[:60]}")

                if found_count == 0:
                    # Fallback for main organization
                    job = {
                        "title": f"{source['name']} - Research Internship",
                        "company": source["name"],
                        "location": "Remote / Global",
                        "url": source["url"],
                        "source": f"Research: {source['name']}",
                        "description": source["description"],
                        "requirements": ["Research interest", "Academic background"],
                        "research_signals": ["research", "funded"],
                        "adoption_signals": ["research"],
                    }
                    jobs.append(job)

            random_delay()

        except Exception as e:
            print(f"  x {source['name']} error: {e}")

    print(f"  [Grants] Found {len(jobs)} opportunities\n")
    return jobs


# --------------------------------------------------
# OPEN SOURCE & GITHUB PROGRAMS
# --------------------------------------------------

def search_open_source_programs():
    """Search for open source contribution programs"""
    print("[Adoption] Searching Open Source Programs...")
    jobs = []

    PROGRAMS = [
        {
            "name": "Google Summer of Code",
            "url": "https://summerofcode.withgoogle.com/",
            "description": "Google's paid summer program for students contributing to open source",
        },
        {
            "name": "Outreachy",
            "url": "https://www.outreachy.org/",
            "description": "Paid internship program for underrepresented groups in tech",
        },
        {
            "name": "Linux Foundation Internships",
            "url": "https://www.linuxfoundation.org/about/careers/",
            "description": "Internships with open source projects",
        },
        {
            "name": "Mozilla Career Development Program",
            "url": "https://careers.mozilla.org/",
            "description": "Mozilla's internship and development programs",
        },
        {
            "name": "Apache Software Foundation",
            "url": "https://www.apache.org/",
            "description": "Community-driven open source projects with contribution programs",
        },
        {
            "name": "TensorFlow Community",
            "url": "https://www.tensorflow.org/community",
            "description": "Contribution opportunities for TensorFlow projects",
        },
        {
            "name": "PyTorch Fellowship Program",
            "url": "https://pytorch.org/",
            "description": "PyTorch project contribution and fellowship opportunities",
        },
    ]

    for program in PROGRAMS:
        try:
            print(f"  → {program['name']}")
            soup = fetch_url(program["url"])
            if not soup:
                continue

            # Extract opportunities
            links = soup.find_all("a", href=True)
            opp_count = 0

            for link in links:
                text = link.get_text(strip=True)
                href = link.get("href", "")

                if not href.startswith("http"):
                    href = urljoin(program["url"], href)

                if any(word in text.lower() for word in ["intern", "fellow", "apply", "join", "participate", "contribute"]):
                    if 5 < len(text) < 150:
                        job = {
                            "title": text[:120],
                            "company": program["name"],
                            "location": "Remote / Global",
                            "url": href,
                            "source": f"Open Source: {program['name']}",
                            "description": program["description"],
                            "requirements": ["Open source contribution", "Community participation"],
                            "research_signals": ["open source"],
                            "adoption_signals": ["open source", "community", "contribution"],
                        }
                        jobs.append(job)
                        opp_count += 1
                        print(f"    ✓ Found: {text[:60]}")

            if opp_count == 0:
                job = {
                    "title": f"{program['name']} - Open Source Contribution",
                    "company": program["name"],
                    "location": "Remote / Global",
                    "url": program["url"],
                    "source": f"Open Source: {program['name']}",
                    "description": program["description"],
                    "requirements": ["Open source experience", "Community driven"],
                    "research_signals": ["open source"],
                    "adoption_signals": ["open source", "contribution"],
                }
                jobs.append(job)

            random_delay()

        except Exception as e:
            print(f"  x {program['name']} error: {e}")

    print(f"  [Open Source] Found {len(jobs)} opportunities\n")
    return jobs


# --------------------------------------------------
# AI COMPANY INNOVATION LABS
# --------------------------------------------------

def search_innovation_labs():
    """Search for AI company innovation labs and research centers"""
    print("[Adoption] Searching AI Innovation Labs...")
    jobs = []

    LABS = [
        {
            "name": "MIT-IBM AI Lab",
            "url": "https://mitibmwatsonailab.mit.edu/",
            "description": "Collaborative AI research and internship opportunities",
        },
        {
            "name": "Stanford AI Index",
            "url": "https://aiindex.stanford.edu/",
            "description": "AI research and internship programs",
        },
        {
            "name": "Carnegie Mellon School of Computer Science",
            "url": "https://www.cs.cmu.edu/",
            "description": "Leading CS research with internship programs",
        },
        {
            "name": "UC Berkeley AI Research Lab",
            "url": "https://ai.berkeley.edu/",
            "description": "Cutting-edge AI research opportunities",
        },
        {
            "name": "Oxford Brookes University Computing Lab",
            "url": "https://www.brookes.ac.uk/",
            "description": "UK-based AI research and internships",
        },
        {
            "name": "Alan Turing Institute",
            "url": "https://www.turing.ac.uk/",
            "description": "UK national institute for data science and AI",
        },
    ]

    for lab in LABS:
        try:
            print(f"  → {lab['name']}")
            soup = fetch_url(lab["url"])
            if not soup:
                continue

            # Look for research/internship sections
            links = soup.find_all("a", href=True)
            lab_count = 0

            for link in links:
                text = link.get_text(strip=True)
                href = link.get("href", "")

                if not href.startswith("http"):
                    href = urljoin(lab["url"], href)

                if any(word in text.lower() for word in ["research", "internship", "career", "opportunity", "intern", "apply"]):
                    if 5 < len(text) < 150:
                        job = {
                            "title": text[:120],
                            "company": lab["name"],
                            "location": "Remote / International",
                            "url": href,
                            "source": f"Lab: {lab['name']}",
                            "description": lab["description"],
                            "requirements": ["Research interest", "Academic excellence"],
                            "research_signals": ["research", "lab", "innovation"],
                            "adoption_signals": ["research", "lab"],
                        }
                        jobs.append(job)
                        lab_count += 1
                        print(f"    ✓ Found: {text[:60]}")

            if lab_count == 0:
                job = {
                    "title": f"{lab['name']} - Research Internship",
                    "company": lab["name"],
                    "location": "Remote / International",
                    "url": lab["url"],
                    "source": f"Lab: {lab['name']}",
                    "description": lab["description"],
                    "requirements": ["Research background", "Innovation mindset"],
                    "research_signals": ["research", "lab"],
                    "adoption_signals": ["research"],
                }
                jobs.append(job)

            random_delay()

        except Exception as e:
            print(f"  x {lab['name']} error: {e}")

    print(f"  [Labs] Found {len(jobs)} opportunities\n")
    return jobs


# --------------------------------------------------
# MAIN SEARCH FUNCTION
# --------------------------------------------------

def search_adoption_opportunities():
    """
    Main function that searches all adoption/innovation sources
    Returns list of opportunities focused on AI project adoption
    """
    print("\n" + "=" * 70)
    print(" ADOPTION HUNTER - AI PROJECT ADOPTION INTERNSHIPS")
    print("=" * 70)
    print("\nSearching for companies, platforms, and institutions that accept")
    print("student AI project ideas and prototypes...\n")

    all_opportunities = []

    # Search all sources
    all_opportunities.extend(search_startup_accelerators())
    all_opportunities.extend(search_innovation_platforms())
    all_opportunities.extend(search_research_grants())
    all_opportunities.extend(search_open_source_programs())
    all_opportunities.extend(search_innovation_labs())

    print("=" * 70)
    print(f" ADOPTION SEARCH COMPLETE - {len(all_opportunities)} opportunities found")
    print("=" * 70 + "\n")

    return all_opportunities


if __name__ == "__main__":
    opportunities = search_adoption_opportunities()
    print("\nOpportunities found:")
    for opp in opportunities[:10]:
        print(f"  - {opp['title'][:60]} ({opp['source']})")