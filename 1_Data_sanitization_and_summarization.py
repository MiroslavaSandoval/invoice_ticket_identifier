###################################################################################################################
###################################### I M P O R T    L I B R A R I E s ###########################################
###################################################################################################################

def import_libraries():
    # Imports libraries
    import cv2
    from datetime import datetime
    import json
    import numpy as np
    import os
    import pytesseract
    from xml.dom.minidom import parse, parseString
    import xml.etree.ElementTree as ET
    from PIL import Image
    from openai import OpenAI
    
    # starts OpenAI client
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    # Indicator that the libraries have been successfully imported
    print("All libraries have been successfully imported.")
    
    # Returns the libraries or variables you need to use outside the function, if necessary
    return cv2, datetime, json, np, os, pytesseract, parse, parseString, ET, Image, client


####################################################################################################
################################ F U N C T I O N S :    T I C K E T S ##############################
####################################################################################################


def preprocess_image(folder, image_name):
    """The preprocess_image function reads an image from a specific folder, converts it to grayscale,
    enhances its contrast through histogram equalization, and applies binarization.
    Then, it saves the processed image in a specific folder and returns the path of the saved image."""

    # Build the full path of the image to be processed
    image_path = os.path.join(folder, image_name)

    # Read the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance contrast with histogram equalization
    equalized = cv2.equalizeHist(gray)

    # Binarization using the original image (as per your specification not to modify this step)
    _, binarized = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    # Define the destination folder for the processed images
    destination_folder = 'processed'
    # Check if the folder exists, if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Modify the save path to include the 'processed' folder
    filename = image_name[:-5] + '_processed.jpeg'
    processed_path = os.path.join(destination_folder, filename)
    
    # Save the processed image in the specified folder
    cv2.imwrite(processed_path, image)

    print(f"Image processed and saved in: {processed_path}")

    return processed_path



def extract_text_from_images(processed_folder, psm_mode):
    """The function extract_text_from_images extracts text from JPEG images in a specific folder 
    using OCR (Optical Character Recognition) with Tesseract, applying a specific configuration 
    based on a given psm (Page Segmentation Mode). The texts extracted from each image are saved 
    in a text file, with separations and labels indicating from which file each portion of text was extracted."""

    # Get a list of all files in the 'processed' folder
    files = os.listdir(processed_folder)
    # Filter only JPG files
    jpg_files = [file for file in files if file.endswith('.jpeg')]

    # Tesseract configuration to use a specific psm mode
    tesseract_config = f'--oem 3 --psm {psm_mode}'

    print("Analyzing images in mode " + str(psm_mode))

    # Open a text file to save the output
    with open('text_output_mode_' + str(psm_mode) + '.txt', 'w', encoding='utf-8') as output_file:
        # Iterate over each JPG file and extract text
        for jpg_file in jpg_files:
            print("Extracting text from " + jpg_file)
            # Build the full path of the image
            full_image_path = os.path.join(processed_folder, jpg_file)
            
            # Open the image
            image = Image.open(full_image_path)
            
            # Use Tesseract to perform OCR on the image with the specified configuration
            text = pytesseract.image_to_string(image, lang="spa", config=tesseract_config)
            
            # Write the extracted text to the file
            output_file.write(f'Text extracted from {jpg_file}:\n')
            output_file.write(text)
            output_file.write('-' * 50 + '\n')
    print("Text extraction completed and saved in text_output_mode_" + str(psm_mode) + ".txt")

def read_file_content(file_name):
    """The read_file_content function opens and reads the full content of a text file
    identified by file_name, removing all newline characters ('\n').
    If the file does not exist and a FileNotFoundError occurs, a message is printed indicating
    that the file was not found. At the end, the content of the file is printed if it was successfully read."""

    # Initialize a variable to store the content
    file_content = ""

    # Try to open the file and read its content
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            file_content = file.read()
            # Remove newline characters
            file_content = file_content.replace("\n", " ")
            print(f"File information from {file_name} loaded.")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return None  # Or you could return an empty string if you prefer ""

    # Return the file content

    return file_content

def get_completion_tickets(text_file):

    """The function sends a prompt to the OpenAI API,
    specifically to a GPT model (in this case, "gpt-3.5-turbo")
    with a set temperature, to obtain a response generated by the model.
    It then returns the content of the first generated response option."""

    prompt = f"""
    Extract from the text of a set of tickets the following information \
    Follow these 7 steps in order:

    1.- All the information from each of the tickets must be analyzed and reported as requested in the following steps. \
    2.- Determine the "Farmacia" where the purchase was made. If the word Chiapas appears on the ticket, the purchase was made at "FARMACIA DEL AHORRO"; otherwise, it was made at "FARMACIA GUADALAJARA". \
    3.- Collect the TOTAL as "Total" without the "$" sign. \
    4.- Collect the purchase date as "FechaCompra" and it must be formatted "YYYY-MM-DD". There should be no "NA". \
    5.- Collect the information under Descripcion and save it in spanish as "DescripcionProductos". If there are multiple product description fields, keep them all in alphabetical order in a string separated by commas. \
    6.- If the purchase was made at "FARMACIA DEL AHORRO", collect ITU which is a string of 27 elements containing dashes, lowercase letters, and numbers, and save it under the key "NUMTICKET"; if it cannot be found, save the value "NA"\
    7.- If after following steps 1, 2, 3, 4, 5, and 6 a field is missing, report it as "NA".\

    The output should be a dictionary, where the key is the name of the file from which the information was extracted.


    ```{text_file}```
    """

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    print("Analysis of Ticket Information using OpenAI completed.")
    return response.choices[0].message.content



