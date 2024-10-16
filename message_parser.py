from datetime import datetime
import re
from gsheet import update_multiple_values
from chat import click_read_more
import time


cons_id = "1FYEs3hyJppB79oPxQnKVksoKejFQ-0M9-bC0yLqGP_c" # Consolidated Test ID 
veg_id = "1hWaUquZDw2eMABKm52jXJ_P2qfF3Cxteiyyjysvxe_o" # Vegetable Sale Test ID



'''This python file contains functions for parsing''' 

# Function to get the current date in ddmmyy format
def current_time():
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year%100
    format_date = f"{day:02d}{month:02d}{year:02d}"
    return format_date

def parseVegetablePurchase(message):
    
    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%B-%Y")
    else:
        formatted_date = None

    # Extract the vegetable information
    vegetables = re.findall(r'Vegetable\s*:\s*(\w+)\s*'
                            r'Purchase_qty\s*:\s*(\d+)\s*'
                            r'Purchase_rate\s*:\s*(\d+)\s*'
                            r'Purchase_type\s*:\s*(\w+)', message)

    # Create the list of lists
    result = [[formatted_date, veg, int(qty), int(rate), int(qty) * int(rate), p_type] for veg, qty, rate, p_type in vegetables]
    
    return result

def parseVegetableSold(message):
# Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%B-%y")
    else:
        formatted_date = None

    # Modify the pattern to handle the purchase lines before sold_qty
    solds = re.findall(r'Vegetable\s*:\s*(\w+)?\s*'
                       r'Purchase_qty\s*:\s*(\d+)?\s*'
                       r'Purchase_rate\s*:\s*(\d+)?\s*'
                       r'Purchase_type\s*:\s*(\w+)?\s*'
                       r'Purchase_location\s*:\s*([\w\s]+)?\s*'  # Purchase location can have spaces
                       r'Sold_qty\s*:\s*(\d*)\s*'
                       r'Sold_rate\s*:\s*(\d*)\s*'
                       r'Sold_location\s*:\s*([\w\s]*)\s*'
                       r'Customer\s*:\s*([\w\s\-]*)\s*'
                       r'Customer_type\s*:\s*(\w*)', message)

    # Create the result list for sold data
    sold_data = []
    for veg, p_qty, p_rate, p_type, p_loc, s_qty, s_rate, s_loc, c_name, c_type in solds:
        if veg and p_rate and p_type and s_qty and s_rate and s_loc and c_name and c_type:
            sold_data.append([formatted_date,
                              veg,  # Set to empty string if None
                              s_qty, 
                              s_rate, 
                              (int(s_qty) * int(s_rate)),  # Calculate only if both are present
                              s_loc.strip(),  # Use strip() only if it's not None
                              c_name.strip(),
                              c_type, 
                              "-",  # This remains static
                              p_rate, 
                              p_type])

    return sold_data

def parseVegetablePurchasevsSold(message):
    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%B-%Y")
    else:
        formatted_date = None
    
    # Find all vegetables purchased and sold
    pvs = re.findall(r'Vegetable\s*:\s*(\w+)\s*'
                     r'Purchase_qty\s*:\s*(\d+)\s*'
                     r'Purchase_rate\s*:\s*(\d+)\s*'
                     r'Purchase_type\s*:\s*(\w+)\s*'
                     r'Purchase_location\s*:\s*(\w+)\s*'
                     r'Sold_qty\s*:\s*(\d+)\s*'
                     r'Sold_rate\s*:\s*(\d+)\s*'
                     r'Sold_location\s*:\s*(\w+)',message)
    
    # p_xxx is for purchase related, s_xxx is for sold related
    result = [[formatted_date, veg, int(p_qty), int(p_rate), int(p_qty) * int(p_rate), p_type, p_loc, int(s_qty), int(s_rate), int (s_qty) * int(s_rate), s_loc] for veg, p_qty, p_rate, p_type, p_loc, s_qty, s_rate, s_loc in pvs]

    return result

'''AMRITGRAM_EVMilk060924
    Last 6 digits are date in ddmmyy format''' 
def parseVegetableMilk(message):
    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%B-%y")
    else:
        formatted_date = None
    
    milk_data = []

    data = re.findall(r'Farmer\s*:\s*(\w+)?\s*'
                      r'Purchase_qty\s*:\s*(\w+)?\s*'
                      r'Purchase_rate\s*:\s*(\w+)?\s*'
                      r'Sold_qty\s*:\s*(\d+)\s*'
                      r'Sold_rate\s*:\s*(\d+)\s*'
                      r'Customer\s*:\s*(\w+)', message)
    
    for f_name, p_qty, p_rate, s_qty, s_rate, c_name in data:
        if f_name and p_qty and p_rate:
            milk_data.append([formatted_date,
                              p_qty,
                              p_rate,
                              int(p_qty) * int(p_rate),
                              "Farmer : " + f_name,
                              s_qty,
                              s_rate,
                              int(s_rate) * int(s_qty),
                              c_name])
        else:
            milk_data.append([formatted_date,
                              "",
                              "",
                              "",
                              "",
                              s_qty,
                              s_rate,
                              int(s_rate) * int(s_qty),
                              c_name])

    return milk_data


