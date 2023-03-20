from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import time
import random

## Comment this line if you already have the users_linkedin.txt
with open("users_linkedin.txt", "w", encoding="utf-8") as archivo:
    archivo.write("Base de datos")
    archivo.write("\n")

import json

with open("config.json") as f:
    config = json.load(f)

## This function only writes in the .txt file
def write_doc(name_profile, work_name):
    with open("users_linkedin.txt", "a", encoding="utf-8") as archivo:
        archivo.write(name_profile)
        archivo.write(",")

        if isinstance(work_name, list):
            if all(isinstance(i, list) for i in work_name):

                for i in range(0, len(work_name)):
                    linea = ",".join(work_name[i])
                    archivo.write(linea)

                    if i < (len(work_name)) - 1:
                        archivo.write(",")

            else:
                linea = ",".join(work_name)
                archivo.write(linea)


## I have created this function so that it tries to search for a path more than once, and in case it does not exist it does not generate error
def waiting_to(path, limit=3):
    intento = 0
    while intento < limit:
        try:
            WebDriverWait(driver, timeout=10).until(
                lambda d: d.find_element(By.XPATH, path)
            )
            return True
        except:
            print("Refreshing page...")
            driver.refresh()
            intento += 1
    else:
        return False


## This function was created to simulate the ktyping of a slow person.
def typing_delay(text, element_selenium, enter=False):
    time.sleep(random.uniform(0.1, 0.2))

    for char in text:
        time.sleep(random.uniform(0.1, 0.4))
        element_selenium.send_keys(char)

    if enter == True:
        time.sleep(random.uniform(0.2, 0.5))
        element_selenium.send_keys(Keys.RETURN)


## This function was created to find in which position the "experience" section is located.
# This function returns the number of where the "experience" section is located.
### The text is in spanish because my LinkedIn was in spanish, please change it to your language
def search_experience():
    time.sleep(random.uniform(0.3, 0.8))
    extract_experience = driver.find_element(
        By.XPATH,
        "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[3]/div[2]/div/div/div/h2/span[1]",
    )
    text_span = extract_experience.text
    experience_place = 3
    print("Buscando experiencia...")

    if text_span != "Experiencia":
        time.sleep(random.uniform(0.3, 0.8))
        extract_experience = driver.find_element(
            By.XPATH,
            "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[4]/div[2]/div/div/div/h2/span[1]",
        )
        text_span = extract_experience.text
        experience_place = 4

        if text_span != "Experiencia":
            experience_place = 5

    return experience_place


## I have created this function to detect in which position the desired experience is located.
# This function returns the position to where the target company's expertise is located.
def search_target_company(n_works_max, section):
    for n_work in range(1, n_works_max + 1):
        link_path_company = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[1]/a".format(
            section, n_work
        )
        try:
            extract_company = driver.find_element(By.XPATH, link_path_company)
            href_company = extract_company.get_attribute("href")

            if (href_company == config["LINKEDIN_TARGET_COMPANY"]) or (
                href_company == config["LINKEDIN_TARGET_COMPANY_OPTIONAL"]
            ):
                company_place = n_work
                print("The company was found in its experience!")
                return company_place
        except:
            return print("The company wasn't found in its experience")

    return print("The company wasn't found in its experience")


## I have created this function to extract the name of each position he/she/they held in the target company.
# This function returns the name of the position that person held and the dates he/she/they held it.
def get_work_name(experience_place, company_place):

    array_positions = []
    print("Buscando nombre de trabajos")

    try:
        path_work_name = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div/div[1]/div/span/span[1]".format(
            experience_place, company_place
        )
        extract_work_name = driver.find_element(By.XPATH, path_work_name)
        time.sleep(random.uniform(0.3, 0.8))
        text_span = extract_work_name.text

        time.sleep(random.uniform(0.3, 0.8))
        job_date = get_work_date(experience_place, company_place)

        array_info = [text_span, job_date]
        array_positions.append(array_info)

        return array_positions

    except:
        try:
            path_work_name = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[1]/div[1]/div/span/span[1]".format(
                experience_place, company_place
            )
            extract_work_name = driver.find_element(By.XPATH, path_work_name)
            time.sleep(random.uniform(0.3, 0.8))
            text_span = extract_work_name.text

            time.sleep(random.uniform(0.3, 0.8))
            job_date = get_work_date(experience_place, company_place)

            array_info = [text_span, job_date]
            array_positions.append(array_info)

            return array_positions

        except:
            array_ = get_work_names(experience_place, company_place)
            return array_


## I have created this function to extract the names of each position he/she/they held in the target company.
# This function returns the names of the positions that person held and the dates he/she/they held it.
def get_work_names(experience_place, company_place):

    array_positions = []
    ul_works_path = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li".format(
        experience_place, company_place
    )
    ul_works = driver.find_elements(By.XPATH, ul_works_path)
    time.sleep(random.uniform(0.3, 0.8))
    n_positions_in_capgemini = len(ul_works)

    for n_position in range(1, n_positions_in_capgemini + 1):
        path_work_name = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div[1]/a/div/span/span[1]".format(
            experience_place, company_place, n_position
        )
        time.sleep(random.uniform(0.3, 0.8))
        get_name = driver.find_element(By.XPATH, path_work_name)
        name_position = get_name.text
        job_date = get_work_dates(experience_place, company_place, n_position)

        array_info = [name_position, job_date]
        array_positions.append(array_info)

    return array_positions


