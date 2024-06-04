# Arata_AppDevelopmentProject

## Getting started (Windows)
---
clone this repo to your workspace/src: 
```
git clone https://github.com/gabriel0139/Arata_AppDevelopmentProject.git
```  

inside the Arrata_AppDevelopmentProject there is a requirements.txt for installing additional requirements.  
inside the Arrata_AppDevelopmentProject folder run:
```
python -m venv AppDevVenv
python -m pip install -r .\requirements.txt


# Powershell (Windows)
.\AppDevVenv\Scripts\activate 

# CMD (Linux)
source AppDevVenv/bin/activate
```  

Once the requirements are installed and the environment activated  
```
# Powershell (Windows)
$env:FLASK_APP = "Arrata"
$env:FLASK_ENV = "development"
New-Item -Path 'instance' -ItemType Directory
flask init-db
flask run

# CMD (Windows)
set FLASK_APP=Arrata
set FLASK_ENV=development
mkdir instance
flask init-db
flask run

# CMD (Linux)
set FLASK_APP=flaskr
set FLASK_ENV=development
mkdir instance
flask init-db
flask run
```


# Usage
## Starting your own branch
```
# from the develop branch
git checkout -b <name of your branch>

# this will create a new branch 
# you can now start modifying
```

## Updating files to GitHub (your own branch)
```
# in your root directory
git status

# check which branch u are on
git branch

# stage your modified files for git to push
git add .

# add a description/message about what changes you made
git commit -m <enter your message>

# push your updates
git push origin feature-x-xxxxx-xxxx
```

## Getting updates from Develop and resolving conflicts  
Do this whenever develop branch has a new update  
This will keep your branch upto date and close to the develop branch
```
# In your feature branch
git pull --rebase origin develop

# You will get a warning when there are conflicts
# Conflicts happen when you there are multiple commits (like changes)
# in the same file you are working on

# You may abort the rebase with
git rebase --abort

# However, if there are no conflicts or you have resolved the conflict
git add -A

git rebase --continue
# You may encounter new conflicts here. Just do as above: resolve, add, 
# continue until no more conflicts and upto date

# finally
git push -f
```

## RESET team's branch
In develop branch, in your system
```
git branch -D <branch-with-name>
git checkout -b <branch-with-name>
git push -f
```

## Username and Password for Staff
For Staff
```
username: admin@admin.com
password: admin
```
