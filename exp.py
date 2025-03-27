import streamlit as st
import uuid
import sqlite3

# Database Connection
def sql_connect():
    return sqlite3.connect("contact_db.db", check_same_thread=False)

# Create Table
def setup_database():
    conn = sql_connect()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
                        contact_id TEXT PRIMARY KEY,
                        name TEXT,
                        phone_no TEXT,
                        address TEXT,
                        email_id TEXT)""")
    conn.commit()
    conn.close()

setup_database()

# Function to Create Contact
def create_contact(name, phone, address, email):
    contact_id = str(uuid.uuid4())
    conn = sql_connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?, ?)", 
                   (contact_id, name, phone, address, email))
    conn.commit()
    conn.close()
    st.success("Contact added successfully!")

# Function to View All Contacts
def view_contacts():
    conn = sql_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to Search Contact
def search_contact(contact_id):
    conn = sql_connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE contact_id = ?", (contact_id,))
    data = cursor.fetchone()
    conn.close()
    return data

# Function to Delete Contact
def delete_contact(contact_id):
    conn = sql_connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id = ?", (contact_id,))
    conn.commit()
    conn.close()
    st.warning("Contact deleted (if it existed).")

# Streamlit UI
st.title("📞 Contact Management System")

menu = st.sidebar.radio("Navigation", ["Add Contact", "View Contacts", "Search Contact", "Delete Contact"])

if menu == "Add Contact":
    st.subheader("Add New Contact")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")
    email = st.text_input("Email ID")
    if st.button("Save Contact"):
        create_contact(name, phone, address, email)

elif menu == "View Contacts":
    st.subheader("All Contacts")
    contacts = view_contacts()
    if contacts:
        st.table(contacts)
    else:
        st.info("No contacts found.")

elif menu == "Search Contact":
    st.subheader("Search Contact by ID")
    contact_id = st.text_input("Enter Contact ID")
    if st.button("Search"):
        contact = search_contact(contact_id)
        if contact:
            st.write(f"**Name:** {contact[1]}")
            st.write(f"**Phone:** {contact[2]}")
            st.write(f"**Address:** {contact[3]}")
            st.write(f"**Email:** {contact[4]}")
        else:
            st.error("Contact not found.")

elif menu == "Delete Contact":
    st.subheader("Delete Contact by ID")
    contact_id = st.text_input("Enter Contact ID")
    if st.button("Delete"):
        delete_contact(contact_id)
