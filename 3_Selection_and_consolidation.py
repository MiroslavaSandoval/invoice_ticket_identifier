############################################################################################################
########################################## F U N C T I O N S ###############################################
############################################################################################################

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
    
def rename_keys(original_dictionary, key_mapping):
    """
    Renames the keys of a dictionary based on a mapping dictionary.

    :param original_dictionary: Dictionary whose keys are to be renamed.
    :param key_mapping: Dictionary with the mapping of current keys to new keys.
    :return: A new dictionary with the renamed keys.
    """
    # Create a new dictionary with the renamed keys
    renamed_dictionary = {key_mapping.get(k, k): v for k, v in original_dictionary.items()}
    return renamed_dictionary


def dictionaries_to_dataframe(xml_summary_dict, tickets_summary_dict, invoice_tickets_relation_dict, key_mapping):
    """
    Converts the data from XML summaries and tickets, along with their relationship, into a pandas DataFrame.
    
    This function takes as input two dictionaries containing summaries of XML invoices and tickets,
    respectively, as well as a dictionary that relates these invoices to the corresponding tickets,
    and a key mapping to rename the keys in the XML summaries dictionaries.
    
    For each invoice-ticket relationship in `invoice_tickets_relation_dict`, the invoice summary is
    combined with the summary of each related ticket, renaming the keys of the invoice summary
    according to `key_mapping`. The 'Pharmacy' keys in the invoice summaries are removed before
    the combination. Each combination is added to a list which is then converted into a pandas DataFrame.
    
    The resulting records in the DataFrame contain a merge of the invoice and ticket data,
    including an identifier for the invoice file (`invoice_file`) and for the ticket
    (`ticket_file`). Missing values in the DataFrame are filled with "NA".
    
    Parameters:
    - xml_summary_dict (dict): Dictionary containing the summaries of the XML invoices.
    - tickets_summary_dict (dict): Dictionary containing the summaries of the tickets.
    - invoice_tickets_relation_dict (dict): Dictionary that relates the invoices with the corresponding tickets.
    - key_mapping (dict): Dictionary that defines how the keys in the invoice summaries should be renamed.
    
    Returns:
    - df (DataFrame): A pandas DataFrame containing the combined information of invoices and tickets,
      ready for further analysis or processing.
    """
    
    records = []
    
    for a, b in invoice_tickets_relation_dict.items():
        d0 = xml_summary_dict[a]
        d0.pop('Farmacia', None)
        d1 = rename_keys(d0, key_mapping)
        
        for b1 in b:
            d2 = tickets_summary_dict[b1]
            d2["invoice_file"] = a
            d2["ticket_file"] = b1
            d = {**d1, **d2}
            records.append(d)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Fill NA where keys/values are missing
    df.fillna("NA", inplace=True)
    
    return df


def calculate_string_similarity(str1, str2):

    """
    Calculates and returns the percentage similarity between two character strings, str1 and str2,
    based on the number of matching characters in the same positions. The similarity is adjusted for
    strings of different lengths by adding spaces to the end of the shorter string until both strings
    have the same length.

    This method is useful for evaluating how similar two strings are, for example, to
    break ties in values or identifiers that are very similar to each other.

    Parameters:
    - str1 (str): First string to compare.
    - str2 (str): Second string to compare.

    Returns:
    - similarity (float): The percentage similarity between the two strings, with 100% indicating
      a perfect match and 0% indicating no match.
    """

    # Align the length of the strings by adding spaces to the shorter one if necessary
    max_len = max(len(str1), len(str2))
    str1 = str1.ljust(max_len)
    str2 = str2.ljust(max_len)
    
    # Count matches
    matches = sum(c1 == c2 for c1, c2 in zip(str1, str2))
    # Calculate similarity as a percentage
    similarity = (matches / max_len) * 100 if max_len > 0 else 0
    return similarity


def calculate_score(x, x_max):
    """
    Calculates a score from 0 to 100 based on a numerical value.
    Numbers <= 31 receive a score of 100, and the score
    decreases linearly for larger numbers up to x_max, where the score reaches 0.

    :param x: The numerical value to be scored.
    :param x_max: The maximum expected value for x for which the score will be 0.
    :return: The calculated score.
    """
    x_min = 31
    if x <= x_min:
        return 100
    else:
        # Calculate the slope based on the decrease of 100 points over the range from x_min to x_max
        m = 100 / (x_max - x_min)
        # Calculate the score ensuring that it is not less than 0
        return round(max(0, 100 - m * (x - x_min)), 0)

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


