from pydoc import doc

import streamlit as st
import pymongo
import certifi


@st.experimental_singleton
def init_connection():
    connection = "mongodb+srv://McCrackenDB:"
    connection += st.secrets["mongo"]["password"]
    connection += "@mccracken.aa00r.mongodb.net/?retryWrites=true&w=majority"

    return pymongo.MongoClient(connection, tlsCAFile=certifi.where())


client = init_connection()


@st.experimental_memo(ttl=600)
def get_start():
    start = {}
    data = client.Portfolio

    start["greeting"] = data.Static.find_one({'title': 'greeting'})["text"]
    start["name"] = data.Static.find_one({'title': 'name'})["text"]
    start["bio"] = data.Static.find_one({'title': 'bio'})["text"]
    start["introduction"] = data.Static.find_one(
        {'title': 'introduction'})["text"]

    return start


@st.experimental_memo(ttl=600)
def get_data(collection):
    return list(client.Portfolio[collection].find())


start = get_start()
work = get_data("Work")
education = get_data("Education")

with st.container():
    st.subheader(start["greeting"])
    st.title(start["name"])
    st.caption(start["bio"])

with st.container():
    st.write(start["introduction"])
    st.write("##")

    column1, column2 = st.columns((1, 2))

    with column1:
        st.write("Not a lot of time?")

    with column2:
        with open("assets/files/resume.pdf", "rb") as file:
            st.download_button(
                label="HERE IS MY RESUME",
                data=file,
                file_name="RalphMcCrackenIII.pdf",
                mime="pdf"
            )

    st.write("---")

with st.container():
    options = st.multiselect(
        label="What would you like to know about me?",
        options=["WORK", "EDUCATION", "CERTIFICATIONS", "AWARDS", "PROJECTS",
                 "FAMILY", "FAVORITE QUOTES", "FAVORITE BIBLE VERSES", "AUDIO", "TESTIMONIES"]
    )

    for option in options:
        if option == "WORK":
            st.header("WORK EXPERIENCE")
            st.write("##")

            for job in work:
                st.subheader(job["title"])
                st.write(
                    job["company"],
                    "|",
                    job['startDate'],
                    " - ", job["endDate"]
                )
                st.caption(job["location"])

        elif option == "EDUCATION":
            st.header("EDUCATION HISTORY")
            st.write("##")

            for degree in education:
                left, right = st.columns((1, 2))

                with left:
                    st.image(image=degree["diplomaImageUrl"])

                with right:
                    st.subheader(degree["degree"])
                    st.write(degree["description"])
                    st.write("GPA:", degree["gpa"])
                    st.write("##")
                    st.write(degree["institute"])
                    st.caption("Class of " + degree["classOfYear"])

        st.write("---")
