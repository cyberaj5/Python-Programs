def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

def celsius_to_kelvin(celsius):
    kelvin = celsius + 273.15
    return kelvin

while True:
    print("Temperature Conversion Menu:")
    print("1. Kelvin to Celsius")
    print("2. Celsius to Kelvin")
    print("3. Quit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        kelvin = float(input("Enter temperature in Kelvin: "))
        celsius = kelvin_to_celsius(kelvin)
        print(f"{kelvin} Kelvin is equal to {celsius} Celsius.")
    elif choice == '2':
        celsius = float(input("Enter temperature in Celsius: "))
        kelvin = celsius_to_kelvin(celsius)
        print(f"{celsius} Celsius is equal to {kelvin} Kelvin.")
    elif choice == '3':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option (1/2/3).")
