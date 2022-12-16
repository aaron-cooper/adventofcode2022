

inventories = []
with open("input.txt", "r") as infile:
    inventory = []
    for line in infile:
        line = line.strip()
        if line == "":
            inventories.append(sum(inventory))
            inventory = []
        else:
            inventory.append(int(line))

inventories.sort(reverse=True)
print(sum(inventories[0:3]))