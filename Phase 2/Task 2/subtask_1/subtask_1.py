dict = {}

with open("stock.txt") as f:
    for line in f:
        item, quantity = line.strip().split(",")
        dict[item] = int(quantity)
f.close()

while True:
    print("1. Add stock\n2. Remove stock\n3. Show stock\n4. Exit program\n")
    choice = input("Enter your choice: ")
    match choice:
        case "1":
            while True:
                item = input("Enter stock: ")
                if item.isalpha():
                    item = item.lower()
                elif item.isnumeric():
                    item = int(item) - 1
                    if item > len(dict) - 1 or item < 0:
                        print("Please enter a valid choice")
                        continue
                else:
                    print("Please enter a valid choice")
                    continue
                quantity = input("Enter quantity: ")
                if quantity.isnumeric():
                    quantity = int(quantity)
                else:
                    print("Please enter a valid choice")
                    continue
                if isinstance(item, int):
                    item = list(dict.keys())[item]
                if item in dict:
                    dict[item] += quantity
                else:
                    dict[item] = quantity
                print(f"{quantity} {item} added to stock")
                break
        case "2":
            while True:
                item = input("Enter stock: ")
                if item.isalpha():
                    item = item.lower()
                elif item.isnumeric():
                    item = int(item) - 1
                else:
                    print("Please enter a valid choice")
                    continue
                quantity = input("Enter quantity: ")
                if quantity.isnumeric():
                    quantity = int(quantity)
                else:
                    print("Please enter a valid choice")
                    continue
                if isinstance(item, int):
                    item = list(dict.keys())[item]
                if item in dict:
                    if dict[item] >= quantity:
                        dict[item] -= quantity
                        print(f"{quantity} {item} removed from stock")
                    else:
                        print(f"Not enough {item} in stock")
                else:
                    print(f"{item} not found in stock")
                break
        case "3":
            print("Stock:")
            for item, quantity in dict.items():
                print(f"{item}: {quantity}")
        case "4":
            with open("stock.txt", "w") as f:
                for item, quantity in dict.items():
                    f.write(f"{item},{quantity}\n")
            f.close()
            print("Exiting program...")
            break