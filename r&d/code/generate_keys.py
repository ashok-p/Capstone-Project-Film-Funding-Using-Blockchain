import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker","rmiller"]
passwords = ["abc123", "def456"] 
#after creating the pickle file, remove the text passwords

##CREATE A FUNCTION AND CALL IT IN MAIN APP.PY FILE
## save the login key id and film invested, date etc. 
# USE THE SAME DATA here to retrieve and award

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(_file_).parent / "hased_pwd.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)