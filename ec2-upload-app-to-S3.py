import pandas as pd
import streamlit as st
import boto3

st.write("""
        # Upload file to S3

        """)

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

    content = newfile.getvalue()
    upload_files(newfile)

    data = pd.read_csv(newfile)
    st.dataframe(data.head(10))

def upload_files(newfile):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('<S3 BUCKET NAME>')
    content = newfile.getvalue()

    s3.Bucket('<S3 BUCKET NAME>').put_object(Key='<OBJECT NAME>', Body=content)

    print("Upload Successful")
    return True

main()
