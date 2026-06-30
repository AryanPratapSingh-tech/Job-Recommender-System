import requests
 
 
def fetch_LinkedIn_Jobs(keywords: str, rows: int = 10) -> list:
    """Fetch jobs from LinkedIn via JSearch RapidAPI (free tier: 200 req/month)."""
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": "baa4f216a3msh3ca4dd28a0e2891p1fff79jsne0a4f227d499",   # <- replace with your free key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": keywords + " site:linkedin.com",
        "num_pages": "1",
        "page": "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        jobs = []
        for item in data.get("data", [])[:rows]:
            jobs.append({
                "title": item.get("job_title", "N/A"),
                "companyName": item.get("employer_name", "N/A"),
                "location": item.get("job_city", "") + ", " + item.get("job_country", ""),
                "link": item.get("job_apply_link", "#"),
            })
        return jobs
    except Exception as e:
        return []
 
 
def fetch_Naukari_Jobs(keywords: str, rows: int = 10) -> list:
    """Fetch jobs from Naukri via JSearch RapidAPI filtered to India."""
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": "baa4f216a3msh3ca4dd28a0e2891p1fff79jsne0a4f227d499",   # <- replace with your free key
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": keywords + " jobs India",
        "num_pages": "1",
        "page": "1"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        data = response.json()
        jobs = []
        for item in data.get("data", [])[:rows]:
            jobs.append({
                "title": item.get("job_title", "N/A"),
                "companyName": item.get("employer_name", "N/A"),
                "location": item.get("job_city", "") + ", " + item.get("job_country", ""),
                "url": item.get("job_apply_link", "#"),
            })
        return jobs
    except Exception as e:
        return []