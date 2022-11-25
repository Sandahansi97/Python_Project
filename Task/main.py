import datetime as dt
from decimal import Decimal
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

df = pd.read_csv("Trade.csv")
print(df)

# Count Trade and Extended Trade
Trade_count = 0
Ex_Trade_count = 0
for Row in df["Tag"]:
    if(Row == "TRADE"):
        Trade_count = Trade_count + 1
    if(Row == "EXTRD"):
        Ex_Trade_count = Ex_Trade_count + 1


# Print Trade Count and Ex Trade Count
print("Trades Count: ", Trade_count)
print("Extended Trades Count: ", Ex_Trade_count)


# Total Values Of Buy Trades and Sell Trades
Total_value_of_BUY_trades = 0
Total_value_of_SELL_trades = 0
i=0
for row in df["Direction"]:
    if (row == "B" or row == "BUY"):
        Total_value_of_BUY_trades += Decimal(float(df["Price"][i])) * Decimal(float(df["Quantity"][i]))

    if (row == "S" or row == "SELL"):
        Total_value_of_SELL_trades += Decimal(float(df["Price"][i])) * Decimal(float(df["Quantity"][i]))
i+=1

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
comments_list = [str(i).strip() for i in df['Comment'].tolist()]
print(comments_list)
Length_of_longest_comment = len(max(comments_list, key=len))
print("Length of longest comment : ", Length_of_longest_comment)


# Longest comment
Longest_comment = max(comments_list, key=len)
print("Longest comment : ", Longest_comment)

# Trade interval
TempLast_Time = df["Trade Date and Time"][len(df)-1]
TempFirst_Time = df["Trade Date and Time"][0]

Last_Time = dt.datetime(int(TempLast_Time[0:4]), int(TempLast_Time[5:7]), int(TempLast_Time[8:10]), int(TempLast_Time[11:13]), int(TempLast_Time[14:16]), int(TempLast_Time[17:19]))
First_Time = dt.datetime(int(TempFirst_Time[0:4]), int(TempFirst_Time[5:7]), int(TempFirst_Time[8:10]), int(TempFirst_Time[11:13]), int(TempFirst_Time[14:16]), int(TempFirst_Time[17:19]))
Trade_Interval = int((Last_Time-First_Time).total_seconds())
print("Trade_Interval : ", Trade_Interval)

Number_of_unique_firms: int = len((pd.concat([df["Buyer"], df["Seller"]])).unique())

print("Number of unique firms : ", Number_of_unique_firms)

Unique_firm_IDs = "|".join(pd.concat([df["Buyer"], df["Seller"]]).unique())
print("Unique firm IDs : ", Unique_firm_IDs)

Item_ID_List = ((df["ItemID"]).unique().tolist())
Item_ID_List.sort()
Item_ID = "|".join(Item_ID_List)
print("Item_ID :", Item_ID)

# Total value per item ID
df["total_value"] = df["Price"]*df["Quantity"]
df1 = df[["ItemID", "total_value"]].groupby("ItemID").sum()
df1 = df1.reset_index()
print(df1)

# Convert into data frames
# Summary
Summary = pd.DataFrame({"Number_of_trades": [Trade_count], "Number_of_extended_trades": [Ex_Trade_count], "Total_value_of_BUY_trades": [Total_value_of_BUY_trades], "Total_value_of_SELL_trades": [Total_value_of_SELL_trades]
, "Length_of_the_longest_comment": [Length_of_longest_comment], "Longest_comment": [Longest_comment], "Trade_interval": [Trade_Interval]}).transpose().reset_index()
Summary.columns = ("Field_name", "Value")
print(Summary)

# List of Firms
List_of_Firms = pd.DataFrame({"Number of unique firms": [Number_of_unique_firms], "Unique firm IDs": [Unique_firm_IDs]}).transpose().reset_index()
List_of_Firms.columns = ("Field_name", "Value")
print(List_of_Firms)

# Totals per Item ID
Totals_per_Item_ID = df1

# Convert to PDF
# Summary PDF
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
Summary_table = ax.table(cellText=Summary.values, colLabels=Summary.columns, loc="upper center")
pp = PdfPages("List_Of_Summary.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()

# List of Firms PDF
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
Firms_table = ax.table(cellText=List_of_Firms.values, colLabels=List_of_Firms.columns, loc="upper center")
pp = PdfPages("List_Of_Firms.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()

# Totals per Item ID
fig, ax = plt.subplots(figsize=(15, 20))
ax.axis('tight')
ax.axis('off')
ItemID_table = ax.table(cellText=Totals_per_Item_ID.values, colLabels=Totals_per_Item_ID.columns, loc="upper center")
pp = PdfPages("List_Of_ItemID.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
