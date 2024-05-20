
########################## G E N E RA L   F U N C T I O N #############################################

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



#######################################################################################################################
######################################## C O M P O N E N T  F U N C T I O N S #########################################
#######################################################################################################################
    
############################################  D A T E    A N A L Y S I S ############################################

def filter_date_dictionaries(stamp_date_a, dictionary_b):
    """
    Filters and returns a new dictionary from dictionary_b, including only those
    elements whose PurchaseDate "FechaCompra" is before a given date 'stamp_date_a'.

    This process involves converting the date strings into datetime objects for precise comparison,
    allowing the identification and selection of only those elements from dictionary_b that meet
    the criteria of being before the specified stamp date.

    Parameters:
    - stamp_date_a (str): The stamp date in the format 'YYYY-MM-DD' against which the purchase dates
      in dictionary_b will be compared.
    - dictionary_b (dict): Dictionary containing the elements to be filtered, each with a
      'PurchaseDate'  "FechaCompra" that will be evaluated.

    Returns:
    - filtered_dictionary (dict): A new dictionary that includes only the elements from
      dictionary_b whose 'PurchaseDate' "FechaCompra" is before 'stamp_date_a'.
    """
    
    # Convert Stamp Date A to datetime object
    stamp_date = datetime.strptime(stamp_date_a, '%Y-%m-%d')
    
    # Dictionary to store filtered results
    filtered_dictionary = {}
    
    # Iterate over each item in dictionary B
    for key, value in dictionary_b.items():
        # Convert the PurchaseDate "FechaCompra" to datetime object for comparison
        purchase_date = datetime.strptime(value["FechaCompra"], '%Y-%m-%d')
        
        # Compare the PurchaseDate with Stamp Date A
        if purchase_date < stamp_date:
            filtered_dictionary[key] = value
    
    return filtered_dictionary



def date_filter(A, B, a):
    """
    Applies a date-based filter between two dictionaries, A and B, comparing the 'StampDate' "FechaTimbrado"
    of a specified element in A against the 'PurchaseDates' "FechaCompra" in B. Returns a dictionary that
    encapsulates the result of the filtering, maintaining the original structure and keys of A to
    clearly identify the processed element.

    This method is useful for determining which elements in B have a 'PurchaseDate'  "FechaCompra" that
    is before the 'StampDate'  "FechaTimbrado" of a specific element in A, facilitating selection or exclusion processes
    based on temporal criteria.

    Parameters:
    - A (dict): Dictionary containing an element with a specified 'StampDate'  "FechaTimbrado".
    - B (dict): Dictionary whose elements, each with a 'PurchaseDate'  "FechaCompra", will be compared
      and potentially included in the result based on the date comparison.
    - a (int): Index of the element in A whose 'StampDate' is used as the comparison criterion.

    Returns:
    - result (dict): A dictionary that encapsulates the elements of B that meet the date criterion,
      associated under the key of the evaluated element of A, maintaining a clear reference
      to the context of the comparison made.
    """

    keys_A = list(A.keys())
    date_results = filter_date_dictionaries(A[keys_A[a]]["FechaTimbrado"], B)

    result = {keys_A[a]: date_results}

    return result



############################################ T O T A L    S I M I L A R I T Y ############################################


