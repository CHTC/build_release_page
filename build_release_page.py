import requests
import sys
from dateutil import parser
import datetime

def get_release_numbers(release_tag):
    """
    Get the correct release number to link to the release documentation
    :param release_tag: string in form 'VX_Y_Z' when X, Y and Z are variables
    :return: [X, Y, Z]
    """

    release_tag_underscore_delimited = release_tag[1:]  # Remove the preceeding 'V'
    release_numbers = release_tag_underscore_delimited.split("_")

    return release_numbers


def get_version_history_url(x: int, y: int, z: int):
    """
    Generate the doc path based on
    Assuming a version number X.Y.Z, the following links can be used

    X == 9, Y == 0
    https://htcondor.readthedocs.io/en/v9_0/version-history/stable-release-series-90.html#version-9-0-Z

    X == 9, Y > 0
    https://htcondor.readthedocs.io/en/v9_1/version-history/development-release-series-91.html#version-9-Y-Z

    When X > 9:

    X > 9, Y == 0
    https://htcondor.readthedocs.io/en/vX_0/version-history/lts-release-X-0.html#version-X-0-Z

    X > 9, Y > 0
    https://htcondor.readthedocs.io/en/vX_x/version-history/feature-release-X-x.html#version-X-Y-Z
    """
    if int(x) == 9:
        if int(y) == 0:
            return f"https://htcondor.readthedocs.io/en/v9_0/version-history/stable-release-series-90.html#version-9-0-{z}"
        elif int(y) > 0:
            return f"https://htcondor.readthedocs.io/en/v9_1/version-history/development-release-series-91.html#version-9-{y}-{z}"
    elif int(x) > 9:
        if int(y) == 0:
            return f"https://htcondor.readthedocs.io/en/v{x}_0/version-history/lts-release-{x}-0.html#version-{x}-0-{z}"
        elif int(y) > 0:
            return f"https://htcondor.readthedocs.io/en/v{x}_x/version-history/feature-release-{x}-x.html#version-{x}-{y}-{z}"
    else:
        raise Exception("Invalid Release Numbers, or Tag Syntax")


def get_release_info(org: str, repo: str, tag: str):

    release_info_result = requests.request("GET", f"https://api.github.com/repos/{org}/{repo}/releases/tags/{tag}")

    release_info = release_info_result.json()

    return release_info


def build_md(title, date, tag, repo, body) -> str:

    x, y, z = get_release_numbers(tag)

    version_history_url = get_version_history_url(x, y, z)

    md = "---\n" + \
        f"\ttitle: {title}\n" + \
        f"\tdate: {date}\n" + \
        "\tlayout: news\n" + \
        f"\trelease_number: {tag}\n" + \
        f"\trelease_type: {repo}\n" + \
        "---" \
        "\n" \
        f"The HTCondor team is pleased to announce the release of HTCondor {x}.{y}.{z}." \
        f"\n\n" \
        f"{body}" \
        f"\n\n" \
        f"A complete list of new features and fixed bugs can " \
        f"be found in the <a href='{version_history_url}'>Version History</a>." \
        f"\n\n" \
        f"Instructions to download HTCondor {x}.{y}.{z} binaries and source code " \
        f"are available on the HTCondor <a href='https://htcondor.org/htcondor/download/'>Download Page</a>."

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
    date = parser.isoparse(release_info['published_at']).strftime("%Y-%m-%d")

    md = build_md(title, date, tag, repo, body)

    with open(f"./{tag}.md", "w") as fp:
        fp.write(md)


if __name__ == '__main__':
    main()
