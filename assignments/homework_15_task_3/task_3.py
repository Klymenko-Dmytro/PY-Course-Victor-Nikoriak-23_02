CHANNELS = ["BBC", "Discovery", "TV1000"]

class TVController:

    def __init__(self, channel_list):
        self.channel_list = channel_list
        self.now_channel = 1

    def first_channel(self):
        self.now_channel = 1
        return print(self.channel_list[self.now_channel - 1])

    def last_channel(self):
        self.now_channel = len(self.channel_list)
        return print(self.channel_list[self.now_channel - 1])

    def turn_channel(self, number_channel):
        self.now_channel = number_channel
        if 1 <= self.now_channel <= len(self.channel_list):
            return print(self.channel_list[self.now_channel - 1])
        else:
            return print("No channel")

    def next_channel(self):
        self.now_channel += 1
        while self.now_channel > len(self.channel_list):
            self.now_channel -= len(self.channel_list)
        return print(self.channel_list[self.now_channel - 1])

    def previous_channel(self):
        self.now_channel -= 1
        while self.now_channel < 1:
            self.now_channel += len(self.channel_list)
        return print(self.channel_list[self.now_channel - 1])

    def current_channel(self):
        return print(self.channel_list[self.now_channel - 1])

    def exists(self, arg):
        if type(arg) == int:
            if 1 <= arg <= len(self.channel_list):
                return print("Yes")
            else:
                return print("No")
        elif type(arg) == str:
            if arg in self.channel_list:
                return print("Yes")
            else:
                return print("No")
        else:
            return print("No")

controller = TVController(CHANNELS)

controller.first_channel()
controller.last_channel()
controller.turn_channel(1)
controller.next_channel()
controller.previous_channel()
controller.current_channel()
controller.exists(4)
controller.exists("BBC")
