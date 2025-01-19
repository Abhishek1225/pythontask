from flask import Flask, request, jsonify, redirect

# from utils import *
import datetime,time
from app.db import *

import hashlib

app = Flask(__name__)

BASE_URL = 'https://short.ly/'

def generate_short_url(original_url):
    """
    Generates a short URL by hashing the original URL
    and returning the first 6 characters of the hash,
    prepended with the base URL.

    Args:
        original_url (str): The original long URL.

    Returns:
        str: A unique short URL string with base URL.
    """
    hash_object = hashlib.md5(original_url.encode())
    short_hash = hash_object.hexdigest()[:6]
    
    short_url = BASE_URL + short_hash
    return short_url
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    expiry = data.get('expiry', 24)  
    short_url = generate_short_url(original_url)
    print(f"Generated short_url: {short_url}")

    # Calculate expiration time
    expires_at = (datetime.datetime.now() + datetime.timedelta(hours=expiry)).strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO urls (original_url, short_url, expiration_time) VALUES (?, ?, ?)",
            (original_url, short_url, expires_at)
        )
        conn.commit()
        print(f"Inserted into database: short_url={short_url}, original_url={original_url}, expiration_time={expires_at}")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'short_url': short_url})


@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    conn = get_db_connection()
    try:
        short_url = request.view_args['short_url']
        row = conn.execute("SELECT original_url, expiration_time FROM urls WHERE short_url = ?", (short_url,)).fetchone()

        if row is None:
            return "URL not found", 404

        row_dict = dict(row)
        print(f"Row as dictionary: {row_dict}")  

        original_url = row_dict.get('original_url')
        expiration_time = row_dict.get('expiration_time')

        if not original_url:
            return "Original URL not found", 404

        print(f"Original URL: {original_url}")
        print(f"Expiration time: {expiration_time}")

        try:
            expiration_timestamp = time.mktime(time.strptime(expiration_time, '%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:
            expiration_timestamp = time.mktime(time.strptime(expiration_time, '%Y-%m-%d %H:%M:%S'))

        current_timestamp = time.time()
        print(f"Current timestamp: {current_timestamp}, Expiration timestamp: {expiration_timestamp}")

        if current_timestamp > expiration_timestamp:
            return "URL expired", 404

        # Log access
        ip_address = request.remote_addr
        print(ip_address)
        
        conn.execute(
            "INSERT INTO access_logs (short_url, ip_address) VALUES (?, ?)",
            (short_url, ip_address)
        )
        conn.commit()

        return jsonify({"original_url": row['original_url']}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/ana/analytics/<short_url>', methods=['GET'])
def get_analytics(short_url):
    conn = get_db_connection()
    try:
        print(f"Fetching analytics for short_url: {short_url}")
        logs = conn.execute("SELECT * FROM access_logs WHERE short_url = ?", (short_url,)).fetchall()
        # print(logs)
        rows_as_dict = [dict(row) for row in logs]
        print(rows_as_dict)

        if not logs:
            return jsonify({'message': 'No logs found for this short URL'}), 404

        access_logs = []
        for log in logs:
            access_logs.append({
                'id': log['id'],
                'short_url': log['short_url'],
                'ip_address': log['ip_address'],
                'access_time': log['access_time']
            })

        return jsonify({'access_logs': access_logs})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
