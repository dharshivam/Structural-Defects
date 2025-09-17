import google.generativeai as genai
import streamlit as st
import datetime as dt
import pandas as pd     
from PIL import Image
import os

key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

st.sidebar.title(":red[UPLOAD YOUR IMAGE HERE]")

uploaded_image = st.sidebar.file_uploader("Here",type=["png","jpg","jpeg"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.subheader(":green[***UPLOADED IMAGE***]")
    st.sidebar.image(image)


#Create main page
st.title(":blue[STRUCTURAL DEFECTS DETECTION] : :orange[***AI assistant structural defects detection***]")   
tips = ''' To use the application follow the steps below:

* Upload an image of a structural defect using the sidebar on the left.
* Click on the button to generate summary
* Click download  to save the report generated'''
st.write(tips)

rep_title = st.text_input(" :green[Report Title :]",None)
prep_by = st.text_input(" :green[Report Prepared By :]",None)
prep_for = st.text_input(" :green[Report Prepared For :]",None)
date = st.date_input(" :green[Date :]", None)

prompt = f'''
Assume you are a structural engineer.The user has provided an image of a structural defects in the image
and generate a report. The report should include the following:


* It should start with the title,prepared by and prepared for details.Provided by the user.
* Use {rep_title} at title, {prep_by} as prepared by,{prep_for} as prepared for the same.
* also mention the current date from {dt.datetime.now().date()}.

* Identify the type of structural defect for eg. honeycomb, voids, cracks  , corrosion , spalling etc
* There could be multiple defects in the image. Identify all the defects seperately.
* For each defect identified provide a brief description of the defect and its potential impact on the structure.
* For each measure the severity of the defect as low , medium or high also mention 
  if the defect is inevitable or avoidable.
* Also mention the time before this defect leads to permanent damage to the structure.
* Also give how much time it will take to repair the defect.
* Provide a short term and long term solution to repair the defect along with estimated cost of repair in Rs.
* What precautionary measures can be taken to prevent such defects in future.
* The report generated should be in word format.
* Show the data in bullet points and tabular format wherever possible.
* Make sure that the report does not exceed 3 pages.

'''
if st.button("Generate Report"):
    if uploaded_image is None:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Generating report..."):
            response = model.generate_content([prompt , image],generation_config={'temperature':0.9})
            st.write(response.text)
            st.success("Report generated successfully!")
            

 #download button
 # Create a download button for the report
 # Convert the report text to a downloadable format (e.g., .txt or .docx , pdf)

        st.download_button(
    label="Download Report",
    data=response.text,
    file_name="structural_defect_report.txt",
    mime="text/plain")
    
        st.success("Thank you for using the Structural Defects Detection App!")