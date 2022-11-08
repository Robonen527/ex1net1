import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 12345))

def process_data(init_data, address, group):
    l = init_data.split(' ',1)
    command_number = l[0]
    data = l[1]
    if command_number == 1:
        group.add_member(Member(data, address))

    if command_number == 2:
        member = group.members[address]
        group.message_to_all(address, f"{member.name}: data")

    if command_number == 3:
        member = group.members[address]

#dddd
class Member:
    def __init__(self, name, address, group = None):
        self.name = name
        self.address = address
        self.messages = []
        self.group = group

    def set_name(self, name):
        self.name = name

    def add_message(self, str):
        self.messages.append(str)

    def set_group(self, group):
        self.group = group

class Group:
    def __init__(self):
        self.members = {}

    def add_member(self, member):
        if member.address not in self.members:
            s.sendto(", ".join([v.name for v in self.members.values()]), member.address)
            self.members[member.address] = member
            member.set_group(self)
            self.message_to_all(member.address, f"{member.name} has joined")

    def message_to_all(self, address, message):
        for key in self.members:
            if key != address:
                self.members[key].add_message(message)


def main():
    group = Group()

    while True:
        data, addr = s.recvfrom(1024)

        s.sendto(data.upper(), addr)

