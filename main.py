import random

choices = ["paper", "scissors", "rock"]  # default game options
losing_combos = {}
game_in_process = True
current_score = 0
player_index = 0
player = ""
ratings_list = []


def get_rating():
    global current_score
    global ratings_list
    global player_index
    ratings = open("rating.txt")
    ratings_list = ratings.read().split("\n")
    ratings.close()

    for player_index, rating in enumerate(ratings_list):
        if player in rating:
            current_score = int(rating.split()[1])
            break
        else:
            player_index = len(ratings_list)
            ratings_list.append(player + " 0")
            update_rating()
            break


def update_rating():
    global ratings_list
    ratings_list[player_index] = player + " " + str(current_score)
    ratings = open("rating.txt", "w")
    ratings.write("\n".join(ratings_list))
    ratings.close()


def add_score(points):
    global current_score
    current_score += points
    update_rating()


def game_options():
    global choices
    selected_options = input()
    if selected_options:
        choices = selected_options.split(",")
    print("Okay, let's start")
    calculate_losing_combos(choices)


def calculate_losing_combos(choices_list):
	global losing_combos
	for idx, option in enumerate(choices_list):
		start = idx + 1
		end = start + len(choices) // 2
		if end <= len(choices):
			losing_combos[option] = choices_list[start:end]
		else:
			new_list = choices_list[start:len(choices_list)]
			start_list = choices_list[:len(choices)//2-len(new_list)]
			new_list.extend(start_list)
			losing_combos[option] = new_list


def main():
    global game_in_process
    global player
    player = input("Enter your name: ")
    print(f"Hello, {player}")

    get_rating()

    game_options()

    while game_in_process:
        user_choice = input()
        computer_choice = random.choice(choices)

        if user_choice in choices:
            if computer_choice in losing_combos[user_choice]:
                print(f"Sorry, but computer chose {computer_choice}")
            elif user_choice == computer_choice:
                print(f"There is a draw ({user_choice})")
                add_score(50)
            else:
                print(
                    f"Well done. Computer chose {computer_choice} and failed")
                add_score(100)
        elif user_choice == "!exit":
            print("Bye!")
            game_in_process = False
        elif user_choice == "!rating":
            print(f"Your rating: {current_score}")
        else:
            print("Invalid input")


main()
