# Define the main character template
define p = Character("[player_name]", color="#a1c4ff")

# Initialize variables
init python:
    player_name = "Farmer"
    money = 100
    day = 1
    
    crops = {
        "wheat": {"planted": 0, "harvested": 0, "days_to_grow": 3, "profit": 10},
        "corn": {"planted": 0, "harvested": 0, "days_to_grow": 5, "profit": 20},
        "carrot": {"planted": 0, "harvested": 0, "days_to_grow": 4, "profit": 25},
    }

    farm = []

    weather = "Sunny"

    def plant_crop(crop):
        global money
        global farm
        if money >= 5:
            money -= 5
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

# script.rpy
label main_menu:
    $ player_name = renpy.input("Enter your name:").strip()
    if player_name == "":
        $ player_name = "Farmer"
    
    # Update the main character with the player's name
    $ p = Character("[player_name]", color="#a1c4ff")
    
    p "Welcome to your farm, [player_name]!"
    p "You have [money] gold coins and it's Day [day]."
    
    call start

label start:
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
            jump start
        "View Farm":
            jump view_farm
        "Exit":
            p "Thanks for playing!"
            $ renpy.quit()

label plant_crops:
    show screen status
    p "What would you like to plant?"
    
    menu:
        "Plant Wheat (5 gold)":
            $ success = plant_crop("wheat")
            if success:
                p "You planted wheat."
            else:
                p "You don't have enough money to plant wheat."
            jump start
        "Plant Corn (5 gold)":
            $ success = plant_crop("corn")
            if success:
                p "You planted corn."
            else:
                p "You don't have enough money to plant corn."
            jump start
        "Plant Carrot (5 gold)":
            $ success = plant_crop("carrot")
            if success:
                p "You planted carrot."
            else:
                p "You don't have enough money to plant carrot."
            jump start
        "Go back":
            jump start

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
    jump start

label fertilize_crops:
    show screen status
    p "Which crop would you like to fertilize?"
    $ choices = [f"{i+1}. {plot['crop']} ({plot['days_left']} days left)" for i, plot in enumerate(farm)]
    if choices:
        $ choice = renpy.input("Choose a crop to fertilize:\n" + "\n".join(choices))
        $ index = int(choice) - 1
        if 0 <= index < len(farm):
            $ fertilize_crop(index)
            p "You fertilized the crop."
        else:
            p "Invalid choice."
    else:
        p "You have no crops to fertilize."
    jump start

label remove_pests:
    show screen status
    p "Which crop would you like to treat for pests?"
    $ choices = [f"{i+1}. {plot['crop']} ({plot['days_left']} days left)" for i, plot in enumerate(farm) if plot["pests"]]
    if choices:
        $ choice = renpy.input("Choose a crop to treat for pests:\n" + "\n".join(choices))
        $ index = int(choice) - 1
        if 0 <= index < len(farm):
            $ remove_pests(index)
            p "You removed pests from the crop."
        else:
            p "Invalid choice."
    else:
        p "You have no crops with pests."
    jump start

label view_farm:
    show screen status
    p "Here is the status of your farm:"
    $ crop_status = "\n".join([f"{i+1}. {plot['crop'].capitalize()} - {plot['days_left']} days left (Watered: {'Yes' if plot['watered'] else 'No'}, Fertilized: {'Yes' if plot['fertilized'] else 'No'}, Pests: {'Yes' if plot['pests'] else 'No'})" for i, plot in enumerate(farm)])
    if crop_status:
        $ crop_status_text = crop_status
    else:
        $ crop_status_text = "Your farm is empty."
    p "[crop_status_text]"
    
    jump start
