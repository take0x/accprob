import requests
from bs4 import BeautifulSoup


def main() -> None:
    url = input("URL: ")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("title")
    print(title.text)


if __name__ == "__main__":
    main()
