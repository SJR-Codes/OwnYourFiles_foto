"""
* Own Your Files - Photos 26.01.2023
* main.py
* description
* MIT License
* Copyright (c) 2023 SJR-Codes / Samu Reinikainen / samu.reinikainen@gmail.com
"""

# run blocks of code only if our program is the main program executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", log_level="info", reload="auto")
    #uvicorn.run("main:app")