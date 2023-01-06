from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys #sendkeys
import re
from selenium.webdriver.chrome.options import Options
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from functools import reduce

#Load the Excel data into a Dictionary
xlsx_path = "challenge.xlsx" #change this to the correct location
df = pd.read_excel(xlsx_path)
df.rename(columns = {'Phone Number': 'Phone', 'Company Name': 'CompanyName', 'Role in Company': 'Role', 'Last Name ': 'LastName', 'First Name': 'FirstName'}, inplace = True)
excel_rows = df.to_dict('records')

#Chrome setup
chromedriver_path = "chromedriver.exe" #change this to the correct location
chrome_options = Options()
chrome_options.add_argument('headless')
chrome_options.add_argument('disable-extensions')
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument("--incognito");
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
#chrome_options.add_experimental_option("detach", True) #This keeps the browser open if headless is removed
chrome_driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

#Edge setup, performs similarly to Chrome
edgedriver_path = "msedgedriver.exe" #change this to the correct location
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')
edge_options.add_argument('disable-extensions')
edge_options.page_load_strategy = 'eager'
edge_options.add_argument("--incognito");
edge_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
edge_driver = Edge(executable_path=edgedriver_path, options=edge_options)

#Firefox, about two times slower than Chrome/Edge
geckodriver_path = "geckodriver.exe" #change this to the correct location
firefox_option = webdriver.FirefoxOptions()
firefox_option.add_argument('-headless')
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", False)
firefox_option.profile = firefox_profile
firefox_option.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
firefox_driver = webdriver.Firefox(executable_path=geckodriver_path, options=firefox_option, firefox_profile=firefox_profile)

driver_to_use = "CHROME" #possible values are CHROME, FIREFOX or EDGE

driver = chrome_driver
if driver_to_use == "FIREFOX":
    driver = firefox_driver
elif driver_to_use == "EDGE":
    driver = edge_driver

#uncomment this if your are not using headless mode
#driver.maximize_window()

#Visit website
rpa_website = driver.get("http://www.rpachallenge.com/")

#Attempt 0: XPath, just for reference
def xpath_data_input(row):
    first_name = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelFirstName"]')
    last_name = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelLastName"]')
    company_name = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelCompanyName"]')
    role = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelRole"]')
    address = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelAddress"]')
    email = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelEmail"]')
    phone = driver.find_element(By.XPATH, '//*[@ng-reflect-name="labelPhone"]')
    submit_button = driver.find_element(By.CLASS_NAME, 'btn.uiColorButton')

    first_name.click()
    first_name.send_keys(row['FirstName'])
    last_name.click()
    last_name.send_keys(row['LastName'])
    company_name.click()
    company_name.send_keys(row['CompanyName'])
    role.click()
    role.send_keys(row['Role'])
    address.click()
    address.send_keys(row['Address'])
    email.click()
    email.send_keys(row['Email'])
    phone.click()
    phone.send_keys(row['Phone']) 
    submit_button.click()

#Attempt 1: CSS Selectors
def css_data_input(row):
    first_name = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelFirstName"]')
    last_name = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelLastName"]')
    company_name = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelCompanyName"]')
    role = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelRole"]')
    address = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelAddress"]')
    email = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelEmail"]')
    phone = driver.find_element(By.CSS_SELECTOR, 'input[ng-reflect-name="labelPhone"]')
    submit_button = driver.find_element(By.CLASS_NAME, 'btn.uiColorButton')
    
    first_name.click()
    first_name.send_keys(row['FirstName']) 
    last_name.click()
    last_name.send_keys(row['LastName'])
    company_name.click()
    company_name.send_keys(row['CompanyName'])
    role.click()
    role.send_keys(row['Role'])
    address.click()
    address.send_keys(row['Address'])
    email.click()
    email.send_keys(row['Email'])
    phone.click()
    phone.send_keys(row['Phone'])
    submit_button.click()
    
