import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def categorize_links(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error fetching: {errh}")
        return [], []
    except requests.exceptions.ConnectionError as errc:
        print(f"Connecting Error fetching: {errc}")
        return [], []
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error fetching: {errt}")
        return [], []
    except requests.RequestException as e:                 # проверка
        print(f"Error fetching {base_url}: {e}")
        return [], []

    soup = BeautifulSoup(response.text, 'html.parser')
    phishing_sites = []
    malware_sites = []

    for link in soup.find_all('a', href=True):
        url = urljoin(base_url, link['href'])
        if 'phish' in url:
            phishing_sites.append(url)
        else:
            malware_sites.append(url)

    return phishing_sites, malware_sites


def main():
    base_url = input("Введите URL сайта: ")
    phishing_sites, malware_sites = categorize_links(base_url)

    if phishing_sites:
        print("PhishingSites:")
        for url in phishing_sites:
            print(url)
    else:
        print("PhishingSites не найдены")

    if malware_sites:
        print("\nMalwareSites:")
        for url in malware_sites:
            print(url)
    else:
        print("MalwareSites не найдены")
