import requests


def shorten_url(url):
    api_url = f"https://tinyurl.com/api-create.php?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.text

    else:
        return "Erreur lors du raccourcessement du lien."



long_url = "https://www.linkedin.com/in/hanif-djanfarou/"
short_url = shorten_url(long_url)
print(f" url raccourci : {short_url}")