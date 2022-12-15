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

class SignalMeter:
    def __init__(self):
        self.special_cycles = set([i for i in range(20, 221, 40)])
        self.signal_sum = 0

    def on_cpu_tick(self, cpu):
        if cpu.cycle in self.special_cycles:
            self.signal_sum += cpu.cycle * cpu.register

class InstructionFactory:
    def create_instruction(self, instruction_string):
        if instruction_string[0:4] == 'addx':
            return Addx(int(instruction_string[5:]))
        else:
            return Noop()


sum = 0
factory = InstructionFactory()
meter = SignalMeter()
cpu = Cpu()
cpu.add_user(meter)
with open('input.txt', 'r') as f:
    for line in f:
        cpu.execute(factory.create_instruction(line.strip()))

print(meter.signal_sum)