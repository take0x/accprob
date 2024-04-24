from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

driver = webdriver.Chrome()
driver.get('https://kenkoooo.com/atcoder/#/contest/show/e4b1a4f8-2043-4d70-8437-663152a8b700')

time.sleep(1)

links = driver.find_elements(By.XPATH, '//table//td/a')

# url = elem[0].get_attribute('href')
# for l in links:
#     contest_id, problem_num = l.get_attribute('href').split('/')[-1].rsplit('_', 1)
#     print(contest_id, problem_num)

contest_id, problem_num = links[0].get_attribute('href').split('/')[-1].rsplit('_', 1)
subprocess.run(['acc', 'new', contest_id])


driver.close()