def convert_to_dictionary(input_data):
    """Converts a JSON format string into a dictionary.
    
    Args:
        input_data (str, dict): String in JSON format or a dictionary.
    
    Returns:
        dict: The resulting dictionary from converting the string or the same dictionary if input_data is already a dictionary.
    """
    if isinstance(input_data, str):
        try:
            return json.loads(input_data)
        except json.JSONDecodeError:
            print("The string is not in valid JSON format.")
            return None
    elif isinstance(input_data, dict):
        # If it is already a dictionary, do nothing
        return input_data
    else:
        print("The provided data type is not supported.")
        return None

def handle_dictionary(file_name, mode, dictionary=None):
    if mode == 'w':
        # Save the dictionary to a file
        try:
            with open(file_name, 'w') as file:
                json.dump(dictionary, file)
            print("Dictionary successfully saved in " + str(file_name) + ".")
            return True
        except Exception as e:
            print(f"Error saving dictionary: {e}")
            return False
    elif mode == 'r':
        # Load the dictionary from a file
        try:
            with open(file_name, 'r') as file:
                loaded_dictionary = json.load(file)
                # If you need to remove newline characters from the dictionary values
                # Assuming all values are strings, which may not always be the case
                loaded_dictionary = {k: v.replace("\n", "") if isinstance(v, str) else v for k, v in loaded_dictionary.items()}
            print("Dictionary in " + str(file_name) + " successfully loaded.")
            return loaded_dictionary
        except Exception as e:
            print(f"Error loading dictionary: {e}")
            return False
    else:
        print("Unsupported mode. Use 'r' to read or 'w' to write.")
        return False


def load_list_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            # Read all lines from the file and remove the newline character at the end
            list = [line.rstrip('\n') for line in file.readlines()]
        print("List successfully loaded.")
        return list
    except Exception as e:
        print(f"Error loading list: {e}")
        return []

###########################################################################################
################################ F U N C T I O N S : X M L ################################
###########################################################################################

def rename_files_with_pattern(folder_path, string_to_search, string_to_replace):
    """
    Renames files in the specified folder, replacing a specific pattern in the file names.

    Parameters:
    - folder_path (str): Path of the folder containing the files to be renamed.
    - string_to_search (str): Text pattern to search for in the file names.
    - string_to_replace (str): Replacement text for the found pattern.
    """
    print("Files containing " + str(string_to_search) + " in their name will be renamed.")
    for file_name in os.listdir(folder_path):
        # Check if the pattern to search is in the file name
        if string_to_search in file_name:
            # Create the new file name by replacing the searched pattern with the replacement
            new_name = file_name.replace(string_to_search, string_to_replace)
            # Build the full path of the original file and the new file
            original_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            # Rename the file
            os.rename(original_path, new_path)
            print(f'Renamed: "{file_name}" to "{new_name}"')
        else: 
            print("No files to rename.")

def extract_xml_information(xml_directory, customer_attributes, irrelevant_attributes, output_file_name):
    """
    Extracts and saves specific information from XML files into a text file.

    Parameters:
    - xml_directory (str): Path to the directory containing the XML files.
    - customer_attributes (list): List of customer-related attributes that should be ignored.
    - irrelevant_attributes (list): List of irrelevant attributes that should not be included.
    - output_file_name (str): Name of the .txt file where the extracted information will be saved.
    """
    prohibited_attributes = customer_attributes + irrelevant_attributes

    print("Starting extraction of information from XML files.")
    print("For security reasons, the following fields are omitted:")
    for attribute in prohibited_attributes:
        print(attribute)
    
    with open(output_file_name, 'w', encoding='utf-8') as file:
        for xml_name in os.listdir(xml_directory):
            if xml_name.endswith('.xml'):
                print("Analyzing file " + str(xml_name))
                full_path = os.path.join(xml_directory, xml_name)
                dom = parse(full_path)
                
                unique_elements = list({e.tagName for e in dom.getElementsByTagName('*')})
                
                file.write(f'{xml_name}:\n')
                for element_name in unique_elements:
                    elements = dom.getElementsByTagName(element_name)
                    for element in elements:
                        attributes = element.attributes
                        for i in range(attributes.length):
                            attr = attributes.item(i)
                            if attr.name not in prohibited_attributes:
                                file.write(f"  {attr.name}: {attr.value}\n")
                
                mnemonic_elements = dom.getElementsByTagName('NEMONICO')
                for element in mnemonic_elements:
                    if element.getAttribute('nombre') == 'NUMTICKET':
                        numticket_value = element.firstChild.nodeValue if element.firstChild else ""
                        file.write(f'"{element.getAttribute("nombre")}":{numticket_value}\n')
                
                file.write('-' * 50 + '\n')
    print("Information extraction from XML files completed.")

