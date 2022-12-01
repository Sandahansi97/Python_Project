import datetime as dt
from decimal import Decimal
import pandas as pd
from fpdf import FPDF

df = pd.read_csv("Trade.csv")
print(df)

# Count Trade and Extended Trade
Trade_count = 0
Ex_Trade_count = 0
for Row in df["Tag"]:
    if Row == "TRADE":
        Trade_count = Trade_count + 1
    if Row == "EXTRD":
        Ex_Trade_count = Ex_Trade_count + 1

# Print Trade Count and Ex Trade Count
print("Trades Count: ", Trade_count)
print("Extended Trades Count: ", Ex_Trade_count)

# Total Values Of Buy Trades and Sell Trades
Total_value_of_BUY_trades = 0
Total_value_of_SELL_trades = 0
i = 0
for row in df["Direction"]:
    if row == "B" or row == "BUY":
        Total_value_of_BUY_trades += Decimal(float(df["Price"][i])) * Decimal(float(df["Quantity"][i]))

    if row == "S" or row == "SELL":
        Total_value_of_SELL_trades += Decimal(float(df["Price"][i])) * Decimal(float(df["Quantity"][i]))
    i += 1

# Print Buy Trade Count and Sell Trade Count
print(round(Total_value_of_BUY_trades, 4))
print(round(Total_value_of_SELL_trades, 3))

# size of comment
length_of_comment = 0
longest_comment = str

for Row in df["Comment"]:
    print(Row)

    if len([Row]) > length_of_comment:
        length_of_comment = len(Row)
        longest_comment = Row

# get comment list
Comments_List = [str(i).strip() for i in df['Comment'].tolist()]
print(Comments_List)

Longest_Comment_Len = len(max(Comments_List, key=len))
print("Length Of Longest Comment : ", Longest_Comment_Len)

# Longest comment
Longest_comment = max(Comments_List, key=len)
print("Longest comment : ", Longest_comment)

# Trade interval
TempLast_Time = df["Trade Date and Time"][len(df) - 1]
TempFirst_Time = df["Trade Date and Time"][0]

Last_Time = dt.datetime(int(TempLast_Time[0:4]), int(TempLast_Time[5:7]), int(TempLast_Time[8:10]),
                        int(TempLast_Time[11:13]), int(TempLast_Time[14:16]), int(TempLast_Time[17:19]))
First_Time = dt.datetime(int(TempFirst_Time[0:4]), int(TempFirst_Time[5:7]), int(TempFirst_Time[8:10]),
                         int(TempFirst_Time[11:13]), int(TempFirst_Time[14:16]), int(TempFirst_Time[17:19]))
Trade_Interval = int((Last_Time - First_Time).total_seconds())
print("Trade_Interval : ", Trade_Interval)

Number_of_unique_firms: int = len((pd.concat([df["Buyer"], df["Seller"]])).unique())
print("Number Of Unique Firms : ", Number_of_unique_firms)

Unique_firm_IDs = "|".join(pd.concat([df["Buyer"], df["Seller"]]).unique())
print("Unique firm IDs : ", Unique_firm_IDs)

# add total values into list
id_list = []
id_list_new = []

i = 0
for ID in df["ItemID"]:
    if ID in id_list:
        previous_value = id_list[id_list.index(ID)-1]
        new_value = round(previous_value + (df["Price"][i] * df["Quantity"][i]), 4)
        id_list.insert(id_list.index(ID)-1, new_value)
        id_list.pop(id_list.index(ID) - 1)
    else:
        id_list.append(df["Price"][i] * df["Quantity"][i])
        id_list.append(ID)
    i += 1

i = 0;
while i < len(id_list):
    tmp_tup = id_list[i], id_list[i+1]
    id_list_new.append(tmp_tup)
    i += 2

# Sort values
id_list_new.sort()
print(id_list_new)

# FPDF2
pdf = FPDF()
pdf.set_font("Courier", size=12)
pdf.add_page()

col_width = pdf.w / 4.5
row_height = pdf.font_size * 2
header_height = row_height * 2
header_width = pdf.w / 2
row_space = row_height * 1.5

# Summary to PDF
pdf.cell(header_width, header_height, "Summary Of Trade ", ln=row_space)
pdf.cell(col_width, row_height, "Num of Trades: " + str(Trade_count), ln=row_space)
pdf.cell(col_width, row_height, "Num of Ex-trade: " + str(Ex_Trade_count), ln=row_space)
pdf.cell(col_width, row_height, "Total Buy values: " + str(round(Total_value_of_BUY_trades, 4)), ln=row_space)
pdf.cell(col_width, row_height, "Total Sell values: " + str(round(Total_value_of_SELL_trades, 3)), ln=row_space)
pdf.cell(col_width, row_height, "Length of the longest comment: " + str(Longest_Comment_Len), ln=row_space)
pdf.cell(col_width, row_height, "Longest Comment: " + str(Longest_comment), ln=row_space)
pdf.cell(col_width, row_height, "Trade Interval: " + str(Trade_Interval), ln=row_space)

# Firms to PDF
pdf.ln(row_height)
pdf.cell(header_width, header_height, "List of Firms ", ln=row_space)
pdf.cell(col_width, row_height, "Number of unique firms: " + str(Number_of_unique_firms), ln=row_space)
pdf.cell(col_width, row_height, "Unique firm IDs: " + str(Unique_firm_IDs), ln=row_space)

# Item ids with Total value- ASC Order to pdf
pdf.ln(row_height)
pdf.cell(header_width, header_height, "Item Ids ", ln=row_space)
pdf.cell(col_width, row_height, "(Total Value , Item ID ) ", ln=row_space)
for val in id_list_new:
    pdf.cell(col_width, row_height, str(val), ln=row_space)

pdf.output("FinalOutput.pdf")
