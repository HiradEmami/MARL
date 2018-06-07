import pandas as pd

# Some sample data to plot.
list_data = [30, 40, 50, 40, 20, 10, 5]

# Create a Pandas dataframe from the data.
df = pd.DataFrame(list_data)

# Create a Pandas Excel writer using XlsxWriter as the engine.
excel_file = 'testfile.xlsx'
sheet_name = 'Sheet1'

writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
df.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
# This is equivalent to the following using XlsxWriter on its own:
#
#    workbook = xlsxwriter.Workbook('filename.xlsx')
#    worksheet = workbook.add_worksheet()
#
workbook = writer.book
worksheet = writer.sheets[sheet_name]

# Apply a conditional format to the cell range.
worksheet.conditional_format('B2:B8', {'type': '5_color_scale'})

# Close the Pandas Excel writer and output the Excel file.
writer.save()