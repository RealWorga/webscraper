import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def get_text_from_url(url):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    #chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        driver.quit()

if __name__ == "__main__":
    url = input("Enter URL of the webpage: ")
    text = get_text_from_url(url)

    if text:
        print("\nExtracted Text:")
        #Text needs to be encoded to utf-8 for cenrtain websites
        print(text.encode("utf-8"))
