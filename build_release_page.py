import requests
import sys
from dateutil import parser
import yaml


def get_github_release_info(org: str, repo: str, tag: str):
    """
    Uses the github api to grab the information about the new release.

    https://docs.github.com/en/rest/reference/releases

    :param org: The org that owns the repo
    :param repo: The repo that the release was made in
    :param tag: The tag attached to the release
    :return: A dictionary of information about the release
    """

    release_info_result = requests.request("GET", f"https://api.github.com/repos/{org}/{repo}/releases/tags/{tag}")

    release_info = release_info_result.json()

    return release_info

def read_input():
    """
    Reads the input which is has expected form 'org/repo tag'

    :return: The values split into the appropriate components
    """

    org, repo = sys.argv[1].split("/")
    tag = sys.argv[2]

    return org, repo, tag

def main():
    """
    Build the yml release file
    """

    # Read in the input
    org, repo, tag = read_input()

    # Use the API to get the missing information
    release_info = get_github_release_info(org, repo, tag)

    # Build the release info dictionary to be dumped
    title = release_info['name']
    content = release_info['body']
    date = parser.isoparse(release_info['published_at']).strftime("%Y-%m-%d")
    release_number = tag[1:].replace("_", ".")  # Assumes tag is of form 'V#_#_#'
    sort_key = ".".join(x.zfill(2) for x in release_number.split("."))

    release = {"title": title, "date": date, "content": content, "release_number": release_number, "release_type": repo,
               "sort_key": sort_key}

    # Get the dictionary as a yaml file
    file = yaml.dump(release)

    # Drop the file at root
    with open(f"./{repo}-{tag}.yml", "w") as fp:
        fp.write(file)


if __name__ == '__main__':
    main()
