# web/app.py - FULLY FIXED VERSION

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from app.storage import (
    load_found, add_refused, add_approved, 
    update_found, get_stats, load_approved,
    remove_refused_from_found, clean_all_duplicates
)
from app.matcher import analyze_job, categorize_jobs
from app.simple_company_researcher import SimpleCompanyResearcher
from app.simple_email_rewriter import SimpleEmailRewriter
from config.env_loader import FLASK_SECRET_KEY, FLASK_DEBUG

app = Flask(__name__)

# Config from .env
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = FLASK_SECRET_KEY

# Initialize AI services
company_researcher = SimpleCompanyResearcher()
email_rewriter = SimpleEmailRewriter()


@app.route("/")
def index():
    """Main dashboard - Shows ALL jobs from ALL pipelines"""
    # Auto-clean refused opportunities on page load
    remove_refused_from_found()
    
    jobs = load_found()
    
    # Enrich all jobs with analysis
    enriched = []
    for job in jobs:
        # Make sure every job has a fingerprint
        if "fingerprint" not in job:
            from app.storage import job_fingerprint
            job["fingerprint"] = job_fingerprint(job)
        
        # Add analysis if missing
        if "analysis" not in job:
            job["analysis"] = analyze_job(job)
        
        enriched.append(job)
    
    # Categorize jobs
    categories = categorize_jobs(enriched)
    
    emotion_ai_jobs = categories["emotion_ai"]
    research_jobs = categories["research"]
    adoption_jobs = categories["adoption"]
    general_ai_jobs = categories.get("general_ai", [])  # Add general AI category
    
    stats = get_stats()
    
    # Calculate total (all categories)
    total_opportunities = len(emotion_ai_jobs) + len(research_jobs) + len(adoption_jobs) + len(general_ai_jobs)
    
    return render_template(
        "index.html",
        emotion_ai_jobs=emotion_ai_jobs,
        research_jobs=research_jobs,
        adoption_jobs=adoption_jobs,
        general_ai_jobs=general_ai_jobs,
        emotion_ai_count=len(emotion_ai_jobs),
        research_count=len(research_jobs),
        adoption_count=len(adoption_jobs),
        general_ai_count=len(general_ai_jobs),
        total_opportunities=total_opportunities,
        stats=stats
    )


@app.route("/refuse/<fingerprint>")
def refuse(fingerprint):
    """Refuse a job by fingerprint"""
    jobs = load_found()
    
    # Find job by fingerprint
    job_to_refuse = None
    job_index = None
    
    for i, job in enumerate(jobs):
        if job.get('fingerprint') == fingerprint:
            job_to_refuse = job
            job_index = i
            break
    
    if job_to_refuse:
        # Add to refused list
        add_refused(job_to_refuse)
        
        # Remove from found list
        jobs.pop(job_index)
        update_found(jobs)
        
        print(f"✅ Refused: {job_to_refuse.get('company')} - {job_to_refuse.get('title')}")
    else:
        print(f"❌ Job not found with fingerprint: {fingerprint}")
    
    return redirect(url_for("index"))


@app.route("/approve/<fingerprint>")
def approve(fingerprint):
    """Approve a job by fingerprint"""
    jobs = load_found()
    
    # Find job by fingerprint
    approved_job = None
    for job in jobs:
        if job.get('fingerprint') == fingerprint:
            approved_job = job
            break
    
    if approved_job:
        add_approved(approved_job)
        
        return redirect(url_for("write_email", fingerprint=fingerprint))
    else:
        flash("❌ Job not found", "error")
        return redirect(url_for("index"))


@app.route("/write_email/<fingerprint>")
def write_email(fingerprint):
    """Show email writing page"""
    jobs = load_found()
    
    # Find job by fingerprint
    job = None
    for j in jobs:
        if j.get('fingerprint') == fingerprint:
            job = j
            break
    
    if job:
        return render_template(
            "email_preview.html",
            job=job,
            fingerprint=fingerprint
        )
    else:
        flash("❌ Job not found", "error")
        return redirect(url_for("index"))


@app.route("/research_company/<fingerprint>")
def research_company(fingerprint):
    """Research company (AJAX)"""
    jobs = load_found()
    
    # Find job by fingerprint
    job = None
    for j in jobs:
        if j.get('fingerprint') == fingerprint:
            job = j
            break
    
    if job:
        result = company_researcher.research_company(
            company_name=job.get('company', 'Unknown'),
            job_title=job.get('title', 'Unknown Position'),
            job_url=job.get('url', '')
        )
        
        return jsonify(result)
    else:
        return jsonify({
            "success": False,
            "research": "Job not found"
        })


@app.route("/enhance_email", methods=["POST"])
def enhance_email():
    """Enhance email (AJAX)"""
    data = request.get_json()
    email_text = data.get('email_text', '')
    
    if not email_text:
        return jsonify({
            "success": False,
            "message": "No email text provided"
        })
    
    result = email_rewriter.enhance_email(email_text)
    return jsonify(result)


@app.route("/approved")
def approved():
    """View approved jobs"""
    approved_jobs = load_approved()
    return render_template("approved.html", jobs=approved_jobs)


@app.route("/stats")
def stats():
    """Show statistics"""
    statistics = get_stats()
    return render_template("stats.html", stats=statistics)


@app.route("/clear_all", methods=["POST"])
def clear_all():
    """Clear all opportunities"""
    from app.storage import clear_found
    clear_found()
    flash("✅ All opportunities cleared!", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    Path("web/templates").mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*60)
    print("  🚀 JOB HUNTER WEB DASHBOARD")
    print("="*60)
    print("\n📊 Starting Flask server...")
    print("🌐 URL: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop\n")
    
    app.run(debug=FLASK_DEBUG, host="0.0.0.0", port=5000)