#Attempt 2: Finding Inputs by ID Using Regex
def id_data_input(row):
    form = driver.find_element(By.CSS_SELECTOR, value='body form > div')
    html = form.get_attribute('innerHTML')
    regex_result = re.findall(r"name=\"label([^\s]+)\" id=\"([^\s]+)\"", html)

    for key, id in regex_result:
        e = driver.find_element(By.ID, id)
        e.click()
        e.send_keys(row[key]) # 0 = First Name 
        
    submit_button = driver.find_element(By.CLASS_NAME, 'btn.uiColorButton')
    submit_button.click()
    
#Attempt 3: JavaScript
def js_data_input(row):
    js = f"const d={{labelAddress: '{row['Address']}',labelCompanyName: '{row['CompanyName']}',labelLastName: '{row['LastName']}',labelFirstName: '{row['FirstName']}',labelEmail: '{row['Email']}',labelPhone: '{row['Phone']}',labelRole: '{row['Role']}'}}\nlist = document.querySelectorAll('body form > div input');\nlist.forEach(function(i){{i.value = d[i.getAttribute('ng-reflect-name')];}});\ndocument.querySelector('.btn.uiColorButton').click();"
    driver.execute_script(js)

#Used by Attempts 1-3
def run_test(text, iterations, test_function):
    all = []
    smallest = 100000
    for x in range(0, iterations):
        start_button = driver.find_element(By.CLASS_NAME, 'btn-large.uiColorButton')
        start_button.click()

        for row in excel_rows:
           test_function(row)
        
        #time.sleep(1)
        #driver.get_screenshot_as_file("screenshot.png")
        message = driver.find_element(By.CSS_SELECTOR, value='div.message2')
        a = message.get_attribute('innerText').replace("Your success rate is 100% ( 70 out of 70 fields) in ", "")
        a = int(a.replace(" milliseconds", ""))
        all.append(a)
        if smallest > a:
            smallest = a
            
        reset = driver.find_element(By.CSS_SELECTOR, value='.btn-large.uiColorButton')
        reset.click()

    print(f"Fastest {text} Selector: {smallest}")
    print(f"Average {text} Selector: {reduce(lambda a, b: a + b, all) / len(all)}")


#The JS for Attempt 4
optimized_js = "const s=document.querySelector('body div.instructions .btn-large');\nconst form=document.querySelector('body div.inputFields > form');\nconst b=form.querySelector('.btn.uiColorButton');\ns.click();"
for i, row in enumerate(excel_rows):
    optimized_js += f"\nconst d{i}={{labelAddress:'{row['Address']}',labelCompanyName:'{row['CompanyName']}',labelLastName:'{row['LastName']}',labelFirstName:'{row['FirstName']}',labelEmail:'{row['Email']}',labelPhone:'{row['Phone']}',labelRole:'{row['Role']}'}}\nconst l{i}=form.querySelectorAll('input');\nl{i}.forEach(function(i){{i.value=d{i}[i.getAttribute('ng-reflect-name')];}});\nb.click();"