'''@AMRITGRAM_Vegetable130924'''
# Function for AMRITGRAM Vegetable Scraping
def parseVegetableMessages(driver, messages):
    for message in messages:
        temp_message = message.text
        # if(temp_message[:26] == ("@AMRITGRAM_Vegetable" + current_time())):
        if(temp_message[:26] == ("@AMRITGRAM_Vegetable" + "111024")):
            click_read_more(driver, message)
            temp_message = message.text
            time.sleep(2)
            purchase = parseVegetablePurchase(temp_message)
            print(purchase)
            print('\n')
            sold = parseVegetableSold(temp_message)
            print(sold)
            print('\n')
            pvs = parseVegetablePurchasevsSold(temp_message)
            print(pvs)
            print('\n')
            update_multiple_values(purchase, "Purchase")
            time.sleep(2)
            update_multiple_values(sold, "Sold")
            time.sleep(2)
            update_multiple_values(pvs, "Purchase vs Sold")
        elif(temp_message[:23] == ("@AMRITGRAM_EVMilk" + current_time())):
            click_read_more(driver, message)
            temp_message = message.text
            time.sleep(2)
            milk = parseVegetableMilk(temp_message)
            print(milk)
            print('\n')
            update_multiple_values(milk, "EV A2 Milk Sale")


''' @AMRITGRAM_Consolidated071024 '''
def parseConsolidated(message):

    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%b-%y")
    else: 
        formatted_date = None

    cons = re.findall(r'Vegetable\s*:\s*(.+?)\s*'
                      r'Farmer\s*:\s*([\w\s]+)\s*'
                      r'Type\s*:\s*(\w+)\s*'
                      r'Tr_Type\s*:\s*([\w\s]+)\s*'
                      r'Client\s*:\s*(\w+)\s*'
                      r'Qty\s*:\s*(\d+(?:\.\d+)?)\s*'
                      r'Price_Org\s*:\s*(\d+(?:\.\d+)?)\s*'
                      r'Price_M\s*:\s*(\d+(?:\.\d+)?)', message)
    
    cons_data = []

    for veg, f_name, type, t_type, c_name, qty, price_o, price_m in cons:
        cons_data.append([
            formatted_date,
            veg,
            f_name.strip(),  # Removes leading/trailing spaces from farmer's name
            "Organic" if type.lower() == "o" else "Inorganic",
            "Market B2B" if t_type.strip().lower() == "m b2b" else 
            "Organic B2B" if t_type.strip().lower() == "o b2b" else "Organic B2C",
            "Kalamna Market" if c_name.lower().strip() == "km" else 
            "EV Sales Kalamna B2C" if c_name.lower().strip() == "ev" else
            "Yuktahaar" if c_name.lower().strip() == "y" else "Invalid Code",
            float(qty),
            float(price_o),
            "",
            float(price_m),
            float(qty) * float(price_o),
            "",
            ""
        ])

    return cons_data

''' @AMRITGRAM_EVAPMC071024 '''
def parseEVAPMC(message):
    
    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%b-%y")
    else:
        formatted_date = None

    # Extract commodity information
    ev = re.findall(r'Commodity\s*:\s*([\w\s]+)\s*'
                    r'Sold_qty\s*:\s*(\d+(?:\.\d+)?)\s*'
                    r'Sold_rate\s*:\s*(\d+(?:\.\d+)?)\s*'
                    r'M_rate\s*:\s*(\d+(?:\.\d+)?)', message)

    ev_data = []

    for comm, s_qty, s_rate, m_rate in ev:
        # Convert the values to floats for decimal support
        s_qty = float(s_qty)
        s_rate = float(s_rate)
        m_rate = float(m_rate)

        # Calculate totals and profit, rounded to 2 decimal places
        total_sold = round(s_qty * s_rate, 2)
        total_mrate = round(s_qty * m_rate, 2)
        profit_amount = round(s_qty * (s_rate - m_rate), 2)
        profit_percentage = round((profit_amount / total_mrate) * 100, 2)

        ev_data.append([
            formatted_date,
            comm.strip(),
            round(s_qty, 2),
            round(s_rate, 2),
            round(m_rate, 2),
            total_sold,      # Total Sold Amount
            total_mrate,     # Total M Rate Amount
            profit_amount,   # Profit Amount
            profit_percentage # Profit Percentage
        ])

    return ev_data


def parseOrganicMessages(driver, messages):
    for message in messages:
        temp_message = message.text.strip()
        if(temp_message[:29] == ("@AMRITGRAM_Consolidated" + current_time())):
        # if(temp_message[:29] == ("@AMRITGRAM_Consolidated111024")):
            click_read_more(driver, message)
            temp_message = message.text
            time.sleep(2)
            cons = parseConsolidated(temp_message)
            print(cons)
            print('\n')
            update_multiple_values(cons, "Consolidated", True)
        elif(temp_message[:23] == ("@AMRITGRAM_EVAPMC" + current_time())):
            click_read_more(driver, message)
            temp_message = message.text
            time.sleep(2)
            evapmc = parseEVAPMC(temp_message)
            print(evapmc)
            print('\n')
            update_multiple_values(evapmc, "EV APMC Veggies & A2 Milk Sale", False)
