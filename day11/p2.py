import re
from collections import deque

# operation value providers
class OldValue:
    def value(self, item):
        return item.worry_level

class Constant:
    def __init__(self, constant):
        self.constant = constant
    def value(self, item):
        return self.constant

# operations
class Add:
    def compute(self, left, right):
        return left + right

class Subtract:
    def compute(self, left, right):
        return left - right

class Multiply:
    def compute(self, left, right):
        return left * right

class Divide:
    def compute(self, left, right):
        return left / right

# calculator
class WorryCalculator:
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def new_worry(self, item):
        return self.operation.compute(self.left.value(item), self.right.value(item))

class CalculatorFactory:
    def create_calculator(self, expression):
        parts = expression.split(' ')
        return WorryCalculator(self.__operation_for(parts[1]), self.__value_provider_for(parts[0]), self.__value_provider_for(parts[2]))

    def __value_provider_for(self, part):
        if part == 'old':
            return OldValue()
        else:
            return Constant(int(part))

    def __operation_for(self, op_char):
        match op_char:
            case '+':
                return Add()
            case '-':
                return Subtract()
            case '*':
                return Multiply()
            case '/':
                return Divide()


# test
class Test:
    def __init__(self, divisor):
        self.divisor = divisor

    def __call__(self, item):
        return item.worry_level % self.divisor == 0

# monkey
class Monkey:
    def __init__(self, items, monkeys, true_monkey, false_monkey, calculator, test):
        self.items = items
        self.monkeys = monkeys
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.calculator = calculator
        self.test = test
        self.num_inspected = 0

    def catch_item(self, item):
        self.items.append(item)

    def inspect_items(self):
        while len(self.items):
            self.num_inspected += 1
            item = self.items.popleft()
            item.worry_level = self.calculator.new_worry(item)
            # 9699690 is the multiple of my inputs tests, idk if it's the same for everyone
            item.worry_level = item.worry_level % 9699690 if item.worry_level > 9699690 else item.worry_level
            if self.test(item):
                self.monkeys[self.true_monkey].catch_item(item)
            else:
                self.monkeys[self.false_monkey].catch_item(item)

#item
class Item:
    def __init__(self, initial_worry_level):
        self.worry_level = initial_worry_level

monkeys = []
calculator_factory = CalculatorFactory()


with open('input.txt', 'r') as infile:
    more_monkeys = True
    while more_monkeys:
        infile.readline() # ignore first line
        starting_item_levels = [ int(i) for i in re.search('(Starting items: )(.*)', infile.readline().strip()).group(2).split(', ')]
        calculator = calculator_factory.create_calculator(re.search('Operation: new = (.*)', infile.readline().strip()).group(1))
        test = Test(int(re.search('Test: divisible by (\d+)', infile.readline().strip()).group(1)))
        true_monkey = int(re.search('If true: throw to monkey (\d+)', infile.readline().strip()).group(1))
        false_monkey = int(re.search('If false: throw to monkey (\d+)', infile.readline().strip()).group(1))
        monkeys.append(Monkey(deque([Item(i) for i in starting_item_levels]), monkeys, true_monkey, false_monkey, calculator, test))

        more_monkeys = infile.readline() != ''

for i in range(10000):
    for j in range(len(monkeys)):
        monkeys[j].inspect_items()

monkeys.sort(key=lambda m: m.num_inspected, reverse=True)

print(monkeys[0].num_inspected * monkeys[1].num_inspected)