if __name__ == "__main__":
    


    ############################################################################################################
    ########################################## L I B R A R I E S ###############################################
    ############################################################################################################


    from datetime import datetime
    import json
    import pandas as pd
    import os
    import shutil

    ############################################################################################################
    ############################################ I N P U T S ##################################################
    ############################################################################################################
    xml_path = 'xml_files'

    selected_invoices_path = 'selected_invoices'

    csv_path = selected_invoices_path + '/relation_xml_invoices.csv'

    xml_dict = handle_dictionary("dic_xml.json", "r")

    tickets_dict = handle_dictionary("dic_tickets.json", "r")
                
    invoice_tickets_relation_dict = handle_dictionary("dic_xml_tickets.json", "r")

    key_mapping = {
        'DescripcionProductos': 'ProductDescription_invoice',
        'Total': 'Total_invoice',
        "NUMTICKET": "NUMTICKET_invoice"
    }
    ############################################################################################################
    ######################### P R O D U C T  1 : INVOICES AND TICKETS RELATION IN CSV ##########################
    ############################################################################################################


    df = dictionaries_to_dataframe(xml_dict, tickets_dict, invoice_tickets_relation_dict, key_mapping)

    # Convert date and numeric columns, and add new calculated columns
    df['FechaCompra'] = pd.to_datetime(df['FechaCompra'])
    df['FechaTimbrado'] = pd.to_datetime(df['FechaTimbrado'])
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    df['Total_invoice'] = pd.to_numeric(df['Total_invoice'], errors='coerce')
    df['days_difference'] = (df['FechaTimbrado'] - df['FechaCompra']).dt.days

    # Group and calculate the maximum difference in days per ticket, and compute similarity and score
    df['Max_difference_days'] = df.groupby('ticket_file')['days_difference'].transform('max')
    df['similarity_NUMTICKET'] = df.apply(lambda row: round(calculate_string_similarity(row['NUMTICKET'], row['NUMTICKET_invoice']),0), axis=1)
    df['Day_Score'] = df.apply(lambda row: calculate_score(row['days_difference'], row['Max_difference_days']), axis=1)

    # Sort the DataFrame and remove unnecessary columns
    ordered_columns = [ 'Farmacia', 'ticket_file','invoice_file',  'FechaCompra','Day_Score', 'similarity_NUMTICKET','NUMTICKET_invoice', 'NUMTICKET', 'Total_invoice', 'Total',  'DescripcionProductos', 'ProductDescription_invoice']
    df = df[ordered_columns].sort_values(by=['ticket_file', 'Day_Score','similarity_NUMTICKET'], ascending=[True, False, False])

    # Remove duplicates and unnecessary columns
    df_to_save = df.drop_duplicates(subset='ticket_file', keep='first')


    # Traducir nombres de columnas de Español a Inglés
    df_to_save = df_to_save.rename(columns={
        'Farmacia': 'Pharmacy',
        'FechaCompra': 'Purchase_Date',
        'similarity_NUMTICKET': 'Ticket_Number_Similarity',
        'NUMTICKET_invoice': 'Invoice_Ticket_Number',
        'NUMTICKET': 'Ticket_Number',
        'Total_invoice': 'Invoice_Total',
        'Total': 'Ticket_Total',
        'DescripcionProductos': 'Ticket_Product_Description',
        'ProductDescription_invoice': 'Invoice_Product_Description',
        "ticket_file" : 'Ticket_file',
        "invoice_file" : 'Invoice_file' 
    })



    # Remove duplicates and unnecessary columns
    df_to_save.loc[:, "Ticket_file"] = df_to_save["Ticket_file"].str.replace('_processed.jpeg', '', regex=False)
    df_to_save.loc[:, "Invoice_file"] = df_to_save["Invoice_file"].str.replace('.xml', '', regex=False)

    # Save the DataFrame to a CSV file
    df_to_save.to_csv(csv_path , index=False)

    print(f"DataFrame successfully saved at {csv_path}")

    ############################################################################################################
    ############################### PRODUCT 2: FILES RENAMED WITH PURCHASE DATE ################################
    ############################################################################################################


    # Create final lists of new names and files to copy
    list_new_names= df_to_save['Ticket_file'].to_list()
    list_files_to_copy  = df_to_save['Invoice_file'].to_list()


    # Rename relevant files

    files = os.listdir(xml_path)

    # Iterate over each file in the source directory
    for file in files:
        # Check if the file contains any of the strings in list_A
        if any(string in file for string in list_files_to_copy):
            # Build the full path of the source and destination file
            source_full_path = os.path.join(xml_path, file)
            destination_full_path = os.path.join(selected_invoices_path, file)
            
            # Copy the file from the source path to the destination path
            shutil.copy(source_full_path, destination_full_path)
            print(f"File {file} successfully copied from {xml_path} to {selected_invoices_path}.")

    for old, new in zip(list_files_to_copy, list_new_names):
        rename_files_with_pattern(selected_invoices_path, old, new)
