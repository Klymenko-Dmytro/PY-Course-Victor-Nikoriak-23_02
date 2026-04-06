class Mathematician:

    def square_nums(self, our_list):
        l = map(lambda x: x ** 2, our_list)
        return print(list(l))

    def remove_positives(self, our_list):
        l = filter(lambda x: x < 0, our_list)
        return print(list(l))

    def filter_leaps(self, our_list):
        l = filter(lambda x: x % 4 == 0, our_list)
        return print(list(l))

m = Mathematician()
m.square_nums([7, 11, 5, 4])
m.remove_positives([26, -11, -8, 13, -90])
m.filter_leaps([2001, 1884, 1995, 2003, 2020])