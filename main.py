import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def save_text_to_pdf(text, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    text_object = c.beginText()
    text_object.setTextOrigin(10, 750)
    text_object.setFont("Helvetica", 12)

    lines = text.split('\n')
    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()

def get_text_from_url(url):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

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
    url = input("Enter the URL of the webpage: ")
    text = get_text_from_url(url)

    if text:
        print("\nExtracted Text:")
        print(text.encode("utf-8"))

        save_folder = "docs/webscraped-pdfs"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        num = 1
        while os.path.exists(f"{save_folder}/{num}.pdf"):
            num += 1

        pdf_path = f"{save_folder}/{num}.pdf"
        save_text_to_pdf(text, pdf_path)
        print(f"\nText saved to {pdf_path}")