import my_modules.my_modules_2 as my_m

x, y = input("Write two numbers (num1 num2): ").split()
print("Result function: ", my_m.sum_numbers(int(x), int(y)))
