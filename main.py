import os
print('Starting SaaS Market Researcher...')
if not os.path.exists('.env'):
    choice = input('No API keys detected. [1] Add keys to .env [2] Continue with web-scraping fallback: ')
    if choice == '2':
        print('Initializing web-scraping engine...')
    else:
        print('Please populate .env file.')
else:
    print('API keys found. Connecting to APIs...')