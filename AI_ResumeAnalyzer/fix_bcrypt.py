import os

with open("backend/app/api/routes.py", "r") as f:
    content = f.read()

# Replace passlib CryptContext
content = content.replace("from passlib.context import CryptContext", "import bcrypt")

content = content.replace('pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")', "")

content = content.replace("pwd_context.hash(user.password)", "bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')")
content = content.replace("pwd_context.hash(updates[\"password\"])", "bcrypt.hashpw(updates[\"password\"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')")

content = content.replace("not pwd_context.verify(form_data.password, user.hashed_password)", "not bcrypt.checkpw(form_data.password.encode('utf-8'), user.hashed_password.encode('utf-8'))")

with open("backend/app/api/routes.py", "w") as f:
    f.write(content)
