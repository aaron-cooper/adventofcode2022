class Cpu:
    def __init__(self):
        self.register = 1
        self.cycle = 1
        self.special_cycles = set([i for i in range(20, 221, 40)])
        self.signal_sum = 0

    def execute(self, instruction):
        while not instruction.is_complete():
            instruction.tick(self)
            self.cycle += 1
            if self.cycle in self.special_cycles:
                self.signal_sum += self.cycle * self.register

class Addx:
    def __init__(self, add_value):
        self.ticks = 2
        self.add_value = add_value

    def is_complete(self):
        return self.ticks == 0

    def tick(self, cpu):
        self.ticks -= 1
        if self.ticks == 0:
            cpu.register += self.add_value

class Noop:
    def __init__(self):
        self.ticks = 1

    def is_complete(self):
        return self.ticks == 0

    def tick(self, cpu):
        self.ticks -= 1

class InstructionFactory:
    def create_instruction(self, instruction_string):
        if instruction_string[0:4] == 'addx':
            return Addx(int(instruction_string[5:]))
        else:
            return Noop()


sum = 0
factory = InstructionFactory()
cpu = Cpu()
with open('input.txt', 'r') as f:
    for line in f:
        cpu.execute(factory.create_instruction(line.strip()))

print(cpu.signal_sum)