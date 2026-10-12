with open("backend/app/api/routes.py", "r") as f:
    content = f.read()

content = content.replace("f\"Error processing resume: {str(e)}\n{traceback.format_exc()}\"", "f\"Error processing resume: {str(e)}\\n{traceback.format_exc()}\"")
with open("backend/app/api/routes.py", "w") as f:
    f.write(content)
