import json
import tempfile
import os
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import base64

def load_json(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)

def render_html(template_path, image_dict):
    env = Environment(loader=FileSystemLoader('/home/jaime/Desktop/PRACTICE-REPOS/test_embajada/templates/'))
    template = env.get_template(template_path)
    rendered_template = template.render(image_dict)
    return rendered_template

if __name__ == "__main__":
    image_path = "/home/jaime/Desktop/PRACTICE-REPOS/test_embajada/images/path_image.json"
    images = load_json(image_path)
    html = render_html('plantilla_prueba_v7_base.html', images)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".html", dir="/home/jaime/Desktop/PRACTICE-REPOS/test_embajada/templates/temp", delete=False) as temp:
        temp_filename = temp.name
        temp.write(html.encode('utf-8'))

    # Set up Chrome WebDriver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1024')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set the path to the ChromeDriver executable
    chrome_driver_path = "/home/jaime/Desktop/PRACTICE-REPOS/test_embajada/chromedriver_linux64/chromedriver"
    service = Service(chrome_driver_path)

    # Enable logging
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'browser': 'ALL'}

    # Create a new instance of the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=caps)

    # Open the temporary HTML file in Chrome
    driver.get("file://" + temp_filename)

    # Save the page as a PDF
    pdf_output_path = "/home/jaime/Desktop/PRACTICE-REPOS/test_embajada/documento_con_imagenes_v7.pdf"
    result = driver.execute_cdp_cmd('Page.printToPDF', {'printBackground': True})
    with open(pdf_output_path, 'wb') as f:
        f.write(base64.b64decode(result['data']))

    # Print browser logs
    for entry in driver.get_log('browser'):
        print(entry)

    # Close the browser window and quit the WebDriver
    driver.quit()

    # Delete the temporary file
    os.remove(temp_filename)
