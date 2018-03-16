# Feed the Family! #

This project is meant to be used for meal planning, grocery budgeting, and shopping lists.

## Tech ##

Built using:
  - Python 3.6
  - npm 5.7
  - node 8.10
  - vue 2.9

Python3 venv used because I like the separation it provides.

IPython used for flask shell via flask-shell-ipython package.

### Dependencies ###

```bash
# From root of app
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip # If you want to, I usually do.
pip install -r requirements.txt

# From root of app
cd frontend
npm install
```

### Starting the applications ###

*Terminal 1*
```bash
cd backend
source venv/bin/activate
export FLASK_APP=groceries.py
export FLASK_DEBUG=1
flask run
```

*Terminal 2*
```bash
cd frontend
npm run dev
```
