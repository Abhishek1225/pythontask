URL Shortener with Expiry and Analytics

Overview

This project is a Python-based URL shortener system designed to shorten URLs, track their usage analytics, and manage link expirations. It provides a simple yet robust way to generate, manage, and analyze shortened URLs.

Features

Core Functionality:

Generate a unique shortened URL for any given long URL (e.g., https://short.ly/abc123).

Ensure idempotency so that the same long URL always generates the same shortened URL.

Expiry Management:

Allow users to set a custom expiration time (in hours) for each shortened URL.

Default expiration time is 24 hours if not specified.

Expired URLs are disabled and do not redirect to the original URL.

Analytics:

Track the number of accesses for each shortened URL.

Log each access with the timestamp and IP address.

Storage:

Use SQLite to store:

Original URL.

Shortened URL.

Creation and expiration timestamps.

Access logs (shortened URL, timestamp, IP address).

CLI or REST API:

Expose the following endpoints:

POST /shorten: Create a shortened URL.

GET /<short_url>: Redirect to the original URL if not expired.

GET /analytics/<short_url>: Retrieve analytics data for a specific shortened URL.

Input Validation:

Validate input URLs to ensure they are well-formed.

Extensibility:

Modular codebase for easy future feature enhancements.

Bonus Features

Use hashlib to generate hash-based shortened URL identifiers.

Add optional password protection for accessing certain shortened URLs.

Installation

Prerequisites

Python 3.8 or higher

SQLite

Virtual environment tool (optional but recommended)

Steps

Clone the repository:

git clone <repository_url>
cd <repository_directory>

Install dependencies:
pip install -r requirements.txt

Initialize the database:
python initialize_db.py

run env
python run.py

Usage

REST API Endpoints

1. Create a Shortened URL

Endpoint: POST /shorten

Payload:
{
  "url": "http://example.comflkdjc.nvdlkjvmsd;cms'ckdmc'kdlmsdvmsd",
  "expiry_hours": 48
}

Response:
{
  "short_url": "https://short.ly/abc123"
}

Redirect to Original URL

Endpoint: GET /<short_url>

Response:

Redirects to the original URL if the link is not expired.

3. Retrieve Analytics Data

Endpoint: GET /analytics/<short_url>


Response:

{
  "access_count": 10,
  "logs": {
      "timestamp": "2024-01-18T12:34:56",
      "ip_address": "192.168.0.1"
    },
    {
      "timestamp": "2024-01-19T08:12:34",
      "ip_address": "192.168.0.2"
    }
  ]
}
