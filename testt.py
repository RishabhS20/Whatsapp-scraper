from datetime import datetime
import re

msg ="""
@AMRITGRAM_Consolidated111024

Date = 30/9/24

Vegetable : Ridge Gourd 
Farmer : Yogesh Lodhe 
Type : O
Tr_Type : O B2C
Client : EV
Qty : 7.5
Price_Org : 45.5
Price_M : 20.5

Vegetable : Ridge Gourd 
Farmer : Yogesh Lodhe 
Type : O
Tr_Type : M B2B
Client : KM
Qty : 2
Price_Org : 20
Price_M : 20

Vegetable : Bottle Gourd 
Farmer : Yogesh Lodhe 
Type : O
Tr_Type : O B2C 
Client : EV 
Qty : 1 
Price_Org : 30
Price_M : 15

"""



emsg = """
@AMRITGRAM_EVAPMC071024

Date = 6/9/24

Commodity : Turai 
Sold_qty : 12
Sold_rate : 12
M_rate : 14

Commodity : Beans 
Sold_qty : 12
Sold_rate : 32
M_rate : 22

Commodity : Paneer Paneer 
Sold_qty : 2
Sold_rate : 45
M_rate : 35

Commodity : Lauki 
Sold_qty : 1.5
Sold_rate : 50
M_rate : 25

Commodity : Tikka 
Sold_qty : 10.5
Sold_rate : 50
M_rate : 35

"""


def parseEVAPMC(message):
    
    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%B-%y")
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


def parseConsolidated(message):

    # Extract the date
    date_match = re.search(r'Date\s*=\s*(\d{1,2}/\d{1,2}/\d{2,4})', message)
    if date_match:
        # Parse and format the date
        raw_date = date_match.group(1)
        parsed_date = datetime.strptime(raw_date, "%d/%m/%y")
        formatted_date = parsed_date.strftime("%#d-%b -%y")
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
            "Kalamana Market" if c_name.lower().strip() == "km" else 
            "EV Sales Kalamana B2C" if c_name.lower().strip() == "ev" else
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


# temp = parseEVAPMC(emsg)
temp = parseConsolidated(msg)
print(temp)

    
