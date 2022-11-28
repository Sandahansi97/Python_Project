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
print(Total_value_of_BUY_trades)
print(Total_value_of_SELL_trades)

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
i = 0
for ID in df["ItemID"]:
    id_list_new = df["Price"][i] * df["Quantity"][i], ID
    id_list.append(id_list_new)
    i += 1

#   Sort values
id_list.sort()

# FPDF2
pdf = FPDF()
pdf.set_font("Arial", size=12)
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
pdf.cell(col_width, row_height, "Total Buy values: " + str(Total_value_of_BUY_trades), ln=row_space)
pdf.cell(col_width, row_height, "Total Sell values: " + str(Total_value_of_SELL_trades), ln=row_space)
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
for val in id_list:
    pdf.cell(col_width, row_height, str(val), ln=row_space)

pdf.output("FinalOutput.pdf")
