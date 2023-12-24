import requests

import json

file = requests.get("https://archlinux.org/mirrors/status/json/")
file = file.content

content = json.loads(file)
China = []
for i in content["urls"]:
    if i["country"] in ["China", "Hong Kong", "Macau","Taiwan"] and i["score"]:
        China.append(
            {"url": i["url"], "last_sync": i["last_sync"], "score": i["score"]}
        )

with open("mirrorlist", "w") as f:
    f.writelines(
        "\n".join(
            [
                f"Server = {n['url']}$repo/os/$arch"
                for n in sorted(China, key=lambda s: s["score"])[:7]
            ]
        )
    )
