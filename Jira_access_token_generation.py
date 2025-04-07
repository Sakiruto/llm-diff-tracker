from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session
import os
import json 
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 

authorization_base_url = "https://auth.atlassian.com/authorize"
token_url = "https://auth.atlassian.com/oauth/token"

client_id = os.getenv("JIRA_CLIENT_ID")
client_secret = os.getenv("JIRA_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:5000/callback"  # {server_url}/callback

# redirect url that I optained from composio default integration 
# https://prerelease.hellozelo.com/?state=production_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb25uZWN0aW9uSWQiOiJjOTA5MTczYi1kYmY4LTQzM2YtYTA0ZS1hNjMyYjZiODg3YjYiLCJpbnRlZ3JhdGlvbklkIjoiOTkyMzU1MTctZjE0MS00ZTgwLTg3MGEtNjE0MmNkZWU0YjJmIiwiYXBwTmFtZSI6ImppcmEiLCJjbGllbnRJbmZvIjp7InByb2plY3RJZCI6IjY0NjhjOGMwLWFlZDgtNGIzZi04ZGQ4LWM0ODJmNzM5OTA1MiIsIm1lbWJlcklkIjoiMzI4MWVmMzUtMjRmNS00YTI3LTliYzQtMTJhNThlNjUxMzg2IiwiZW1haWwiOiJzaHJpc2h2ZXNoLnJlZGR5QGhlbGxvemVsby5jb20ifSwiaWF0IjoxNzQyNDAyNzE2fQ.tlyShx8Jgxk7nr6rKPk1Et6h1bsSS2TNQhXXupe1dps&code=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI0NzYyODVlNy0yMWYxLTRhZTMtOGJhMi1jNzNjNTViMDFjZTgiLCJzdWIiOiI3MTIwMjA6NTM5ODAwZjItYzJlOS00Y2Y5LWI5YzYtNjdkMTE3Njk4MGI0IiwibmJmIjoxNzQyNDAyNzI1LCJpc3MiOiJhdXRoLmF0bGFzc2lhbi5jb20iLCJpYXQiOjE3NDI0MDI3MjUsImV4cCI6MTc0MjQwMzAyNSwiYXVkIjoiMnZad0lLeTE5cW1ac2E3TEpvbzJ1dmMzaDlLVlJQNEkiLCJjbGllbnRfYXV0aF90eXBlIjoiTk9ORSIsImh0dHBzOi8vaWQuYXRsYXNzaWFuLmNvbS9wa2NlIjoiUlZMaGtSK3BuZ3JiSmMyL25LR0xqZlNMVnZUaXlOTlJqc3EvK2VKM3NOd1VmbEkxL2RIclFnNjlBZW9qTmRBUDk5SXVNVXJjYmc5ZzNXQ3hKN3J0ZC9xU3BER25QRzBkdnd2elhmVnlEWFo5Umk4SysxNWtzcU1hU0dpTURKbXk5dVZpWVY1NU1FcDFyaU5Ueks4dUpCbzFkRldmWFZod0NMV1VpdEJ6dlJIeDNGaz0iLCJodHRwczovL2lkLmF0bGFzc2lhbi5jb20vaXYiOiJ3YjBYK081TjZEcGp5c2RUIiwiaHR0cHM6Ly9pZC5hdGxhc3NpYW4uY29tL3ZlcmlmaWVkIjp0cnVlLCJodHRwczovL2lkLmF0bGFzc2lhbi5jb20vdWp0IjoiNDc2Mjg1ZTctMjFmMS00YWUzLThiYTItYzczYzU1YjAxY2U4Iiwic2NvcGUiOlsibWFuYWdlOmppcmEtY29uZmlndXJhdGlvbiIsIm1hbmFnZTpqaXJhLWRhdGEtcHJvdmlkZXIiLCJtYW5hZ2U6amlyYS1wcm9qZWN0IiwibWFuYWdlOmppcmEtd2ViaG9vayIsIm1hbmFnZTpzZXJ2aWNlZGVzay1jdXN0b21lciIsIm9mZmxpbmVfYWNjZXNzIiwicmVhZDpqaXJhLXVzZXIiLCJyZWFkOmppcmEtd29yayIsInJlYWQ6c2VydmljZWRlc2stcmVxdWVzdCIsIndyaXRlOmppcmEtd29yayIsIndyaXRlOnNlcnZpY2VkZXNrLXJlcXVlc3QiXSwiaHR0cHM6Ly9pZC5hdGxhc3NpYW4uY29tL2F0bF90b2tlbl90eXBlIjoiQVVUSF9DT0RFIiwiaHR0cHM6Ly9pZC5hdGxhc3NpYW4uY29tL2hhc1JlZGlyZWN0VXJpIjp0cnVlLCJodHRwczovL2lkLmF0bGFzc2lhbi5jb20vc2Vzc2lvbl9pZCI6ImQ3NGQyYjE3LWMwOTUtNDE4Ny05NjBlLTNiOWZmYzBlMzhjOSIsImh0dHBzOi8vaWQuYXRsYXNzaWFuLmNvbS9wcm9jZXNzUmVnaW9uIjoidXMtZWFzdC0xIn0.jK6oHIEHzXahJUEYom4EzHwvla3LgjzPW9aSWYtyYeQ


@app.route("/")
def login():
    scope = ["read:jira-user", "read:jira-work"]
    audience = "api.atlassian.com"

    jira_oauth = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    authorization_url, state = jira_oauth.authorization_url(
        authorization_base_url,
        audience=audience,
    )
    session["OAUTH_STATE"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    jira_oauth = OAuth2Session(client_id, state=session["OAUTH_STATE"], redirect_uri=redirect_uri)
    token_json = jira_oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)
    with open("token.json", "w") as token_file:
        json.dump(token_json, token_file, indent=4) 
    return token_json,200
    
if __name__ == "__main__":
    app.run(debug=True)
