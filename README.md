# IRE mini-bootcamp: Web scraping with Python (2023)
Materials for a Dec. 2023 mini bootcamp on web scraping with Python.

## Setting up
1. If you haven't already, [follow our guide to install Python on your computer](https://docs.google.com/document/d/1cYmpfZEZ8r-09Q6Go917cKVcQk_d0P61gm0q8DAdIdg/edit).
2. [Download and unzip the class materials onto your desktop](https://github.com/ireapps/python-mini-bootcamp-scraping-2023/archive/refs/heads/main.zip). (Unzipping instructions: If you're on a PC, right-click on the file and choose "Extract all." Mac users, double-click the file.)
3. Open your computer's command-line interface -- _cmd_ on a PC, _Terminal_ on a Mac -- and _cd_ into the folder that you just unzipped. If you unzipped it onto your desktop, the command to get there would be something like `cd Desktop/python-mini-bootcamp-scraping-2023`. Then try `ls` (or `dir` on a PC) to list the files and ensure that you're in the right place.
4. Create a virtual environment:
- PC: `python -m venv env`
- Mac: `python3 -m venv env`
5. Activate the virtual environment:
- PC: `.\env\Scripts\activate`
- Mac: `source env/bin/activate`
6. Verify that you're in the activated virtual environment -- you should see `(env)` prepended to the command prompt -- then install the Python dependencies: `pip install -r requirements.txt`.
7. Install the Playwright browsers: `playwright install`