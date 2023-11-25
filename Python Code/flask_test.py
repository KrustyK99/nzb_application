import sqlite3

# filename to form database
file = "auto_increment_test.db"
  
try:
  conn = sqlite3.connect(file)
  print("Database auto_increment_test.db formed.")
except:
  print("Database auto_increment_test.db not formed.")