def num_function():
    a, b = input("Write please two numbers (num1 num2): ").split()
    try:
        print(f"Result: {(int(a) ** 2) / int(b)}")
    except ZeroDivisionError:
        print("b = 0, its Error")
    except ValueError:
        print("a or b = chars, its Error")


num_function()
