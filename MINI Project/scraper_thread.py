from PyQt5 import QtCore
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

class ScraperWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(pd.DataFrame)
    progress = QtCore.pyqtSignal(int, int)

    def __init__(self, base_url):
        super().__init__()
        self.base_url = base_url
        self.categories_and_pages = {
            'graphic-design': range(1, 2),
            'seo': range(1, 2)
        }
        self.total_items = len(self.categories_and_pages) * 10
        self.stop_scrap = False
        self.paused = False  # Used to manage the pause state

    def run(self):
        all_data = pd.DataFrame()
        scraped_items = 0
        
        for category, page_range in self.categories_and_pages.items():
            category_data, scraped_items = self.scrape_data(self.base_url, category, page_range, scraped_items)
            all_data = pd.concat([all_data, category_data], ignore_index=True)
            if self.stop_scrap:
                break
            print(f"Scraping category: {category}")

        all_data.to_csv(r'D:\BSCS\3rd Semester\DSA\MINI Project\live_scrap_freelancer_data.csv', index=False, encoding='utf-8')
        self.finished.emit(all_data)

    def scrape_data(self, base_url, category, page_range, scraped_items):
        service = Service(executable_path=r'D:\BSCS\3rd Semester\DSA\chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service=service)
        
        names = []
        profile_links = []
        titles = []
        locations = []
        rates = []
        job_success_scores = []
        total_earnings = []
        categories = []

        for page in page_range:
            url = f"{base_url}/{category}/{page}"
            driver.get(url)
            time.sleep(3)

            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')

            for freelancer in soup.findAll('div', class_='directory-freelancer-item-container'):
                if self.stop_scrap:
                    driver.quit()
                    return pd.DataFrame(), scraped_items
                
                while self.paused:  # Manage pause state
                    time.sleep(1)

                name = freelancer.find('a', class_='find-freelancer-username').text.strip() if freelancer.find('a', class_='find-freelancer-username') else 'N/A'
                profile_link = "https://www.freelancer.pk" + freelancer.find('a', class_='find-freelancer-username')['href'] if freelancer.find('a', class_='find-freelancer-username') else 'N/A'
                title = freelancer.find('div', class_='user-tagline').text.strip() if freelancer.find('div', class_='user-tagline') else 'N/A'
                location = freelancer.find('div', class_='user-location').text.strip() if freelancer.find('div', class_='user-location') else 'N/A'
                rate = freelancer.find('span', class_='user-hourly-rate').text.strip() if freelancer.find('span', class_='user-hourly-rate') else 'N/A'
                job_success = freelancer.find('span', class_='Rating')['data-star_rating'] if freelancer.find('span', class_='Rating') else 'N/A'
                earnings = freelancer.find('div', class_='Earnings')['data-user_earnings'] if freelancer.find('div', class_='Earnings') else 'N/A'

                names.append(name)
                profile_links.append(profile_link)
                titles.append(title)
                locations.append(location)
                rates.append(rate)
                job_success_scores.append(job_success)
                total_earnings.append(earnings)
                categories.append(category)

                scraped_items += 1
                self.progress.emit(scraped_items, self.total_items)

        df = pd.DataFrame({
            'Name': names,
            'Profile Link': profile_links,
            'Title': titles,
            'Location': locations,
            'Rate per Hour': rates,
            'Job Success Score': job_success_scores,
            'Total Earnings': total_earnings,
            'Category': categories
        })
        
        driver.quit()
        return df, scraped_items

    def stop(self):
        self.stop_scrap = True

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