def compare_floating_numbers(num1, num2):
    """
    Compares two floating-point numbers to determine their percentage similarity,
    based on the number of matching digits in each position after the decimal point.

    The numbers are first converted to floats (if not already), and then to strings,
    ensuring that both have the same number of digits after the decimal point.
    Similarity is calculated as the percentage of digits that match in the same
    positions in both string representations of the numbers.

    Parameters:
    - num1 (float or str): First number to compare.
    - num2 (float or str): Second number to compare.

    Returns:
    - similarity_percentage (float): Percentage of similarity between the two numbers, based on
      matching digits after the decimal point.
    """
    # Convert both numbers to floats
    num1 = float(num1)
    num2 = float(num2)
    
    # Convert the numbers to strings with the same number of digits after the decimal point
    max_decimals = max(len(str(num1).split('.')[1]), len(str(num2).split('.')[1]))
    num1_str = f"{num1:.{max_decimals}f}"
    num2_str = f"{num2:.{max_decimals}f}"
    
    # Count matches and calculate the percentage of similarity
    matches = sum(digit1 == digit2 for digit1, digit2 in zip(num1_str, num2_str) if digit1.isdigit() and digit2.isdigit())
    total_digits = sum(digit.isdigit() for digit in num1_str)
    
    # Calculate the similarity percentage, avoiding division by zero
    similarity_percentage = (matches / total_digits * 100) if total_digits > 0 else 0
    
    return similarity_percentage


def max_similarity_score_floats(list1, list2):
    """
    Finds the highest similarity score between the elements of two lists of floating-point numbers.
    
    Calculates the percentage similarity between each pair of floating-point numbers from the two lists and returns
    the highest similarity score found.
    
    Parameters:
    - list1 (list): First list of floating-point numbers.
    - list2 (list): Second list of floating-point numbers.
    
    Returns:
    - max_score (float): The highest similarity score among all possible pairs.
    """
    scores = [compare_floating_numbers(num1, num2) for num1 in list1 for num2 in list2]
    max_score = max(scores) if scores else 0
    return max_score
def find_best_total(A, B, a):
    # Dictionary to store the dictionaries that meet the condition

    """
    Identifies and returns a dictionary that represents the best match for 'Total'
    between a specific element of a dictionary A and the elements of a dictionary B.

    The function evaluates the similarity of 'Total' values between a selected element from
    dictionary A and all elements of dictionary B, using a similarity metric
    based on the comparison of floating-point numbers. The best match is determined by the
    highest similarity score between the 'Total' value of the selected element from A and
    the 'Total' values of all elements in B.

    In case there are multiple elements in B with the same maximum similarity score,
    all these elements will be included in the returned dictionary, associated under the key of
    the evaluated element from A.

    Parameters:
    - A (dict): Dictionary whose values include a 'Total' to be compared.
    - B (dict): Dictionary with which the 'Total' values of A will be compared.
    - a (int): Index of the element in A for which to find the best match in B.

    Returns:
    - max_dics (dict): Dictionary containing the best match(es) found,
      where the key is the identifier of the evaluated element in A and the value is a dictionary
      with the best matches found in B, using the similarity of 'Total' values as a comparison criterion.
    """
     
    keys_B = list(B.keys())
    keys_A = list(A.keys())

    search_key = "Total"
    
    total_A = A[keys_A[a]][search_key]

    global_max = 0

    max_dics = {}
    # Initialize max_dic_for_A as an empty dictionary
    max_dic_for_A = {}
          
    for key_B in keys_B:
        total_B = B[key_B][search_key]
        local_max = max_similarity_score_floats([total_A], [total_B])
        
        if local_max > global_max:
            global_max = local_max
            max_dic_for_A = {key_B: B[key_B]}  # Reinitialize with the new maximum value
        elif local_max == global_max and global_max != 0:
            max_dic_for_A[key_B] = B[key_B]  # Add to an existing dictionary
            
    max_dics[keys_A[a]] = max_dic_for_A
    
    return max_dics



################################### S T R I N G   A N A L Y S I S :   NUMTICKET, DESCRIPTION,  PHARMACY  ###############################

def LCSubstr(S1, S2):
    """The LCSubstr function calculates the length of the longest common substring 
    (LCSubstr) between two strings S1 and S2."""
    # Ensure both are strings for comparison
    S1 = str(S1).lower() if isinstance(S1, str) else str(S1)
    S2 = str(S2).lower() if isinstance(S2, str) else str(S2)
    
    m = len(S1)
    n = len(S2)
    result = 0  # Length of the LCSubstr
    length_table = [[0] * (n + 1) for _ in range(m + 1)]  # Initialize the matrix

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                length_table[i][j] = 0
            elif S1[i-1] == S2[j-1]:
                length_table[i][j] = length_table[i-1][j-1] + 1
                result = max(result, length_table[i][j])
            else:
                length_table[i][j] = 0
    return result

