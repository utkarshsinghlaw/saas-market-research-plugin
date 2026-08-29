import os
import requests
from dotenv import load_dotenv

def query_github(query, token):
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'} if token else {}
    print(f"\n[*] Querying GitHub API for: '{query}'")
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json().get('items', [])
            print(f"Top 3 repositories found:")
            for item in items[:3]:
                print(f" - {item['full_name']} | Stars: {item['stargazers_count']} | URL: {item['html_url']}")
        else:
            print(f"[-] GitHub API error: {response.status_code}")
    except Exception as e:
        print(f"[-] Error connecting to GitHub: {e}")

def main():
    print("=== SaaS Market Research Plugin ===")
    load_dotenv()
    
    gh_token = os.getenv('GITHUB_TOKEN')
    
    if not gh_token:
        print("[!] No GITHUB_TOKEN found in .env file.")
        choice = input("Continue with unauthenticated rate-limited requests? (y/n): ")
        if choice.lower() != 'y':
            print("Exiting.")
            return

    search_term = input("\nEnter SaaS keyword or market to validate: ")
    query_github(search_term, gh_token)
    
    print("\n[+] Research complete.")

if __name__ == "__main__":
    main()