#The JS for Attempt 6. 
#The last click() is there instead of onSubmit() is to trigger a redraw of the UI, so that the success message text can be found
#It's slower but running this in headless mode already gives 0ms
#We can always generate d0, d1, d2, etc. using a loop instead of hard coding it, so that it works even if the Excel data is changed
hacky_js = """let form=document.querySelector('body div.inputFields > form');
let b=form.querySelector('.btn.uiColorButton');
let d0={labelAddress:'98 North Road',labelCompanyName:'IT Solutions',labelLastName:'Smith',labelFirstName:'John',labelEmail:'jsmith@itsolutions.co.uk',labelPhone:'40716543298',labelRole:'Analyst'}
let d1={labelAddress:'11 Crown Street',labelCompanyName:'MediCare',labelLastName:'Dorsey',labelFirstName:'Jane',labelEmail:'jdorsey@mc.com',labelPhone:'40791345621',labelRole:'Medical Engineer'}
let d2={labelAddress:'22 Guild Street',labelCompanyName:'Waterfront',labelLastName:'Kipling',labelFirstName:'Albert',labelEmail:'kipling@waterfront.com',labelPhone:'40735416854',labelRole:'Accountant'}
let d3={labelAddress:'17 Farburn Terrace',labelCompanyName:'MediCare',labelLastName:'Robertson',labelFirstName:'Michael',labelEmail:'mrobertson@mc.com',labelPhone:'40733652145',labelRole:'IT Specialist'}
let d4={labelAddress:'99 Shire Oak Road',labelCompanyName:'Timepath Inc.',labelLastName:'Derrick',labelFirstName:'Doug',labelEmail:'dderrick@timepath.co.uk',labelPhone:'40799885412',labelRole:'Analyst'}
let d5={labelAddress:'27 Cheshire Street',labelCompanyName:'Aperture Inc.',labelLastName:'Marlowe',labelFirstName:'Jessie',labelEmail:'jmarlowe@aperture.us',labelPhone:'40733154268',labelRole:'Scientist'}
let d6={labelAddress:'10 Dam Road',labelCompanyName:'Sugarwell',labelLastName:'Hamm',labelFirstName:'Stan',labelEmail:'shamm@sugarwell.org',labelPhone:'40712462257',labelRole:'Advisor'}
let d7={labelAddress:'13 White Rabbit Street',labelCompanyName:'Aperture Inc.',labelLastName:'Norton',labelFirstName:'Michelle',labelEmail:'mnorton@aperture.us',labelPhone:'40731254562',labelRole:'Scientist'}
let d8={labelAddress:'19 Pineapple Boulevard',labelCompanyName:'TechDev',labelLastName:'Shelby',labelFirstName:'Stacy',labelEmail:'sshelby@techdev.com',labelPhone:'40741785214',labelRole:'HR Manager'}
let d9={labelAddress:'87 Orange Street',labelCompanyName:'Timepath Inc.',labelLastName:'Palmer',labelFirstName:'Lara',labelEmail:'lpalmer@timepath.co.uk',labelPhone:'40731653845',labelRole:'Programmer'}
let ci = ng.probe(b).componentInstance;
ci.start();
let l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d0[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d1[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d2[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d3[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d4[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d5[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d6[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d7[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d8[i.getAttribute('ng-reflect-name')];});
ci.onSubmit();
l0=form.querySelectorAll('input');
l0.forEach(function(i){i.value=d9[i.getAttribute('ng-reflect-name')];});
b.click();
"""

#This function removes the click Start and looping of the Excel rows
def run_optimized_js_test(text, iterations, js_string):
    all = []
    smallest = 100000
    for x in range(0, iterations):
        driver.execute_script(js_string)
        #time.sleep(1)
        #driver.get_screenshot_as_file("screenshot.png")
        message = driver.find_element(By.CSS_SELECTOR, value='div.message2')
        a = message.get_attribute('innerText').replace("Your success rate is 100% ( 70 out of 70 fields) in ", "")
        a = int(a.replace(" milliseconds", ""))
        all.append(a)
        if smallest > a:
            smallest = a
            
        reset = driver.find_element(By.CSS_SELECTOR, value='.btn-large.uiColorButton')
        reset.click()
    
    print(f"Fastest {text}: {smallest}")
    print(f"Average {text}: {reduce(lambda a, b: a + b, all) / len(all)}")
        

#Attempt 0: XPath, just for reference
run_test("XPath", 100, xpath_data_input)

#Attempt 1: CSS Selectors
run_test("CSS", 100, css_data_input)

#Attempt 2: Finding Inputs by ID Using Regex
run_test("Regex+ID", 100, id_data_input)

#Attempt 3: JavaScript
run_test("JS", 100, js_data_input)

#Attempt 4: Optimizing the JavaScript
run_optimized_js_test("Optimized JS", 100, optimized_js)

#Attempt 5: Throwing Money at Hardware (No code as it was running Attempt 4 on Azure instances)

#Attempt 6: Getting Hacky
run_optimized_js_test("Hacky JS", 100, hacky_js)

driver.quit()
