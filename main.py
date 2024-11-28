import pymongo
from pymongo import MongoClient
import streamlit as st
import pandas as pd

# Conectarea la MongoDB
client = MongoClient('mongodb://localhost:27017/')

databases = client.list_database_names()
print("Baze de date disponibile:", databases)

db = client['Recommandation-SystemDB']  # selectam baza de date necesara
print("Baza de date selectată:", db.name)

#verificam colectiile disponibile
collections = db.list_collections()
print("Colecții disponibile:", [col["name"] for col in collections])

# accesam colectia 'Users'
collection = db['Users']
document_count = collection.count_documents({})
print("Numărul de documente din colecția 'Users':", document_count)

# CRUD

# adăugarea unui utilizator
st.title("Adăugare Utilizator")

preference_options = [
    'Historical', 'Beach', 'City', 'Nature', 'Adventure', 'Monument',
    'Cultural', 'Ancient Ruins', 'Other', 'Religious Site', 'Volcano',
    'Market', 'Museum', 'Point of Interest', 'Caves', 'Water Park', 'Spa',
    'Natural Attraction', 'Mountain', 'Lake', 'Island', 'Castle',
    'Hotel', 'Scenic Drive', 'Architectural', 'Palace'
]

user_name = st.text_input("Numele Utilizatorului")
user_email = st.text_input("Email")
user_gender = st.selectbox("Gen", ["Masculin", "Feminin"])
user_num_adults = st.number_input("Număr Adulți", min_value=1)
user_num_children = st.number_input("Număr Copii", min_value=0)
user_preferences = st.multiselect("Preferințe (select one or more)", preference_options)


if st.button("Adaugă Utilizator"):
    new_user = {
        "Name": user_name,
        "Email": user_email,
        "Preferences": user_preferences,
        "Gender": user_gender,
        "NumberOfAdults": user_num_adults,
        "NumberOfChildren": user_num_children
    }

    collection.insert_one(new_user)
    st.success(f"Utilizatorul {user_name} a fost adăugat cu succes!")


# afisare utilizartori
st.title("Vizualizare Utilizatori")

num_users_to_display = st.selectbox("Selectează numărul de utilizatori de afișat", [10, 20, 30, 50, 100, 200], index=1)

users_cursor = collection.find().limit(num_users_to_display)

users_list = list(users_cursor)
if users_list:
    df = pd.DataFrame(users_list)
    df = df[["Name", "Email", "Preferences", "Gender", "NumberOfAdults", "NumberOfChildren"]]
    st.dataframe(df)
else:
    st.write("Nu există utilizatori în baza de date.")


# Actualizarea unui utilizator
st.title("Actualizare Utilizator")

user_id = st.text_input("UserID Utilizator pentru actualizare")

if user_id:
    user = collection.find_one({"UserID": int(user_id)})
    if user:
        st.write(f"User Found: {user['Name']}")

        new_name = st.text_input("Nume nou", value=user['Name'])
        new_email = st.text_input("Email nou", value=user['Email'])
        new_preferences = st.text_input("Preferințe noi", value=user['Preferences'])

        if st.button("Actualizează"):
            collection.update_one(
                {"UserID": int(user_id)},
                {"$set": {"Name": new_name, "Email": new_email, "Preferences": new_preferences}}
            )
            st.success(f"Utilizatorul {new_name} a fost actualizat cu succes!")
    else:
        st.error("Utilizatorul nu a fost găsit.")


# Ștergerea unui utilizator
st.title("Ștergere Utilizator")

user_id_to_delete = st.text_input("UserID Utilizator pentru ștergere")

if user_id_to_delete:
    user_to_delete = collection.find_one({"UserID": int(user_id_to_delete)})
    if user_to_delete:
        st.write(f"User Found: {user_to_delete['Name']}")

        if st.button("Șterge Utilizator"):
            collection.delete_one({"UserID": int(user_id_to_delete)})
            st.success(f"Utilizatorul {user_to_delete['Name']} a fost șters cu succes!")
    else:
        st.error("Utilizatorul nu a fost găsit.")

