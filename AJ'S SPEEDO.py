# Car speedo

print("Welcome to Speedo")
print("Where speed is tested:")
print(" ")

name = input("Enter your car name: ")
cylinders = int(input("Enter how many cylinders your car has: "))
gear = int(input("Enter the number of gears your car has: "))
acc_rate = float(input("Enter the acceleration rate of your car at 0-100 km/h: "))
engine_power = int(input("Enter the engine horsepower of your car(eg:Honda Accord  192-252 hp): "))
weight = int(input("Enter the weight of your car in kilograms: "))
transmission_type = input("Enter the transmission type a or b (a;automatic, b;manual): ")

print("Below are your car details:")
print("Name:", name)
print("Cylinders:", cylinders)
print("Gears:", gear)
print("Acceleration rate (0-100 km/h):", acc_rate)
print("Engine power (hp):", engine_power)
print("Weight (kg):", weight)
print("Transmission type:", transmission_type)



if engine_power > 250 and weight < 1600 and cylinders >= 6 and gear >= 5 and acc_rate >= 10:
    print("Your", name, "is classified as a fast car,Extremely FAST!!!")
elif engine_power > 150 and weight < 2000 and cylinders >= 4 and acc_rate <= 7:
    print("Your", name, "is classified as a moderately fast car.Which means your Car is fast buh not fast enough")
elif engine_power < 250 and weight > 1600 and cylinders <= 6  and acc_rate <= 10:
    print("Your", name, "is classified a slow car.SLOW!!")
else:
    print("Your", name, "is classified as a standard performance car.Your car is just Normal")

#COURTSEY AJANI OLUWAFERANMI EMMANUEL