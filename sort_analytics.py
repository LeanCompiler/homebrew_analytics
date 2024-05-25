import json


def install_sort(analytics):
    return analytics.get("30d_installs")


with open("package_analytics.json", "r") as file:
    package_analytics = json.load(file)

package_analytics.sort(key=install_sort, reverse=True)

print(json.dumps(package_analytics, indent=2))
