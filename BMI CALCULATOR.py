print ("WELCOME TO CYBER AJ'S BMI CALCULATOR")
print("TIME TO KNOW WHETHER YOU ARE CLASSIFIED AS")
print("UNDERWEIGHT,NORMAL WEIGHTED,OVERWEIGHT AND THE OBESE")
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def interpret_bmi(bmi):
    return "Underweight" if bmi < 18.5 else "Normal weight" if 18.5 <= bmi < 25 else "Overweight" if 25 <= bmi < 30 else "Obese"

weight = float(input("Enter your weight in kilograms: "))
height = float(input("Enter your height in meters: "))
bmi = calculate_bmi(weight, height)
print(f"Your BMI is: {bmi:.2f}")
print(f"YOU ARE CLASSIFIED AS: {interpret_bmi(bmi)}")
#COURTESY AJANI OLUWAFERANMI EMMANUEL