def max_consecutive_chars(A, B):
    """
    Calculates the maximum similarity of consecutive substrings between the elements of lists A and B.
    
    The function compares each element of A with each element of B to find the greatest length
    of common substring (using LCSubstr). The sum of the maximum lengths for each element of A
    defines the return value.
    
    Parameters:
    - A (list): First list of strings to compare.
    - B (list): Second list of strings to compare.
    
    Returns:
    - total_max (int): Sum of the maximum lengths of common substrings for each element of A.
    """
    total_max = 0
    for a in A:
        a = a.lower() if isinstance(a, str) else a
        max_length_for_a = 0
        for b in B:
            b = b.lower() if isinstance(b, str) else b
            max_length_for_a = max(max_length_for_a, LCSubstr(a, b))
        total_max += max_length_for_a
    return total_max



def find_max_consecutive_substring(A, B, a, key_pos_B):
    """
    Finds and stores in a dictionary the elements of B that have the maximum similarity of 
    consecutive substrings with a specific element of A, based on a specific key.

    Compares a specific value (given by key_pos_B) from the element 'a' in dictionary A with all 
    corresponding values in dictionary B. Stores the elements of B that achieve the maximum similarity 
    with the element from A in a new dictionary.

    Parameters:
    - A (dict): Dictionary containing elements to compare.
    - B (dict): Dictionary with elements to be compared against A.
    - a (int): Index of the specific element from A to compare.
    - key_pos_B (str): The key of the elements in B that will be compared with the element in A.

    Returns:
    - result (dict): A dictionary with the elements of B that have the maximum similarity with the
      specific element of A, indicated by 'a'.
    """
    keys_B = list(B.keys())
    keys_A = list(A.keys())
    
    value_A = A[keys_A[a]][key_pos_B]
    global_max = 0
    max_dic_for_A = {}

    for key_B in keys_B:
        value_B = B[key_B][key_pos_B]
        local_max = max_consecutive_chars([value_A], [value_B])

        if local_max > global_max:
            global_max = local_max
            max_dic_for_A = {key_B: B[key_B]}
        elif local_max == global_max and global_max != 0:
            max_dic_for_A[key_B] = B[key_B]

    result = {keys_A[a]: max_dic_for_A}
    return result


####################################### D I S C R E P A N C Y   R E S O L U T I O N   F U N C T I O N  ####################################


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

def highest_similarity(A, B, a, key_pos_B):
    
    """
    Finds and returns a dictionary that represents the best match for a specific value
    identified by the key key_pos_B in an element of the dictionary A against
    all corresponding values in the dictionary B, using the similarity of character strings
    as the comparison criterion.

    This function is useful for breaking ties and finding the most similar match when there
    are character strings very similar to each other, based on a percentage of similarity
    calculated for each pair of values.

    Parameters:
    - A (dict): Main dictionary containing the values to compare.
    - B (dict): Dictionary against which the values of A are compared.
    - a (int): Index of the element in A whose value is to be compared.
    - key_pos_B (str): The key under which the values to be compared are found in both
      dictionaries.

    Returns:
    - max_dics (dict): Dictionary containing the best match found, where the
      key is the identifier of the evaluated element in A and the value is a dictionary with the
      best match found in B, based on the similarity of the character string values specified by key_pos_B.
    """

    keys_B = list(B.keys())
    keys_A = list(A.keys())
    
    value_A = A[keys_A[a]][key_pos_B]

    global_max = 0
    max_dics = {}
    max_dic_for_A = {}
          
    for key_B in keys_B:
        value_B = B[key_B][key_pos_B]
        local_max = calculate_string_similarity(value_A, value_B)
        
        if local_max > global_max:
            global_max = local_max
            max_dic_for_A = {key_B: B[key_B]}  # Reinitialize with the new maximum value
        elif local_max == global_max and global_max != 0:
            max_dic_for_A[key_B] = B[key_B]  # Add to an existing dictionary
            
    max_dics[keys_A[a]] = max_dic_for_A
    
    return max_dics


