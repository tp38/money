# Money

This project offer 2 applications :
1. **banks** : on which we may track money transactions on a bank account. The model is :
    [bank] 1-1 ---> 0-* [bank account] 1-1 ---> 1-* [pay media]  1-1 ---> 0-* [transaction] 
2. **budget** : on which we may distribute transactions between categories. A category have a name and a target solde. For each category, we monitor that transactions sum is less than target solde.

## Directories

This project have several directories :

- money.code : django code with urls, models, views and html templates.
- money.docs : some uml document for this project
- money.media : logos for the differents banks
- money.postgres : data for postgresql
- money.static : contain jquery and bootstrap files


## Installation

Frontend is based on Django framework and backend is a PostgreSQQL server. This document describe how to install them on Docker containers :
- Configuration of each container are in **Dockerfile** and **docker-compose.yml** files. read this files and docker documentation to customize them according to your needs.
- run : docker compose up 
- **entrypoint.sh** : launch Django developpement web server 

With this configuration :
- PostgreSql can be access by pgAdmin on localhost port 5555
- Application can be access by the url http://localhost:8000/banks/ 

## Admin_tools

In this directory, there's some python scripts to import or export data :

- **extract_bank-user.csh** : This script is use to extract data on production server. It produce several differents json files that being used to migrate data from *old budget project* to *new money project*. It has no use now and i just conserving it as an archive.
- **extract_db.csh** : This script is use to extract data on server as a json file to backup or import them somewhere else.
- **migrate_db.sh** : This script is use to import data with extract_bank-user.csh. It has no use now and i just conserving it as an archive.
- **package.sh** : use to create a package for updating server
- **update_db.sh** : use to update the dev server within production data or vice versa.

There's also :

- **requirements.txt** : list python modules (with versions) need for the project. This file may be use by a pip install -r requirements.txt command.
- **secret.txt.example** : a file that contain password for *update_db.sh*.
