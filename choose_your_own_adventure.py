name = input("Type your name: ")
print(f"Welcome {name} to this adventure!")

answer = input("You are on a dirt road, it has come to an end and you can go left or right.Which way would you like to go? ")
if answer.lower() == "left":
    answer = input("You come to a river, you can walk around it or swim. Type walk to walk around and swim to swim: ")
    if answer == "swim":
        print("You swam accros and were eaten by an alligator.")
    elif answer == "walk":
        print("You walked many miles, ran out of water and you lost the game.")
    else:
        print("Not a valid option. You lose.")

elif answer.lower() == "right":
    answer = input("You came to a bridge, it looks woobly, do you wnatto cross it or head back(cross/back)? ")
    if answer == "back":
        print("You go back to main road. You neither won nor loss")
    elif answer == "cross":
        print("You cross a bridge, you met a stranger. Do you want to talk to him? Type yes or no: ")

    else:
        print("Not a valid option. You lose.")

else:
    print("Not a valid option. You lose.")

print(f"Thank you {name} for trying.")