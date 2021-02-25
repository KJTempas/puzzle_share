# Puzzle Share

### An app to share jigsaw puzzles with friends and neighbors
Add new puzzles(name, # of pieces, mfg company, owner, picture), see what puzzles are available, checkout and return puzzles.
### To install
#### Virtual Environment
Create and activate a virtual environment. Use Python3 as the interpreter. Suggest locating the venv/ directory outside of the code directory

Mac Version:
python3 -m venv env
source env/bin/activate

Windows Version:
python -m venv env
env\Scripts\activate

#### Install required modules
pip install -r requirements.txt (pip3 for Mac)
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

#### View Site
Local site available at http://127.0.0.1:8000

#### Create superuser
python manage.py createsuperuser

enter username and password

will be able to use these to log into admin console at

https://127.0.0.1:8000/admin

#### Screenshots
![Screen Shot 2021-02-25 at 1 22 10 PM](https://user-images.githubusercontent.com/54478043/109211381-c2ea2000-7773-11eb-9a23-0fa55c3b9c31.png)

#### Run tests
python manage.py test puzzle_share.tests