## I have created this function because there are many variables in Linkedin profiles.
## I mean, there are profiles that in their experience, have skills, there are others that don't, there are profiles that have a city, there are others that don't.
# This function returns the date when that person worked in the position.
def get_work_date(experience_place, company_place):
    print("Starting date extraction...")
    try:
        path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[1]/div[1]/span[2]/span[1]".format(
            experience_place, company_place
        )
        time.sleep(random.uniform(0.3, 0.8))
        extract_work_time = driver.find_element(By.XPATH, path_work_time)
        date_span = extract_work_time.text

        if "-" not in date_span:
            raise ValueError("Ocurrió un error")

        return date_span
    except:
        path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div/div[1]/div/span/span[1]".format(
            experience_place, company_place
        )
        time.sleep(random.uniform(0.3, 0.8))
        extract_work_time = driver.find_element(By.XPATH, path_work_time)
        date_span = extract_work_time.text

        return date_span


## I have created this function because there are many variables in Linkedin profiles.
## I mean, there are profiles that in their experience, have skills, there are others that don't, there are profiles that have a city, there are others that don't.
# This function returns the dates when that person worked in the position.
def get_work_dates(experience_place, company_place, work_position):
    print("Starting dates extraction...")
    try:
        path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div[1]".format(
            experience_place, company_place, work_position
        )
        driver.find_element(By.XPATH, path_work_time)

        print("This profile has no skills")
        try:
            path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div[1]/a/span/span[1]".format(
                experience_place, company_place, work_position
            )
            time.sleep(random.uniform(0.3, 0.8))
            extract_work_time = driver.find_element(By.XPATH, path_work_time)
            date_span = extract_work_time.text

            if "-" not in date_span:
                raise ValueError("Ocurrió un error")

            return date_span

        except:
            path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div[1]/a/span[1]/span[1]".format(
                experience_place, company_place, work_position
            )
            time.sleep(random.uniform(0.3, 0.8))
            extract_work_time = driver.find_element(By.XPATH, path_work_time)
            date_span = extract_work_time.text

            if "-" in date_span:
                return date_span

            else:

                path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div[1]/a/span[1]/span[2]".format(
                    experience_place, company_place, work_position
                )
                time.sleep(random.uniform(0.3, 0.8))
                extract_work_time = driver.find_element(By.XPATH, path_work_time)
                date_span = extract_work_time.text

                if "-" not in date_span:
                    raise ValueError("Ocurrió un error")

                return date_span

    except:
        print("This profile has skills")
        try:
            path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div/a/span/span[1]".format(
                experience_place, company_place, work_position
            )
            time.sleep(random.uniform(0.3, 0.8))
            extract_work_time = driver.find_element(By.XPATH, path_work_time)
            date_span = extract_work_time.text

            if "-" not in date_span:
                raise ValueError("Ocurrió un error")

            return date_span

        except:
            path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div/a/span[1]/span[1]".format(
                experience_place, company_place, work_position
            )
            extract_work_time = driver.find_element(By.XPATH, path_work_time)
            time.sleep(random.uniform(0.3, 0.8))
            date_span = extract_work_time.text

            if "-" in date_span: 
                return date_span

            else:

                path_work_time = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[2]/div[2]/ul/li[{}]/div/div[2]/div/a/span[2]/span[1]".format(
                    experience_place, company_place, work_position
                )
                time.sleep(random.uniform(0.3, 0.8))
                extract_work_time = driver.find_element(By.XPATH, path_work_time)
                date_span = extract_work_time.text

                return date_span


## I created this function because LinkedIn changes the profiles path
# This function returns the right path detected
def search_path_profile(div, li):
    try:
        print("cheking path profile...")
        path = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[{}]/div/ul/li[{}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a".format(
            div, li
        )
        exist = waiting_to(path, 2)

        if exist:
            return path
        else:
            raise ValueError("Ocurrió un error")

    except:
        try:
            path = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[{}]/div/ul/li[{}]/div/div/div[2]/div/div[1]/div/span/span/a".format(
                div, li
            )
            exist = waiting_to(path, 2)

            if exist:
                return path
            else:
                raise ValueError("Ocurrió un error")

        except:
            path = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[{}]/div/ul/li[{}]/div/div/div[2]/div[1]/div[1]/div/span/span/a".format(
                div, li
            )
            exist = waiting_to(path, 2)

            if exist:
                return path
            else:
                raise ValueError("Ocurrió un error")


## I created this function because sometimes LinkedIn adds advertising on top of profiles
# This function returns 3 if there is advertising
def check_adv():
    if (
        waiting_to(
            "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/div/div/div/a"
        )
        == True
    ):
        return 3
    else:
        return 2


# Download WebDriver
print("Downloading webdriver...")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(
    service=ChromiumService(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    ),
    options=options,
)
driver.maximize_window()
print("Download.")
print(" ")

