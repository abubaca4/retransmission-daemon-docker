import urllib.request, json, os

req = urllib.request.Request("https://api.github.com/repos/retransmission/retransmission/releases")
req.add_header("User-Agent", "GitHub-Actions")

try:
    with urllib.request.urlopen(req) as response:
        releases = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching releases: {e}")
    releases = []

stable = next((r for r in releases if not r.get("prerelease")), None)
latest = releases[0] if releases else None

builds = {}
def add_build(ref, tag):
    if ref not in builds: builds[ref] = []
    if tag not in builds[ref]: builds[ref].append(tag)

add_build("main", "main")

if stable:
    add_build(stable["tag_name"], stable["tag_name"])
    add_build(stable["tag_name"], "latest")

if latest:
    add_build(latest["tag_name"], latest["tag_name"])
    add_build(latest["tag_name"], "latest-include-beta")

matrix = [{"ref": ref, "tags": tags} for ref, tags in builds.items()]

with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"matrix={json.dumps(matrix)}\n")
