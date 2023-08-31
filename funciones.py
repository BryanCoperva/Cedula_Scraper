from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from funciones import *
from selenium.common.exceptions import NoSuchElementException

def find_and_click_element(driver, xpath):
    """
    Find and click an element using its XPath.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        xpath (str): The XPath to locate the element.
    """
    element = driver.find_element(By.XPATH, xpath)
    element.click()

def get_values_from_inputs(driver, input_ids):
    """
    Get values from input elements using their IDs.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        input_ids (list): List of IDs of input elements.

    Returns:
        list: List of values retrieved from the input elements.
    """
    values = [driver.find_element(By.ID, input_id).get_attribute("value") for input_id in input_ids]
    return values




def process_excel_file(init, final, file_path):
    """
    Process an Excel file, perform data transformations, and return a DataFrame.

    Args:
        init (int): Start index for selecting rows from the DataFrame.
        final (int): End index (exclusive) for selecting rows from the DataFrame.
        file_path (str): Path to the Excel file to be processed.

    Returns:
        pandas.DataFrame: A DataFrame with the processed and transformed data.
    """
    
    df = pd.read_excel(file_path)
    df['Name'] = df.Name.apply(lambda X: X.replace('/', ' ').replace('*', '').rstrip())
    df_filtered = df['Name']
    df_filtered.drop_duplicates(inplace=True)
    df_input = pd.DataFrame(df_filtered).iloc[init:final]
    
    def split_name(name):
        # Implement the split_name function here
        pass
    
    df_input['NameSplit'] = df_input.Name.apply(lambda X: split_name(X))
    df_input['Name'] = df_input.NameSplit.apply(lambda X: X[0])
    df_input['Last Name'] = df_input.NameSplit.apply(lambda X: X[1])
    df_input['Middle Name'] = df_input.NameSplit.apply(lambda X: X[2])
    
    return df_input


from selenium import webdriver


# Función de inicialización
def iniciar_scraper(driver, url, wait_condition=False, class_name=None):
    """
    Initialize a Chrome WebDriver and open a specified webpage.

    Args:
        driver (WebDriver): An instance of the Selenium WebDriver.
        url (str): The URL of the webpage to open.
        wait_condition (bool): If True, wait for up to 30 seconds for the presence of an element.
        class_name (str): The class name of the element to wait for.

    Returns:
        None
    """
    driver.get(url)  # Open the webpage
    
    if wait_condition and class_name:
        # Perform scrolling until the element is found
        while True:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
                break  # Stop the loop after finding the element
            except:
                # Scroll down by 200 pixels
                driver.execute_script("window.scrollBy(0, 100);")
        
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))






def split_name(name):
    name = name.replace('*','').replace('/',' ').rstrip()
    #name.replace('/',' ')
    splited = get_name(name)
    if len(splited) <3:
        nam1 = splited[0]
        nam2 = splited[1]
        return [nam1, nam2, None]
    if len(splited) <4:
        nam1 = splited[0]
        nam2 = splited[1]
        nam3 = splited[2]
        return [nam1, nam2, nam3]
    nam1 = ' '.join(splited[:-2])
    nam2 = splited[-2]
    nam3 = splited[-1]
    return [nam1, nam2, nam3]
def get_name(name, inverse=False):
    flag=0
    skips = ['de', 'los', 'la', 'santa', 'del']
    namedir = name.lower().split(' ')
    new_name = list()
    for i in range(len(namedir)):
        word = namedir[i]
        if flag:
            temp.append(namedir[i-1])
        if word in skips:
            if not flag:
                temp = list()
            flag=1
            continue
        if flag:
            temp.append(namedir[i])
            word = ' '.join(temp)
        new_name.append(word)
        flag = 0
    return new_name


