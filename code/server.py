from flask import Flask, request
import requests
import json
import ipaddress

app = Flask(__name__)

# Replace with your own Discord Webhook
DISCORD_WEBHOOK_URL = 'YOUR WEBHOOK'


def get_ipv4():
    """
    Retrieves the client's public IPv4 address if possible.
    """
    for header in ["X-Forwarded-For", "X-Real-IP"]:
        if header in request.headers:
            raw_ip = request.headers[header].split(",")[0].strip()
            try:
                ip = ipaddress.ip_address(raw_ip)
                if isinstance(ip, ipaddress.IPv4Address):
                    return raw_ip
            except ValueError:
                continue

    try:
        ip = ipaddress.ip_address(request.remote_addr)
        if isinstance(ip, ipaddress.IPv4Address):
            return request.remote_addr
    except ValueError:
        pass

    return "IP not detected"


@app.route('/', methods=['GET', 'POST'])
def index():
    ip_address = get_ipv4()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    method = request.method
    url = request.url
    headers = dict(request.headers)
    cookies = request.cookies
    args = request.args.to_dict()
    form_data = request.form.to_dict()
    json_data = request.get_json(silent=True)

    # Prepare the message for Discord
    embed = {
        "title": "📡 New HTTP Request",
        "color": 0x3498db,
        "fields": [
            {"name": "🌐 Public IP (IPv4)", "value": f"`{ip_address}`", "inline": False},
            {"name": "🔗 Method", "value": f"`{method}`", "inline": True},
            {"name": "📎 URL", "value": f"`{url}`", "inline": False},
            {"name": "🧭 User-Agent", "value": f"`{user_agent}`", "inline": False},
        ]
    }

    # Add headers
    try:
        headers_json = json.dumps(headers, indent=2)[:900]  # Discord limit
        embed["fields"].append({"name": "📬 Headers", "value": f"```json\n{headers_json}```", "inline": False})
    except Exception:
        pass

    # Cookies
    if cookies:
        cookies_json = json.dumps(cookies, indent=2)
        embed["fields"].append({"name": "🍪 Cookies", "value": f"```json\n{cookies_json}```", "inline": False})

    # GET params
    if args:
        args_json = json.dumps(args, indent=2)
        embed["fields"].append({"name": "🔍 GET Params", "value": f"```json\n{args_json}```", "inline": False})

    # POST form
    if form_data:
        form_json = json.dumps(form_data, indent=2)
        embed["fields"].append({"name": "📤 POST Form", "value": f"```json\n{form_json}```", "inline": False})

    # JSON body
    if json_data:
        json_body = json.dumps(json_data, indent=2)
        embed["fields"].append({"name": "📦 JSON Body", "value": f"```json\n{json_body}```", "inline": False})

    # Send to Discord
    payload = {
        "embeds": [embed]
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Error sending to webhook: {e}")

    return "Request received and logged.", 200


if __name__ == '__main__':
    # Local HTTPS with self-signed certificate (optional)
    # app.run(host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))

    # Standard/local environment (HTTP)
    app.run(host='0.0.0.0', port=5000)
