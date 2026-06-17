#creat an expert system
print("WELCOME TO HEALTH CARE")
MALARIA =["extreme tiredness" , "fever" ,"headache" , "high temperature" ]
HIV =["fever","headache","rash","sore throat"]
COVID_19 =["cough","muscle aches" , "sneezing","difficulty in sleeping"]
FEVER = ["feeling cold","flushed","sweating","shivering"]
GONORRHEA= ["swollen testes" , "rash","bleeding","painful bowel movements"]
SYMPTOMS = ["extreme tiredness" , "fever" ,"headache" , "high temperature" ,"rash","sore throat","numbness","muscle aches" , "change of sense of taste or smell","difficulty in sleeping",
"feeling cold","flushed","sweating","shivering","swollen testes" , "yellow or greenish discharge from the penis","bleeding","painful bowel movements"]
print(" ")
input ("select  the symptoms from the list below :")
print(" ")
symptom_1 = input("The symptom_1 :")
symptom_2 = input("The symptom_2 :")
symptom_3 = input("The symptom_3 :")
symptom_4 = input("The symptom_4 :") 

if symptom_1= "headache", symptom_2="high temperature", symptom_3="fever":
print("You have malaria")