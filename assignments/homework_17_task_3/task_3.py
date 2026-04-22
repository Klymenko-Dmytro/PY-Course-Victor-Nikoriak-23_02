class Fraction:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        if self.b == other.b:
            return Fraction(self.a + other.a, self.b)
        else:
            i = self.b * other.b
            while i > 0:
                if (self.a * other.b + self.b * other.a) % i == 0 and (self.b * other.b) % i == 0:
                    return Fraction((self.a * other.b + self.b * other.a) / i, self.b * other.b / i)
                else:
                    i -= 1
            return None

    def __sub__(self, other):
        if self.b == other.b:
            return Fraction(self.a - other.a, self.b)
        else:
            i = self.b * other.b
            while i > 0:
                if (self.a * other.b - self.b * other.a) % i == 0 and (self.b * other.b) % i == 0:
                    return Fraction((self.a * other.b - self.b * other.a) / i, self.b * other.b / i)
                else:
                    i -= 1
            return None

    def __mul__(self, other):
        return Fraction(self.a * other.a, self.b * other.b)

    def __truediv__(self, other):
        return Fraction(self.a * other.b, self.b * other.a)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

if __name__ == "__main__":
    x = Fraction(1, 2)
    y = Fraction(1, 4)
    print((x + y) == Fraction(3, 4))
    print(vars(x + y))
    print(vars(x - y))
    print(vars(x * y))
    print(vars(x / y))
