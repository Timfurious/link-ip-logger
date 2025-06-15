# link-ip-logger

This project is a simple Flask web application that logs HTTP requests and sends detailed information about each request to a Discord channel via a webhook. It captures the client's public IPv4 address, HTTP method, URL, user agent, headers, cookies, GET/POST parameters, and JSON body.

## Features

- Logs every HTTP request (GET and POST) to the root endpoint `/`
- Extracts and displays:
  - Public IPv4 address (if available)
  - HTTP method and URL
  - User-Agent string
  - Request headers and cookies
  - GET and POST parameters
  - JSON body (if present)
- Sends all collected information as a formatted embed to a specified Discord webhook

## Installation

1. **Clone the repository** and install dependencies:
    ```sh
    pip install flask requests
    ```

2. **Set your Discord webhook URL**  
   Replace the value of `DISCORD_WEBHOOK_URL` in `script.py` with your own Discord webhook.

3. **Run the application:**
    ```sh
    python server.py
    ```

4. **Send HTTP requests** to `http://localhost:5000/` and check your Discord channel for logs.

## Example

Here is a sample log sent to Discord:

```
📡 New HTTP Request
🌐 Public IP (IPv4): 192.168.1.10
🔗 Method: GET
📎 URL: http://localhost:5000/
🧭 User-Agent: Mozilla/5.0 ...
📬 Headers: {...}
🍪 Cookies: {...}
🔍 GET Params: {...}
📤 POST Form: {...}
📦 JSON Body: {...}
```

## Disclaimer

This project is for educational and demonstration purposes only.  
**Do not use it for malicious purposes or to collect data without user consent.**

---

**Author:** Timfurious
