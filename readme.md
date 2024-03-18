# Blog App using Flask and MySQL

#### App description

This is `Flask` based Blog app with `MySQL` (ORM) at backend. It has four sections:

1. Posts Page:
   Global users who visit website can see the posts uploaded by admin. Pagination is implemented at backend.

2. Contact Page:
   If users want to contact admin, they can fill the contact form which asks there name, contact no., email, and any message they want to deliver.

3. About Page:
   Here admin can write introductory information of his Blog website, his purpose, and any information he wants to deliver to his readers.

4. Dashboard (For Admin only):
   Admin (website owner) has to login via credentials. And then he can create, delete, and update posts. 



## Guide: Running the App
Follow these steps:

1. Pre-requisites
2. Setup and Connect Database to App 
5. Run Website


### 1. Pre-requisites
Update and install python venv.
```bash
sudo apt update
sudo apt-get install python3-venv
```

Clone github repo for this project.
```bash
cd ~
git clone https://github.com/Saweiz/Flask-Blog-App
cd Flask-Blog-App
```

Create virtual environment and activate it.
```bash
python3 -m venv venv
source venv/bin/activate
```

Install Flask and other python packages.
```bash
pip install flask flask-sqlalchemy pymysql

```


### 2. Setup and Connect Database to App 

Now we will access MySQL server and create Database and Tables. Say, MySQL server credentials and params are,

```text
username = admin
password = my_sql_passwd
host = 172.17.0.2
port = 3306
database_name = blog_app_db
```

Now to create database and tables, get into the MySQL server via MySQL Client,
```bash
# install MySQL Client
sudo apt install mysql-client
```
```bash
# access MySQL server
mysql -u admin -p --host 172.17.0.2 --protocol tcp
```
After entering password, run following SQL commands,
```sql
CREATE DATABASE blog_app_db;
USE blog_app_db;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
 
# contacts table
CREATE TABLE `contacts` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `phone_num` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
# posts table
CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `title` text NOT NULL,
  `tagline` text NOT NULL,
  `slug` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(12) NOT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
ALTER TABLE `contacts` ADD PRIMARY KEY (`sno`);
 
ALTER TABLE `posts` ADD PRIMARY KEY (`sno`);
 
ALTER TABLE `contacts` MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
 
ALTER TABLE `posts` MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9; COMMIT;
```

#### Connecting Database with Flask App
You need to edit config.json for this,
```json
...
...
"local_uri": "mysql://username:password@host:port/database_name",
"prod_uri": "mysql://username:password@host:port/database_name",
...
...
```

referring to the supposed credentials and params in previous section, `"local_uri"` in `config.json` would be:
```json
"local_uri": "mysql://admin:my_sql_passwd@172.17.0.2:3306/blog_app_db",
```
Note: In case of RDS, <b>host = database endpoint<b>.


### 3. Run Website
Run python file,
```python
python3 main.py
```
And the app would be running on `http://localhost:5000`.

