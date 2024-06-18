# Define the main character template
define p = Character("[player_name]", color="#a1c4ff")
# Define the current crop

# set gui textbox align

# Initialize variables
init python:
    player_name = "Farmer"
    money = 100
    day = 1
    
    crops = {
        "wheat": {"planted": 0, "harvested": 0, "days_to_grow": 3, "profit": 15, "price": 5},
        "potato": {"planted": 0, "harvested": 0, "days_to_grow": 5, "profit": 40, "price": 8},
        "carrot": {"planted": 0, "harvested": 0, "days_to_grow": 4, "profit": 28, "price": 7},
        "pumpkin": {"planted": 0, "harvested": 0, "days_to_grow": 7, "profit": 25, "price": 10},
        "golden_seed": {"planted": 0, "harvested": 0, "days_to_grow": 1, "profit": 9999, "price": 9999},
    }

    farm = []

    weather = "Sunny"

    def plant_crop(crop):
        global money
        global farm
        crop_price = crops[crop]["price"]
        if money >= crop_price:
            money -= crop_price
            farm.append({"crop": crop, "days_left": crops[crop]["days_to_grow"], "watered": False, "fertilized": False, "pests": False})
            return True
        return False

    def pass_day():
        global day
        global farm
        global money
        global weather
        day += 1
        new_farm = []
        for plot in farm:
            if plot["pests"]:
                plot["days_left"] += 1  # Pests slow down growth
            elif plot["fertilized"]:
                plot["days_left"] -= 1  # Fertilizer speeds up growth
            if not plot["watered"]:
                plot["days_left"] += 1  # Lack of water slows down growth
            plot["watered"] = False  # Reset watering status
            plot["fertilized"] = False  # Reset fertilization status if not re-applied
            plot["days_left"] -= 1  # Progress growth

            if plot["days_left"] <= 0:
                money += crops[plot["crop"]]["profit"]
                crops[plot["crop"]]["harvested"] += 1
                if plot["crop"] == "golden_seed":
                    renpy.call("win_game")
            else:
                new_farm.append(plot)
        farm = new_farm
        random_event()

    def water_crop(index):
        farm[index]["watered"] = True

    def fertilize_crop(index):
        farm[index]["fertilized"] = True

    def remove_pests(index):
        farm[index]["pests"] = False

    def random_event():
        global farm
        global weather
        import random
        event = random.choice(["good_weather", "bad_weather", "pests", "bonus"])
        if event == "good_weather":
            renpy.notify("Good weather! Crops grow faster.")
            weather = "Sunny"
            for plot in farm:
                plot["days_left"] -= 1
        elif event == "bad_weather":
            renpy.notify("Bad weather! Crops grow slower.")
            weather = "Rainy"
            for plot in farm:
                plot["days_left"] += 1
        elif event == "pests":
            renpy.notify("Pests! Some crops are affected.")
            for plot in farm:
                if random.choice([True, False]):
                    plot["pests"] = True
        elif event == "bonus":
            renpy.notify("Bonus! You found extra seeds.")
            global money
            money += 20

# Define a screen to show status information
screen status:
    frame:
        background "#0008"
        xalign 0.98
        yalign 0.02
        has vbox
        label "Day: [day]" text_size 20
        label "Money: [money] coins" text_size 20
        label "Weather: [weather]" text_size 20

screen farm_status:
    zorder 1
    frame:
        # background "#0008"
        xalign 0.5
        yalign 0.5
        has vbox
        # text "Farm Status" size 20 xalign 0.5
        for i, plot in enumerate(farm):
            vbox:
                text "[i+1]. [plot['crop'].capitalize()] - [plot['days_left']] days left" size 20
                hbox:
                    text "Watered: [ 'Yes |' if plot['watered'] else 'No |']"
                    text "Fertilized: [ 'Yes |' if plot['fertilized'] else 'No |']"
                    text "Pests: [ 'Yes' if plot['pests'] else 'No']"
                text "\n"
                
# script.rpy
label start:
    $ player_name = renpy.input("Enter your name:").strip()
    if player_name == "":
        $ player_name = "Farmer"
    
    # Update the main character with the player's name
    $ p = Character("[player_name]", color="#a1c4ff")
    
    p "Welcome to your farm, [player_name]!"
    p "You have [money] gold coins and it's Day [day]."
    
    call start_game from _call_start_game

