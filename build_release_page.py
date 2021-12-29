import requests
import sys
from dateutil import parser
import yaml


def get_release_info(org: str, repo: str, tag: str):

    release_info_result = requests.request("GET", f"https://api.github.com/repos/{org}/{repo}/releases/tags/{tag}")

    release_info = release_info_result.json()

    return release_info

def main():
    """
    Build the md page for the release
    """

    org, repo = sys.argv[1].split("/")
    tag = sys.argv[2]

    release_info = get_release_info(org, repo, tag)
    title = release_info['name']
    content = release_info['body']
    date = parser.isoparse(release_info['published_at']).strftime("%Y-%m-%d")

    release = {"title": title, "date": date, "content": content, "release_number": tag, "release_type": repo}

    file = yaml.dump(release)

    with open(f"./{repo}-{tag}.yml", "w") as fp:
        fp.write(file)

if __name__ == '__main__':
    main()
