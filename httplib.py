import httplib2
import json

# Define the connection parameters
HOST = "your-splunk-azure-cluster-url"
PORT = 8089
TOKEN = "your-splunk-token"
CERTIFICATE_FILE = "path/to/your/certificate/file"

# Create an HTTP client object and set the authentication headers
http = httplib2.Http()
http.add_certificate(keyfile=None, certfile=CERTIFICATE_FILE, password=None)
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
url = f"https://{HOST}:{PORT}/services/search/jobs"

# Define the search query and create the request body
search_query = "search index=main | head 10"
request_body = {
    "search": search_query,
    "output_mode": "json"
}

# Send the search request to Splunk and print the results
response, content = http.request(url, "POST", headers=headers, body=json.dumps(request_body))
search_results = json.loads(content.decode("utf-8"))
for result in search_results["results"]:
    print(result)