label start_game:
    show screen status
    p "What would you like to do today?"
    
    menu:
        "Plant Crops":
            jump plant_crops
        "Water Crops":
            jump water_crops
        "Fertilize Crops":
            jump fertilize_crops
        "Remove Pests":
            jump remove_pests
        "Pass Day":
            $ pass_day()
            p "It's now Day [day]."
            jump start_game
        "View Farm":
            jump view_farm
        "Exit":
            p "Thanks for playing!"
            $ renpy.quit()

label plant_crops:
    show screen status
    $ planted_crops = sum([1 for plot in farm])
    if planted_crops >= 5:
        p "You have reached the maximum number of crops you can plant."
        jump start_game
    else:
        p "You have [5- planted_crops] slots available to plant crops."
        p "What would you like to plant?"
    
    menu:
        "Plant Wheat (5 gold, Profit: 10, Days: 3)":
            $ success = plant_crop("wheat")
            if success:
                p "You planted wheat."
            else:
                p "You don't have enough money to plant wheat."
            jump view_farm
        "Plant Potato (8 gold, Profit: 20, Days: 5)":
            $ success = plant_crop("potato")
            if success:
                p "You planted potato."
            else:
                p "You don't have enough money to plant potato."
            jump view_farm
        "Plant Carrot (7 gold, Profit: 25, Days: 4)":
            $ success = plant_crop("carrot")
            if success:
                p "You planted carrot."
            else:
                p "You don't have enough money to plant carrot."
            jump view_farm
        "Plant Pumpkin (7 gold, Profit: 25, Days: 4)":
            $ success = plant_crop("pumpkin")
            if success:
                p "You planted pumpkin."
            else:
                p "You don't have enough money to plant pumpkin."
            jump view_farm
        "Plant Golden Seed (9999 gold, Profit: 9999, Days: 1)" if money >= 999:
            $ success = plant_crop("golden_seed")
            if success:
                p "You planted the Golden Seed."
            else:
                p "You don't have enough money to plant the Golden Seed."
            jump view_farm
        "Go back":
            jump start_game

label water_crops:
    show screen status
    p "Which crop would you like to water?"
    $ choices = [f"{i+1}. {plot['crop']} ({plot['days_left']} days left)" for i, plot in enumerate(farm)]
    if choices:
        $ choice = renpy.input("Choose a crop to water:\n" + "\n".join(choices))
        $ index = int(choice) - 1
        if 0 <= index < len(farm):
            $ water_crop(index)
            p "You watered the crop."
        else:
            p "Invalid choice."
    else:
        p "You have no crops to water."
    jump start_game

label fertilize_crops:
    show screen status
    p "Which crop would you like to fertilize?"
    $ choices = [f"{i+1}. {plot['crop']} ({plot['days_left']} days left)" for i, plot in enumerate(farm)]
    if choices:
        $ choice = renpy.input("Choose a crop to fertilize:\n" + "\n".join(choices))
        $ index = int(choice) - 1
        if 0 < index < len(farm):
            $ fertilize_crop(index)
            p "You fertilized the crop."
        else:
            p "Invalid choice."
    else:
        p "You have no crops to fertilize."
    jump start_game

label remove_pests:
    show screen status
    p "Which crop would you like to treat for pests?"
    $ choices = [f"{i+1}. {plot['crop']} ({plot['days_left']} days left)" for i, plot in enumerate(farm) if plot["pests"]]
    if choices:
        $ choice = renpy.input("Choose a crop to treat for pests:\n" + "\n".join(choices))
        $ index = int(choice) - 1
        if 0 < index < len(farm):
            $ remove_pests(index)
            p "You removed pests from the crop."
        else:
            p "Invalid choice."
    else:
        p "You have no crops with pests."
    jump start_game

label view_farm:
    hide screen status
    show screen farm_status
    $ renpy.pause(5)  # Pause for 5 seconds to allow the player to view the farm status
    hide screen farm_status
    jump start_game

label win_game:
    scene black
    show screen status
    p "Your final score is: [money] gold coins."
    p "You have successfully managed your farm for [day] days."
    p "Congratulations! You have harvested the Golden Seed and won the game!"
    $ renpy.pause(5)
    $ renpy.quit()