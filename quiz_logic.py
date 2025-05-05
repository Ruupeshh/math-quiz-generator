import random

def generate_question(op, difficulty):
    # setting up difficulty ranges
    low = 0
    high = 1  # just placeholders

    if difficulty == "Easy":
        low = 1
        high = 10
    elif difficulty == "Medium":
        low = 10
        high = 100
    else:
        low = 100
        high = 1000

    # grab two random numbers in that range
    first = random.randint(low, high)
    second = random.randint(low, high)

    # if user picked mixed, just randomly choose one operation
    if op == "mixed":
        op = random.choice(["+", "-", "×", "÷"])

    # now handle the actual question generation
    if op == "+":
        return [first, second, op, first + second]  # sum
    elif op == "-":
        return [first, second, op, first - second]  # subtract
    elif op == "×":
        return [first, second, op, first * second]  # multiply
    elif op == "÷":
        # making sure it's clean division
        result = first  # use this as the final answer
        first = first * second  # so a / b = result
        return [first, second, op, result]  # division without messy decimals
