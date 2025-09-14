import requests
import time
import concurrent.futures

def get_file(url, filename):
    try:
        print(f"About to start downloading {filename} from {url}.")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as file:
            for data in response.iter_content(chunk_size=8192):
                file.write(data)
        print(f"{filename.capitalize()} has been successfully downloaded.")
    except requests.exceptions.RequestException as error:
        return f"Sorry there was an error downloading {filename}: {error}."

def main():
    sites = {
        "https://www.jython.org": "jython.html",
        "http://olympus.realpython.org/dice": "dice.html",
            }

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(get_file, url, filename): filename
                         for url, filename in sites.items()}

        for future in concurrent.futures.as_completed(futures):
            filename = futures[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"{filename} generated an exception: {exc}")

    end_time = time.time()
    print(f"Downloads took {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()