def cédula_profesional(driver, nombre, apellido_paterno, apellido_materno):
    """
    Search for professional cédula using Name, Paternal Last Name, and Maternal Last Name.

    Args:
        driver (WebDriver): An instance of the Selenium WebDriver.
        nombre (str): First name of the person.
        apellido_paterno (str): Paternal last name of the person.
        apellido_materno (str): Maternal last name of the person.

    Returns:
        dict: A dictionary containing the professional cédula information if found.
    """
    # Bloqueo inicio
    data = []
    bloqueo1 = None
    try:
        bloqueo1 = driver.find_element(By.CLASS_NAME, 'tp-gateway')
        driver.execute_script("window.scrollBy(0, 200);")
        driver.execute_script("window.scrollBy(1, 200);")
        bloqueo1 = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME,'tp-gateway'))
        )
        bloqueo1.click()

        driver.refresh()


    

        
        #bloqueo1.click()
    except NoSuchElementException:
        pass  # Continúa con el código si el elemento no está presente
    
    celda_nombre = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="input-nombre"]'))
    )
    celda_nombre = driver.find_element(By.XPATH, '//*[@id="input-nombre"]')
    celda_nombre.send_keys(nombre)

    # Ingresar Apellido Paterno
    celda_paterno = driver.find_element(By.XPATH, '//*[@id="input-apaterno"]')
    celda_paterno.send_keys(apellido_paterno)

    # Ingresar Apellido Materno
    celda_materno = driver.find_element(By.XPATH, '//*[@id="input-amaterno"]')
    celda_materno.send_keys(apellido_materno)

    # Click en botón buscar
    buscar = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH,'//*[@id="container-form-1"]/form/div[4]/div/input')), 
    )
    buscar.click()
    max_wait_time = 5  # Tiempo máximo de espera en segundos
    start_time = time.time()  # Momento de inicio de espera

    while time.time() - start_time < max_wait_time:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            driver.refresh()
            break  # Salir del bucle si se encuentra la ventana emergente
        except:

            time.sleep(1)  # Esperar 1 segundo antes de intentar nuevamente

        
        # Encontrar botones ver-mas
    ver_botones = driver.find_elements(By.CLASS_NAME, 'ver-mas')
        # Iterar sobre los botones
    
    
    for ver in ver_botones:
        cantidad_registros = len(ver_botones)
        print("Cantidad de registros:", cantidad_registros)

        # Desplazar la página para hacer visible el botón
        driver.execute_script("arguments[0].scrollIntoView();", ver)
        ver.click()
        
        # Encontrar los elementos de entrada de texto por su id
        input_cedula = driver.find_element(By.ID, "input-cedula-result")
        input_tipo = driver.find_element(By.ID, "input-tipo-result")
        input_sexo = driver.find_element(By.ID, "input-sexo-result")
        input_nombre = driver.find_element(By.ID, "input-nombre-result")
        input_paterno = driver.find_element(By.ID, "input-paterno-result")
        input_materno = driver.find_element(By.ID, "input-materno-result")
        input_escuela = driver.find_element(By.ID, "input-escuela-result")
        input_titulo = driver.find_element(By.ID, "input-titulo-result")

        # Obtener los valores de los campos
        valor_cedula = input_cedula.get_attribute("value")
        valor_tipo = input_tipo.get_attribute("value")
        valor_sexo = input_sexo.get_attribute("value")
        valor_nombre = input_nombre.get_attribute("value")
        valor_paterno = input_paterno.get_attribute("value")
        valor_materno = input_materno.get_attribute("value")
        valor_escuela = input_escuela.get_attribute("value")
        valor_titulo = input_titulo.get_attribute("value")

        # Agregar los valores a la lista de diccionarios
        data.append({
        "Cédula": valor_cedula,
        "Tipo de Cédula": valor_tipo,
        "Sexo": valor_sexo,
        "Nombre": valor_nombre,
        "Paterno": valor_paterno,
        "Materno": valor_materno,
        "Escuela": valor_escuela,
        "Título": valor_titulo
        })
        # Encontrar los elementos de entrada de texto por su id
        cerrar = driver.find_element(By.XPATH, '//*[@id="cerrar_resut_personal"]')
        cerrar.click()
    driver.quit()
