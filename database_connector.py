import mysql.connector
def DataUpdate(FirstName,LastName,Feedback):
   mydb = mysql.connector.connect(
       host="localhost",
       user="root",
       passwd="root",
       database="chatrobofeedback")
   mycursor = mydb.cursor()

   sql='INSERT INTO feedback (firstName, lastName, feedback) VALUES ("{0}","{1}", "{2}");'.format(FirstName,LastName,Feedback)
   mycursor.execute(sql)
   mydb.commit()