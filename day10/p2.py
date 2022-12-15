class Cpu:
    def __init__(self):
        self.register = 1
        self.cycle = 1
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def execute(self, instruction):
        while not instruction.is_complete():
            for user in self.users:
                user.on_cpu_tick(self)
            instruction.tick(self)
            self.cycle += 1


class Instruction:
    def __init__(self):
        self.ticks = self.instruction_duration()

    def is_complete(self):
        return self.ticks == 0

    def tick(self, cpu):
        self.ticks -= 1
        if self.ticks == 0:
            self.on_complete(cpu)

class Addx(Instruction):
    def __init__(self, add_value):
        super().__init__()
        self.add_value = add_value

    def instruction_duration(self):
        return 2

    def on_complete(self, cpu):
        cpu.register += self.add_value

class Noop(Instruction):
    def __init__(self):
        super().__init__()

    def instruction_duration(self):
        return 1

    def on_complete(self, cpu):
        pass

class Screen:
    def __init__(self):
        self.width = 40
        self.height = 6
        self.image = [[' ' for i in range(self.width)] for i in range(self.height) ]
        self.cursor = (0, 0)
        pass

    def on_cpu_tick(self, cpu):
        (x, y) = self.cursor
        if abs(cpu.register - x) <= 1:
            self.image[y][x] = '#'
        x += 1
        if x == self.width:
            x = 0
            y += 1
        self.cursor = (x, y)

class InstructionFactory:
    def create_instruction(self, instruction_string):
        if instruction_string[0:4] == 'addx':
            return Addx(int(instruction_string[5:]))
        else:
            return Noop()


sum = 0
factory = InstructionFactory()
screen = Screen()
cpu = Cpu()
cpu.add_user(screen)
with open('input.txt', 'r') as f:
    for line in f:
        cpu.execute(factory.create_instruction(line.strip()))

for line in screen.image:
    for c in line:
        print(c, end='')
    print()