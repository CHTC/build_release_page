import requests
import datetime
import sys
from slugify import slugify


def get_release_info(org: str, repo: str, tag: str):

    release_info_result = requests.request("GET", f"https://api.github.com/repos/{org}/{repo}/releases/tags/{tag}")

    release_info = release_info_result.json()

    return release_info


def build_md(title, tag, repo, body) -> str:
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    md = "---\n" + \
        f"   title: {title}\n" + \
        f"   date: {date}\n" + \
        "   layout: news\n" + \
        f"   release_number: {tag}\n" + \
        f"   release_type: {repo}\n" + \
        "---\n" + \
        f"{body}"

    return md


def main():
    """
    Build the md page for the release
    """

    org, repo = sys.argv[1].split("/")
    tag = sys.argv[2]

    release_info = get_release_info(org, repo, tag)

    title = release_info['name']
    body = release_info['body']

    md = build_md(title, tag, repo, body)

    with open(f"./{slugify(title)}.md", "w") as fp:
        fp.write(md)


if __name__ == '__main__':
    main()
