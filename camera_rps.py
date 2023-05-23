import cv2
from keras.models import load_model
import numpy as np
import random
import time

class RockPaperScissors:
    def __init__(self, model_path='keras_model.h5', video_source=0):
        self.model = load_model(model_path)
        self.cap = cv2.VideoCapture(video_source)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.computer_rps = ["rock", "paper", "scissors"]
        self.computer_wins = 0
        self.user_wins = 0

    def get_computer_choice(self):
        computer_choice = random.choice(self.computer_rps)
        return computer_choice

    def get_prediction(self, prediction):
        if np.argmax(prediction) == 0:
            return "rock"
        elif np.argmax(prediction) == 1:
            return "paper"
        elif np.argmax(prediction) == 2:
            return "scissors"
        else:
            return "nothing"

    def get_user_choice(self):
        countdown = 3
        start_time = time.time()

        while True: 
            ret, frame = self.cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1  # Normalize the image
            self.data[0] = normalized_image
            prediction = self.model.predict(self.data)
            output_frame = frame.copy()  # Create a copy of the frame for output
            
            elapsed_time = time.time() - start_time  # Calculate the elapsed time

            if elapsed_time < countdown:
                countdown_text = str(countdown - int(elapsed_time))
                cv2.putText(output_frame, countdown_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('frame', output_frame)
            else:
                user_choice = self.get_prediction(prediction)
                cv2.putText(output_frame, f"You chose: {user_choice}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('frame', output_frame)
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        return user_choice

    def get_winner(self, computer_choice, user_choice):
        print(f"Computer chooses: {computer_choice}")
        print(f"You choose: {user_choice}")
        if computer_choice == user_choice:
            print("It is a tie!")
        elif (computer_choice == "rock" and user_choice == "scissors") or (computer_choice == "paper" and user_choice == "rock") or (computer_choice == "scissors" and user_choice == "paper"):
            return "You lost"
        else:
            return "You won!"

    def play(self):
        while self.computer_wins < 3 and self.user_wins < 3:
            computer_choice = self.get_computer_choice()
            user_choice = self.get_user_choice()
            winner = self.get_winner(computer_choice, user_choice)
            
            if winner == "You lost":
                self.computer_wins += 1
            elif winner == "You won!":
                self.user_wins += 1
            
            print(f"Computer wins: {self.computer_wins} | User wins: {self.user_wins}")
        
        if self.computer_wins == 3:
            print("Computer wins the game!")
        else:
            print("You win the game!")

        self.cap.release()
        cv2.destroyAllWindows()

game = RockPaperScissors()
game.play()