###################################################################################################################################################
####################################################  M A I N   L O O P   F U N C T I O N  ########################################################
###################################################################################################################################################

def relate_invoices_tickets(xml_summary_dict, tickets_summary_dict):

    """
    Establishes a relationship between invoices and tickets based on multiple comparison criteria,
    such as dates, pharmacies, purchase totals, product descriptions, and ticket numbers. The function
    iterates over each element of the XML summaries dictionary (invoices), applying a series of
    filters and comparisons to find the most similar corresponding tickets from
    the tickets summaries dictionary.

    The criteria are applied in the following order: purchase dates, pharmacy match,
    similarity of the total purchase, match in the product description, and finally,
    similarity in the ticket number. For cases where there are still multiple matching tickets
    after all the previous filters, it attempts to break the tie based on the
    highest similarity of the ticket number.

    Parameters:
    - xml_summary_dict (dict): Dictionary containing the summaries of XML invoices.
    - tickets_summary_dict (dict): Dictionary containing the summaries of the tickets.

    Returns:
    - final_result (dict): A dictionary that relates each invoice (key) with the most similar corresponding tickets (value).
      The value is a list of ticket keys that best match each invoice based on the established criteria.
    
    This process helps identify tickets that are potentially related to
    each invoice, facilitating transaction reconciliation and record verification.
    """
    
    A = xml_summary_dict

    B = tickets_summary_dict

    keys_A = list(A.keys()) # names of the ticket files

    len_A = len(keys_A) # length over which the values will be iterated

    final_result = {}


    for a in range(len_A):      

        B = tickets_summary_dict

        date_results = date_filter(A, B, a)       

        B = date_results[keys_A[a]]  # updates the dictionary to only include the tickets that match best 

        # List of pharmacies that have the longest common substring. Pharmacies with the longest length are kept
        pharmacy_test = find_max_consecutive_substring(A, B, a, "Farmacia")

        B = pharmacy_test[keys_A[a]]  # updates the dictionary to only include the tickets that match best 
        
        total_test = find_best_total(A, B, a)

        B = total_test[keys_A[a]]  # updates the dictionary to only include the tickets that match best 

        product_description_test = find_max_consecutive_substring(A, B, a, 'DescripcionProductos')

        B = product_description_test[keys_A[a]]

        if len(list(B.keys())) > 1:

            ticket_number_test = find_max_consecutive_substring(A, B, a, 'NUMTICKET')  

            B = ticket_number_test[keys_A[a]]

            if len(list(B.keys())) > 1:

                ticket_number_test_2 = highest_similarity(A, B, a, 'NUMTICKET')

                B = ticket_number_test_2[keys_A[a]]

        final_result[keys_A[a]] = list(B.keys())

    return final_result


if __name__ == "__main__":

    ##########################################################################################################################
    ################################################### L I B R A R I E S  ###################################################
    ##########################################################################################################################

    from datetime import datetime
    import json


    ##########################################################################################################################
    #####################################################  I N P U T S #######################################################
    ##########################################################################################################################


    dic_xml  = handle_dictionary("dic_xml.json", "r")

    dic_tickets = handle_dictionary("dic_tickets.json", "r")

    ############################################################################################################################################
    ####################################################### E X E C U T I O N  &  S A  V I N G   ###############################################
    ############################################################################################################################################

    dic_xml_tickets = relate_invoices_tickets(dic_xml, dic_tickets)

    handle_dictionary("dic_xml_tickets.json", "w", dic_xml_tickets )

