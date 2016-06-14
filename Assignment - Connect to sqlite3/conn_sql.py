import sqlite3
import re

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor() #cursor object, digunakan agar bisa mengeksekusi command sql pada python

cur.execute('DROP TABLE IF EXISTS Counts;') #mengeksekusi command sql, drop table jika ada table yang exis
cur.execute('CREATE TABLE Counts (email TEXT, count INTEGER);') #buat table baru

fh = open('mbox.txt')
for line in fh:
	if not line.startswith('From: ') : continue # ambil line yang awalnya 'From: '
	pieces = line.split() #displit dan diambil emailnya
	y = re.findall('@(\S+)',pieces[1])
	email = ''.join(y)
	cur.execute('SELECT count FROM Counts WHERE email = ?', (email, )) # '?' merupakan placeholder untuk sebuah variable (binding variable),yang disini mengacu ke variable email. Digunakan untuk prevent sql injection. 
	row = cur.fetchone() #kalo mau ngeprint baris, hasil "SELECT", menggunakan fetch. fetchone ngeambil satu baris saja, dalam hal ini ambil nilai count, dimana email = dimas@gmail.com (contohnya)
	if row is None:
		cur.execute('INSERT INTO Counts (email, count) VALUES (?, 1)', (email, )) #kalo count ga ada, maka count bernilai 1 (hanya 1 email aja yang masuk dari dia)
	else:
		cur.execute('UPDATE Counts SET count=count+1 WHERE email = ?', (email, )) #artinya email dari dia, lebih dari 1, ditambahkan

	conn.commit() #commit dilakukan untuk menuliskan ke SQL server (ngesave)

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

print
print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

cur.close() #closing sqlite connection
