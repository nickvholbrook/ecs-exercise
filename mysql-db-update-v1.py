# 1. Get version from versionTable (row #1)

# 2. Ingest list of files from PATH. Get number. 

# 3. If number exceeds version, execute contents of file and set newVersion to version if it's higher than version.

# 4. Update version


from os import listdir
from os.path import isfile, join
import sys
import mysql.connector

path = sys.argv[1]
mysql_uname = sys.argv[2]
mysql_host = sys.argv[3]
mysql_db = sys.argv[4]
mysql_pass = sys.argv[5]

db = mysql.connector.connect(host=mysql_host, user=mysql_uname, passwd=mysql_pass, database=mysql_db)
crs = db.cursor()


print("path: " + path + " " + mysql_uname + " " + mysql_host + " " + mysql_db + " " + mysql_pass)

files = sorted([f for f in listdir(path) if isfile(join(path, f))])

crs.execute("SELECT version FROM versionTable limit 1")
current_version = int(crs.fetchone()[0])
new_version = current_version
print(current_version)

for f in files:
    prefix = ""
    for c in f:
        if c.isdigit():
            prefix = prefix + c
        else:
            break
    
    print(prefix)
    try:
        this_version = int(prefix)
        
        if this_version > current_version: 
            print(f)
            hndl = open(join(path, f), mode='r')
            contents = hndl.read()
            hndl.close()
            crs.execute(contents)
            
            print("imported " + f)
            if this_version > new_version:
                new_version = this_version
    except ValueError:
        continue

if new_version > current_version:
    crs.execute("UPDATE versionTable SET version = " + str(new_version))

db.commit()
crs.close()
db.close()