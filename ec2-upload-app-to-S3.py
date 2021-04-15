import pandas as pd
import yfinance as yf
import streamlit as st
import boto3

st.write("""
        # Simple Stock Price App

        Shown are the stock **closing price** and ***volume*** of Google!

        """)

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GOOGL'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')
# Open  High    Low Close   Volume  Dividends   Stock Splits

st.write("""
        ## Closing Price
        """)
st.line_chart(tickerDf.Close)
st.write("""
        ## Volume Price
        """)
st.line_chart(tickerDf.Volume)

STYLE = """
<style>
img {
    max-width: 100%;

}
</style>
"""

def main():

    st.info(__doc__)
    st.markdown(STYLE, unsafe_allow_html=True)

    newfile = st.file_uploader("Upload file", type="csv")
    show_file = st.empty()

    if not newfile:
        show_file.info("Please upload a file of type: " + ", ".join(["csv"]))
        return

    upload_files(newfile)

    data = pd.read_csv(newfile)
    st.dataframe(data.head(10))

def upload_files(newfile):
    s3 = boto3.resource('s3')
    bucket = 'machinelearningupload'
    #bucket = s3.Bucket('gregsupload')
    file_details = newfile.name
    content = newfile.getvalue()

    s3.Bucket(bucket).put_object(Key=file_details, Body=content)

    print(file_details, "Uploaded Successfully to S3 Bucket:", bucket)
    return True

main()
