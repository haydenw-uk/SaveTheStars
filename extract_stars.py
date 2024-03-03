import requests
import csv

def get_starred_repositories(username, token):
    url = f'https://api.github.com/users/{username}/starred'
    headers = {'Authorization': f'token {token}'}
    starred_repositories = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            starred_repositories.extend(response.json())
            if 'link' in response.headers:
                links = {rel[6:-1]: url[url.index('<')+1:url.index('>')] for url, rel in
                         (link.split(';') for link in response.headers['link'].split(','))}
                url = links.get('next')
            else:
                url = None
        else:
            print(f"Failed to fetch starred repositories. Status code: {response.status_code}")
            return None

    return starred_repositories

def save_to_csv(starred_repositories, filename='stars.csv'):
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['Name', 'Description', 'Language', 'Stars', 'URL']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for repo in starred_repositories:
            writer.writerow({
                'Name': repo['name'],
                'Description': repo['description'],
                'Language': repo['language'],
                'Stars': repo['stargazers_count'],
                'URL': repo['html_url']
            })
            print(f"[INFO] Saving {repo['name']} to {filename}")

def display_welcome_message():
    ascii_logo_art = """ 
███████  █████  ██    ██ ███████     ████████ ██   ██ ███████     ███████ ████████  █████  ██████  ███████ ██ 
██      ██   ██ ██    ██ ██             ██    ██   ██ ██          ██         ██    ██   ██ ██   ██ ██      ██ 
███████ ███████ ██    ██ █████          ██    ███████ █████       ███████    ██    ███████ ██████  ███████ ██ 
     ██ ██   ██  ██  ██  ██             ██    ██   ██ ██               ██    ██    ██   ██ ██   ██      ██    
███████ ██   ██   ████   ███████        ██    ██   ██ ███████     ███████    ██    ██   ██ ██   ██ ███████ ██                                                                                                    
    """
    print(ascii_logo_art + "\nSave your GitHub Repo Stars from your account to a csv file.\n\n")

if __name__ == "__main__":
    display_welcome_message()

    try:
        github_username = input("Enter your GitHub Username : ")
        access_token = input("Enter your GitHub Personal Access Token : ")
    except Exception:
        print("[ERROR] Invalid input = quit. Please restart this script to try again.")
        exit()

    starred_repositories = get_starred_repositories(github_username, access_token)

    if starred_repositories:
        save_to_csv(starred_repositories)
        print("[COMPLETION INFO] All starred repositories saved to stars.csv")
    else:
        print("[WARNING] Failed to save starred repositories. Check your credentials and / or internet connection and try again.")