def filter_file_lines(file_name, lines_to_exclude):
    """
    Reads a file, filters out lines that begin with any of the specified prefixes,
    and overwrites the file with the remaining lines.

    Parameters:
    - file_name (str): The name or path of the file to be processed.
    - lines_to_exclude (list): A list of strings; lines beginning with any of these strings will be excluded.
    """

    print("The following information will be filtered from the file " + file_name + ":")
    for line in lines_to_exclude:
        print(line)

    filtered_lines = []
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            if not any(line.strip().startswith(prefix) for prefix in lines_to_exclude):
                filtered_lines.append(line)

    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(filtered_lines)

    print("Sensitive data filtering completed.")

def get_completion_xml(text_file):

    """The function get_completion sends a prompt to the OpenAI API,
    specifically to a GPT model (in this case, "gpt-3.5-turbo")
    with a set temperature, to obtain a response generated by the model.
    It then returns the content of the first generated response option."""
    prompt = f"""
    Extract from the text of a set of invoices the following information \
    Follow these 6 steps:

    1.- All files must be analyzed and reported.\
    2.- Determine if the purchase was made at Farmacia Guadalajara or at Farmaceutica de Chiapas (Farmacias del ahorro) and save it in a field called "Farmacia". \
    3.- Collect the "NUMTICKET" field if the purchase was made at Farmacias del ahorro, and if not found, save the value "NA". \
    4.- In all cases, collect the "Total". There should be no "NA". \
    5.- Collect the invoiced date, in spanish is Fecha Timbrado and save it in the value "FechaTimbrado" which must be in the format "YYYY-MM-DD". There should be no "NA". \
    6.- Collect information in Description and save it in the value "DescripcionProductos". If there are multiple product description fields, keep them all in alphabetical order in a string separated by commas. Do not translate the descriptions. \

    The output should be a dictionary, where the key is the name of the file from which the information was extracted.

    ```{text_file}```
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0,
    )
    
    print("Analysis of XML file information using OpenAI completed.")
    return response.choices[0].message.content


if __name__ == "__main__":
        
    ###############################################################################################
    ###############################   F I X E D   R O U T E S    ##################################
    ###############################################################################################


    cv2, datetime, json, np, os, pytesseract, parse, parseString, ET, Image, client = import_libraries()

    pytesseract.pytesseract.tesseract_cmd = r'C://Users//MI17441//AppData//Local//Programs//Tesseract-OCR//tesseract.exe'

    ticket_files = os.listdir('Tickets') 

    tickets_jpg = [ticket for ticket in ticket_files if ticket.endswith((('.jpeg', '.jpg')))] 

    text_tickets= 'text_output_mode_4.txt'

    route_xml = 'xml_files'

    text_xml= 'text_xml.txt'

    excluded_lines_txt = "excluded_lines.txt"

    irrelevant_attributes_txt = "irrelevant_attributes.txt"

    customer_attributes_txt = "customer_attributes.txt"

    ##############################################################################################################
    #########################   E X E C U T I O N   O F   T I C K E T   F U N C T I O N S  #####################
    ##############################################################################################################

    # Execute preprocessing on all .jpeg images in the current directory
    for ticket_jpg in tickets_jpg:
        processed_image_path = preprocess_image("Tickets", ticket_jpg)

    extract_text_from_images('processed', 4)

    # Load text from tickets
    tickets_content = read_file_content(text_tickets)

    #Summary of the information and organization in dictionary 
    summary_dict_tickets = get_completion_tickets(tickets_content)

    # Format cleaning
    summary_dict_tickets = json.loads(summary_dict_tickets)

    # Saving final dictionary
    handle_dictionary("dic_tickets.json", "w", dictionary=summary_dict_tickets)

    ####################################################################################################
    #########################   E X E C U T I O N   O F   X M L   F U N C T I O N S #####################
    ####################################################################################################

    rename_files_with_pattern(route_xml, "_{RfcReceiver}_{Series}_{Folio}_{RfcReceiver}_{Series}_{Folio}", "CFC110121742")

    lines_to_exclude = load_list_from_file(excluded_lines_txt)

    irrelevant_attributes = load_list_from_file(irrelevant_attributes_txt)

    customer_attributes = load_list_from_file(customer_attributes_txt)

    extract_xml_information(route_xml, customer_attributes, irrelevant_attributes, text_xml)

    filter_file_lines(text_xml, lines_to_exclude)

    xml_file_content = read_file_content(text_xml)

    xml_summary_dict = get_completion_xml(xml_file_content)
    # Format cleaning
    xml_summary_dict = convert_to_dictionary(xml_summary_dict)

    # Saving final dictionary 
    handle_dictionary("dic_xml.json", "w", dictionary=xml_summary_dict)