# import random
# chances = 3
# number = random.randint(1, 10)
# print("Welcome to the Number Guessing Game!")
# print("I'm thinking of a number between 1 and 10.")
# print(f"You have {chances} chances to guess the number.")
# while chances > 0:    
#     guess = int(input("Enter your guess: "))
#     if guess == number:
#         print("Congratulations! You've guessed the number!")
#         break
#     elif guess < number:
#         print("Too low! Try again.")
#     else:        
#         print("Too high! Try again.")
#     chances -= 1
# if chances == 0:    
#     print(f"Sorry, you've run out of chances. The number was {number}.")



d = {"a":{"b":{"c":1,"d":{"e":2,"f":{"g":3}}}}}
count = 1
def func(d, count):
    for key, val in d.items():
        if isinstance(val, dict):
            count+=1
            count = func(val, count)
    return count

print(func(d, count))


d = [(1,2,3,5)]
print(dict(d))