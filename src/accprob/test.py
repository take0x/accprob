from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

# url = 'https://kenkoooo.com/atcoder/#/contest/show/e4b1a4f8-2043-4d70-8437-663152a8b700'
url = input("URL : ")

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options)
driver.get(url)

time.sleep(3)

contest_title = driver.find_element(By.XPATH, '//h1').text
links = driver.find_elements(By.XPATH, '//table//td/a')

for ind, l in enumerate(links):
    contest_id = l.get_attribute('href').split('/')[-3]
    problem_id = l.get_attribute('href').split('/')[-1]
    problem_dir = contest_title + '/' + format(ind + 1, '02') + '/test'
    problem_url = f'https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}'
    subprocess.run(['oj', 'd', '-d', problem_dir, problem_url], stdout=subprocess.DEVNULL)
    print('Downloaded the test case :', format(ind + 1, '02'), problem_id)

driver.close()
