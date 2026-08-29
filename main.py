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

def query_stackoverflow(query):
    print(f"\n[*] Querying StackOverflow API for: '{query}'")
    url = f"https://api.stackexchange.com/2.3/search?order=desc&sort=votes&intitle={query}&site=stackoverflow"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            items = response.json().get('items', [])
            print(f"Top 3 StackOverflow questions found:")
            for item in items[:3]:
                print(f" - Score: {item['score']} | Title: {item['title']} | URL: {item['link']}")
        else:
            print(f"[-] StackOverflow API error: {response.status_code}")
    except Exception as e:
        print(f"[-] Error connecting to StackOverflow: {e}")

def query_producthunt(query, token):
    if not token:
        print(f"\n[-] Skipping ProductHunt: No API token provided.")
        return
    print(f"\n[*] Querying ProductHunt API for: '{query}'")
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    graphql_query = """
    query {
      posts(search: "%s", first: 3) {
        edges {
          node {
            name
            tagline
            votesCount
            website
          }
        }
      }
    }
    """ % query
    
    try:
        response = requests.post(url, headers=headers, json={'query': graphql_query})
        if response.status_code == 200:
            data = response.json()
            edges = data.get('data', {}).get('posts', {}).get('edges', [])
            print(f"Top 3 ProductHunt products found:")
            for edge in edges:
                node = edge['node']
                print(f" - {node['name']}: {node['tagline']} | Votes: {node['votesCount']} | URL: {node['website']}")
        else:
            print(f"[-] ProductHunt API error: {response.status_code} {response.text}")
    except Exception as e:
        print(f"[-] Error connecting to ProductHunt: {e}")

def main():
    print("=== SaaS Market Research Plugin ===")
    load_dotenv()
    
    gh_token = os.getenv('GITHUB_TOKEN')
    ph_token = os.getenv('PRODUCTHUNT_TOKEN')
    
    if not gh_token:
        print("[!] No GITHUB_TOKEN found in .env file.")
    if not ph_token:
        print("[!] No PRODUCTHUNT_TOKEN found in .env file.")
        
    search_term = input("\nEnter SaaS keyword or market to validate: ")
    
    query_github(search_term, gh_token)
    query_stackoverflow(search_term)
    query_producthunt(search_term, ph_token)
    
    print("\n[+] Research complete.")

if __name__ == "__main__":
    main()