# Go to LinkedIn
print("Going to LinkedIn...")
time.sleep(random.randint(1, 2))
driver.get("http://www.linkedin.com/")
time.sleep(random.randint(1, 3))

waiting_to("/html/body/nav/div/a[2]")
# Search login and click on
driver.find_element(By.XPATH, "/html/body/nav/div/a[2]").click()
time.sleep(random.randint(1, 5))

# Type username
print("Typing email...")
box_username = driver.find_element(
    By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[1]/input"
)
typing_delay(config["LINKEDIN_USERNAME"], box_username)
time.sleep(random.randint(1, 3))

# Type password
print("Typing password...")
box_password = driver.find_element(
    By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[2]/input"
)
typing_delay(config["LINKEDIN_PASSWORD"], box_password, True)
print("Loging...")
print(" ")
time.sleep(random.uniform(0.1, 0.4))

input("Press Enter when you are in the list of people who work or used to work in the target company.")

again = "Y"
path_main = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/div[2]/div/button[2]"

while again == "Y":
    try:

        for profile_nn in range(1, 11):
            n_profile = profile_nn
            repetir_perfil = "Y"

            while repetir_perfil == "Y":
                print("Initializing... ")
                try:
                    print(" ")

                    print("Starting with profile #", n_profile, "...")
                    sales = check_adv()
                    print("Searching the profile path...")
                    profile_path = search_path_profile(sales, n_profile)
                    time.sleep(random.uniform(0.3, 0.9))
                    print("Clicking on the profile...")
                    driver.find_element(By.XPATH, profile_path).click()
                    time.sleep(random.uniform(0.3, 0.8))
                    print("Accessing profile #", n_profile, "...")

                    try:
                        time.sleep(random.uniform(0.3, 0.8))
                        driver.find_element(
                            By.XPATH, "/html/body/div[3]/div/div/div[1]/h2"
                        )
                        time.sleep(random.uniform(0.3, 0.8))
                        driver.find_element(
                            By.XPATH, "/html/body/div[3]/div/div/div[3]/button"
                        ).click()
                        print("Profile cannot be accessed.")
                        time.sleep(random.uniform(0.3, 0.8))
                        repetir_perfil = "N"

                    except:
                        print("Loading profile  #", n_profile, "...")
                        waiting_to(
                            "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1",
                            2,
                        )

                        time.sleep(random.uniform(0.3, 0.9))

                        # Identifying the place of the experience
                        experience_place = search_experience()

                        # getting the numbers max of elements (works)
                        print("Identifying experience...")
                        ul_experience_path = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li".format(
                            experience_place
                        )
                        time.sleep(random.uniform(0.3, 0.8))
                        ul_experience = driver.find_elements(
                            By.XPATH, ul_experience_path
                        )
                        n_works = len(ul_experience)
                        time.sleep(random.uniform(0.3, 0.8))

                        # Identifying the place of the company target
                        print("Identifying company target...")
                        company_place = search_target_company(n_works, experience_place)

                        name_profile_ = driver.find_element(
                            By.XPATH,
                            "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1",
                        )
                        time.sleep(random.uniform(0.3, 0.8))

                        name_profile = name_profile_.text
                        time.sleep(random.uniform(0.3, 0.8))

                        # Getting the name of the work(s) and their dates
                        work_name = get_work_name(experience_place, company_place)

                        print(" ")
                        write_doc(name_profile, work_name)

                        # Trying to find out the name of the company he/she/they moved to after resigning from the target company.
                        try:
                            link_path_nextwork = "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[{}]/div[3]/ul/li[{}]/div/div[1]/a".format(
                                experience_place, company_place - 1
                            )
                            extract_nextwork = driver.find_element(
                                By.XPATH, link_path_nextwork
                            )
                            href_nextwork = extract_nextwork.get_attribute("href")
                            with open(
                                "users_linkedin.txt", "a", encoding="utf-8"
                            ) as archivo:
                                archivo.write(",")
                                archivo.write(href_nextwork)
                                archivo.write("\n")
                        except:
                            with open(
                                "users_linkedin.txt", "a", encoding="utf-8"
                            ) as archivo:
                                archivo.write(",NA")
                                archivo.write("\n")
                        print(" ")
                        time.sleep(random.uniform(0.3, 2.8))
                        driver.back()
                        repetir_perfil = "N"
                except:
                    print("I had issues checking the #" + str(n_profile))
                    n_profile = input(
                        "Enter the profile number you want to proceed to analyze: "
                    )
        print("Turning the page...")
        try:
            driver.find_element(By.XPATH, path_main).click()
        except:
            try:
                botton_path = "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[{}]/div/div/button[2]".format(
                    sales + 3
                )
                driver.find_element(By.XPATH, botton_path).click()
            except:
                try:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/div[2]/div/button[2]/span",
                    ).click()
                except:
                    path_main = input(
                        "I could't find the 'next' bottom, please click 'next' and then enter :( "
                    )
    except:
        again = input("Enter 'Y' if you wish to continue with this script (Y/N)")

print(" ")
print("Done.")

time.sleep(1)
driver.quit()
