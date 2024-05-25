import time
import json
import requests
import concurrent.futures

start = time.perf_counter()

all_packages_url = "https://formulae.brew.sh/api/formula.json"
all_packages = requests.get(all_packages_url).json()

package_names = [package.get("name") for package in all_packages][0:10]

package_analytics = []


def download_package(name):
    package_url = f"https://formulae.brew.sh/api/formula/{name}.json"
    package_response = requests.get(package_url)
    package = package_response.json()

    name = package.get("name")
    package_desc = package.get("desc")
    package_30d_installs = package["analytics"]["install"]["30d"][f"{name}"]

    package_data = {"name": name, "desc": package_desc,
                    "30d_installs": package_30d_installs}

    package_analytics.append(package_data)

    response_time_elapsed = package_response.elapsed.total_seconds()
    time.sleep(response_time_elapsed)

    print(f"{name} downloaded in {response_time_elapsed}")


with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_package, package_names)

# trying to use threads
"""
number_of_threads = 5
for thread in range(number_of_threads):
    executor = concurrent.futures.ThreadPoolExecutor()
    # futures = [executor.submit(download_package, package_name) for package_name in package_names if package_names ]

    for package_name in package_names:
"""

with open("package_analytics.json", "w") as f:
    json.dump(package_analytics, f, indent=2)

finish = time.perf_counter()
print(f"\nFinished in {(finish - start)} seconds (s).\n")
