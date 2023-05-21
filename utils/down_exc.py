from io import BytesIO
import base64
import pandas as pd

def download_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False)
    writer.save()
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    href = f'<a href="data:application/vnd.ms-excel;base64,{b64}" download="predicted_profit.xlsx">Download Excel</a>'
    return href
