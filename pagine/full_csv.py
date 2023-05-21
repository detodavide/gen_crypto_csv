import streamlit as st
import os
import pandas as pd
import joblib
from io import BytesIO

from utils.cache_convert import convert_df

def main(df=None):

        # Download buttons
        csv = convert_df(df)
        filename = "filename"

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{filename}.csv',
            mime='text/csv',
        )

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            # Close the Pandas Excel writer and output the Excel file to the buffer
            writer.save()

            download2 = st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name=f'{filename}.xlsx',
                mime='application/vnd.ms-excel'
            )

if __name__=="__main__":
    main()