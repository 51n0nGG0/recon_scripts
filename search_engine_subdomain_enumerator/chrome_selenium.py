from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import urllib.parse as urlparse
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

from search_engine_subdomain_enumerator.proxy_selector import get_random_proxy

class SeleniumEnumerator():
    def __init__(self, domain):
        self.driver = None
        self.domain = domain
        self.subdomains = []
        self.base_url = "https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0"
        self.timeout = 25
        self.engine_name = "Google"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 200
        
        options = Options()
        
        options.add_argument("--start-maximized")
        
        """
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920x1080")
        """
        proxy = get_random_proxy()
        
        print(proxy)

        proxy_user = os.getenv("PROXY_USER")
        proxy_password = os.getenv("PROXY_PASSWORD")
        
        print(proxy_user)
        print(proxy_password)
        
        proxy_options = {
            "proxy": {
                "http": f"http://{proxy_user}:{proxy_password}@{proxy}",
                "https": f"http://{proxy_user}:{proxy_password}@{proxy}"
            }
        }
        
        print(proxy_options)
        
        options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
        )
        
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(seleniumwire_options=proxy_options, options=options, service=Service(ChromeDriverManager().install()))
    
    def get_page(self, num):
        return num + 10
    
    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS
    
    def check_max_pages(self, page_no):
        if self.MAX_PAGES == 0:
            return False
        return page_no >= self.MAX_PAGES
    
    def extract_domains(self,resp):
        links_list = set()
        link_regx = re.compile('<cite.*?>(.*?)</cite>')
        try:
            links_list = set(link_regx.findall(resp))
            for link in links_list:
                link = re.sub('<span.*>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain:
                    print("%s: %s" % (self.engine_name, subdomain))
                    self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        return links_list
    
    def should_sleep(self):
        time.sleep(random.uniform(3, 10))
        return
    
    def generate_query(self):
        if self.subdomains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.subdomains[:self.MAX_DOMAINS - 2])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query
    
    def check_response_errors(self, resp):
        if isinstance(resp, str) and 'Our systems have detected unusual traffic' in resp:
            print('\033[91m[!] Error: Google probably now is blocking our requests\033[0m')
            print('\033[91m[~] Finished now the Google Enumeration ...\033[0m')
            return False
        return True
    
    def enumerate(self):
        print(f"[\033[34m{self.engine_name}\033[0m] Enumerating subdomains for {self.domain}...")
        flag = True
        page_no = 0
        prev_links = []
        retries = 0
        
        while flag:
            query = self.generate_query()
            count = query.count(self.domain)
            print(f"[\033[34m{self.engine_name}\033[0m] Query: {query} | Subdomains found: {len(self.subdomains)} | Page: {page_no}")
            
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)
                
            if self.check_max_pages(page_no):
                return self.subdomains
            resp = self.send_req(query, page_no)
            with open(f"resp{page_no}.html", "w", encoding="utf-8") as file:
                file.write(resp)
            
            if not self.check_response_errors(resp):
                return self.subdomains
            links = self.extract_domains(resp)
            
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)
                
                if retries >= 3:
                    return self.subdomains
                
            prev_links = links
            self.should_sleep()
            
        return self.subdomains

    def send_req(self, query, page_no=1):
        url = self.base_url.format(query=query, page_no=page_no)
        
        try:
            self.driver.get(url)
            
            if self.is_accept_cookies_page():
                self.accept_cookies()
                
            return self.driver.page_source
                
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
            
    def is_accept_cookies_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Accept all"]'))
            )
            return True
        except:
            return False
        
    def accept_cookies(self):
        accept = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="Accept all"]'))
        )
        accept.click()
        time.sleep(2)
        
    def run(self):
        domain_list = self.enumerate()
        print(domain_list)
        for domain in domain_list:
            print(domain)