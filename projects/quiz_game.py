# print("Welcome to my computer quiz!")

# playing = input("Do you want to play? ")

# if playing.lower() != "yes":
#     quit()

# print("Okay! Let's play :)")
# score = 0

# answer = input("What does CPU stand for? ")
# if answer.lower() == "central processing unit":
#     print("Correct!")
#     score += 1
# else:
#     print("Incorrect!")

# answer = input("What does GPU stand for? ")
# if answer.lower() == "graphic processing unit":
#     print("Correct!")
#     score += 1
# else:
#     print("Incorrect!")

# answer = input("What does RAM stand for? ")
# if answer.lower() == "random access memory":
#     print("Correct!")
#     score += 1
# else:
#     print("Incorrect!")

# answer = input("What does PSU stand for? ")
# if answer.lower() == "power supply unit":
#     print("Correct!")
#     score += 1
# else:
#     print("Incorrect!")

# print("You got " + str(score) + " questions correct!")
# print("You got " + str((score/4) * 100) + "%.")



class QuizGame:
    def __init__(self) -> None:
        print("Welcome to the quize game!")
        playing = input("Do you want to play? ")

        if playing.lower() != "yes":
            quit()
        print("Okay! Let's play :)")

        self.questions = [
            "What does CPU stand for? ",
            "What does GPU stand for? ",
            "What does RAM stand for? ",
            "What does PSU stand for? "
        ]
        self.answers = [
            "central processing unit",
            "graphic processing unit",
            "random access memory",
            "power supply unit"
        ]

    def round(self, question: str, answer: str) -> bool:
        reply = input(question)
        if reply.lower() == answer:
            print("Correct!")
            return True
        else:
            print("Incorrect!")
            return False

    def play(self) -> None:
        score = 0
        for i in range(len(self.questions)):
            result = self.round(self.questions[i], self.answers[i])
            if result == True:
                score += 1
        
        print("You got " + str(score) + " questions correct!")
        print("You got " + str((score/4) * 100) + "%.")


obj = QuizGame()
obj.play()