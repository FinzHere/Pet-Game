from pathlib import Path
import random
import sys
import json
import os

thingsToEat = ["Bread", "Ice Cream", "Cookies", "Pet Food", "An Apple", "A Nuclear Warhead", "A Pretzel", "Grapes", "An Undiscovered Animal", "An Unkown Bacterium"]
thingsToPlay = ["Fetch", "Hide and Seek", "Tug-of-war with a rope", "Tug-of-war with posidens trident", "Chess", "Checkers", "Snakes and Ladders", "Rummikub", "Blackjack", "Roulette", "Baccarat", "Rummy", "Go Fish", "Poker", "with a Meteorite that fell from Space", "with a Little Alien"]

age = 1
nextAgeCounter = 0
neededEXP = 3

print("JIMMYS HERE!")

plrstatsfile = {
      "Player":{
              "nickname":""
    },
    "Stats": { 
        "TotalPets": 0,
        "TotalLevels": 0,
        "TotalXP": 0,
        "TotalFeeds": 0,
        "TotalPlays": 0,
        "TotalGambles": 0,
        "TotalErrors": 0,
        "TotalUnborns": 0
    }
}

def ChangePlrName(name):
    filepath = Path(__file__).parent / "Saves" / "player.json"
    with open(filepath, "r") as f:
         plrstatsfile = json.load(f) 

    plrstatsfile["Player"]["nickname"] = name

    with open(filepath, "w") as f:
        json.dump(plrstatsfile, f, indent=4)

def PlrStatsUpdater(thingy, number):
    filepath = Path(__file__).parent / "Saves" / "player.json"
    with open(filepath, "r") as f:
         plrstatsfile = json.load(f) 

    plrstatsfile["Stats"][thingy] = plrstatsfile["Stats"][thingy] + number

    with open(filepath, "w") as f:
        json.dump(plrstatsfile, f, indent=4)
          
#PET CLASS
class Pet:
    def __init__(self, petName: str, petAge: int, petEXP: int, EXPneeded: int) -> None:
        self.petName = petName
        self.petAge = petAge
        self.petEXP = petEXP
        self.EXPneeded = EXPneeded

    #Function for feeding pet
    def Feed(self) -> None:
        foodChoice = random.choice(thingsToEat)
        print(f"\n{self.petName} is hungry!")
        print(f"You fed {self.petName} {foodChoice} and they gained +1 EXP!")
        self.petEXP = self.petEXP + 1
        PlrStatsUpdater("TotalFeeds", 1)
        PlrStatsUpdater("TotalXP", 1)
    
    #Function for playing
    def Play(self) -> None:
        playChoice = random.choice(thingsToPlay)
        print(f"\n{self.petName} wants to play!")
        print(f"You played {playChoice} with {self.petName} and they gained +1 EXP!")
        self.petEXP = self.petEXP + 1
        PlrStatsUpdater("TotalPlays", 1)
        PlrStatsUpdater("TotalXP", 1)

    #Level-up system for pet
    def PetLevelUp(self) -> None:
        if self.petAge >= 99:
            self.petEXP = 0
            self.EXPneeded = 1
            self.petAge = 99
            print(f"\n{pet.petName} is at max level!")
        elif self.petAge <= 0:
            print(f"\n{self.petName} Is Unborn!!")
            PetPath = Path(__file__).parent / "DataSaves" / f"{self.petName}Save.json"
            PetPath.unlink()
            PlrStatsUpdater("TotalUnborns", 1)
            print("Deleting pet save file...")
            print("\nGoodbye!")
            sys.exit()
        else:
            if self.petEXP >= self.EXPneeded:
                self.petAge += 1
                self.petEXP = 0
                self.EXPneeded = self.petAge + 2
                print(f"\n{self.petName} grew up! {self.petName} is now level {self.petAge}!")
                PlrStatsUpdater("TotalLevels", 1)
            else:
                print(f"\nYour pet needs {self.EXPneeded - self.petEXP}EXP to grow up!")
    
    #EXPNEEDED CHECK
    def EXPcheck(self) -> None:
        self.EXPneeded = self.petAge + 2

#GAMBLING FUNC
    def gambling(self):
        #FUNC--only vars
        gamblingAgeneeded = 2
        minChoice = 1
        maxChoice = 2
        while True:
            PlrStatsUpdater("TotalGambles", 1)
            if self.petAge >= gamblingAgeneeded:
                print(f"{gamblingAgeneeded} of {self.petName}\'s levels are on the line!")
                randnumb = random.randint(1,2)
                try:
                    while True:
                        numberChoice = int(input(f"{minChoice} or {maxChoice}!"))
                        if numberChoice == randnumb:
                            print(f"Well Done! {self.petName} gained levels!")
                            maxChoice = maxChoice * 2
                            self.petAge -= gamblingAgeneeded
                            self.petAge += gamblingAgeneeded*2
                            PlrStatsUpdater("TotalLevels", gamblingAgeneeded)
                            gamblingAgeneeded *= 2
                            break
                        elif numberChoice > maxChoice or numberChoice < minChoice:
                            print("Please input one of the available numbers!")
                            continue
                        else:
                            print(f"You lost! {self.petName} lost levels!")
                            minChoice = 1
                            maxChoice = 2
                            self.petAge -= gamblingAgeneeded
                            gamblingAgeneeded = 2
                            break
                    again = str(input("Gamble again?\ny/N?").strip().lower())
                    if again in ["y", "yes"]:
                        continue
                    else:
                        break
                except ValueError:
                    print("Please input a integer(number) and try again!")
                    PlrStatsUpdater("TotalErrors", 1)
            else:
                print(f"{self.petName} does not have enough levels!")
                break

#CREATING NEW PETSAVE
def NameCallingFunc():
    while True:
        namePet = input("What would you like your pet to be called? ").strip()
        filename = f"DataSaves/{namePet}Save.json"

        # Check if file exists
        try:
            with open(filename, "r"):
                # File exists
                print(f"{filename} already exists! Do you want to overwrite it?")
                overwrite = input("y/N? ").strip().lower()

                if overwrite in ["y", "yes"]:
                    return namePet     # Accept overwrite
                else:
                    print("Okay, returning to menu...\n")
                    return None        # ⟵ NEW: lets menu loop continue
            
        except FileNotFoundError:
            # File does NOT exist → Confirm name
            print(f"Your pet's name will be {namePet}.")
            confirmName = input(f"Are you sure {namePet} is the name you want?\n(y/N)?").strip().lower()

            if confirmName in ["y", "yes"]:
                return namePet         # Name confirmed
            else:
                print("Okay, let's choose a different name.\n")
                continue
            
#Warning for user
print("IMPORTANT NOTICE!\nDO NOT change the name or location of the json save files. This could break it!")
print("WARNING🚨🚨")

if os.path.exists("Saves/player.json"):
    with open("Saves/player.json", "r") as f:
        plrstatsfile = json.load(f)
    print(f"Welcome back {plrstatsfile["Player"]["nickname"]}!")
else:
    while True:
        playername = str(input("What's your name?").strip())
        if playername == "":
            print("\nPlease input a name!")
            continue
        else:
            break
    plrstatsfile["Player"]["nickname"] = playername
    with open("Saves/player.json", "w") as f:
        json.dump(plrstatsfile, f, indent=4)
    

#Main Menu
while True:
    try:
        print("\nWhat would you like to do?")
        menu = int(input("1-New Game, 2-Load Save, 3-Find All Save Files, 4-Delete Save Files, 5-Change Player Name, 6-List Player Stats, 7-Save and Quit"))
        #New Creation System
        if menu == 1:
            nameOfPet = NameCallingFunc()
            if nameOfPet is None:
                continue   # ⟵ Returns to menu if naming canceled
            else:
                PlrStatsUpdater("TotalPets", 1)
                break      # Start the game with the chosen name
        #Loading System
        elif menu == 2:
            loadname = input('Type the pet name to load, or "back" to go back(CASE SENSITIVE): ').strip()

            if loadname.lower() in ["b", "back"]:
                continue

            filename = f"DataSaves/{loadname}Save.json"
            try:
                with open(filename, "r") as f:
                    loadeddata = json.load(f)

                nameOfPet = loadeddata["petName"]
                age = loadeddata["petAge"]
                nextAgeCounter = loadeddata["petEXP"]
                neededEXP = loadeddata["EXPneeded"]
                break
                #Stops system from throwing an error and breaking
            except FileNotFoundError:
                print("Your pet's save file was not found!")
        #File Searching System 
        elif menu == 3:
            filename = Path(__file__).parent / "DataSaves"
            if filename.exists() and filename.is_dir():
                for item in filename.iterdir():
                    print(item)
                print("WARNING!")
                print("Please Only Do The Thing In Front Of the Save.json if not this will not load.")
        #Deleting save files system!
        elif menu == 4:
            cp = str(input("Please Enter The Admin Device Pass"))
            #Pass Detc
            if cp == "ABC123":
                choice = input("Please Enter The Name of the Pet(Case Sensitive!): ")
                print()
                filename = Path(__file__).parent / "DataSaves"
                if filename.exists() and filename.is_dir():
                    filepath = filename / f"{choice}Save.json"
                    if filepath.exists() and filepath.is_file():
                        print("EXISTS\n")
                        sure = str(input("Are You Sure You Want This Deleted [Y/N]").strip().lower())
                        if sure in ["y", "yes"]:
                            print("DELETING FILE",filepath)
                            filepath.unlink()
                            print("DELETED FILE")
                        elif sure in ["n", "no"]:
                            print("Ok Thats fine")
                            quit
                        else:
                            print("You Input Does Not Match Any Off The Posiblilitys please do y/n")
                        
                    else:
                        print("NEGITIVE")
            else:
                quit
        
        elif menu == 5:
            while True:
                new_name = str(input("\nWhat would you like your name to be?").strip())
                if new_name == "":
                    print("Please input a name!")
                    continue
                else:
                    ChangePlrName(new_name)
                    break

        #Player Stats Listing
        elif menu == 6:
            print("\n--- PLAYER STATISTICS ---")
            descriptive_names = {
                "TotalPets": "Total Number of Pets Created",
                "TotalXP": "Total XP Earned",
                "TotalFeeds": "Total Number of Feeds",
                "TotalPlays": "Total Number of Plays",
                "TotalGambles": "Total Gambling Attempts",
                "TotalErrors": "Total Input Errors",
                "TotalUnborns": "Total Number of Unborns"
            }

            for key, value in plrstatsfile["Stats"].items():
                label = descriptive_names.get(key, key)
                print(f"{label}: {value}")

        #System Exit
        elif menu == 7:
            print("Goodbye!")
            sys.exit()

    except ValueError:
        print("Please enter a valid number!")
        PlrStatsUpdater("TotalErrors", 1)

#Makes an instance of the class called "pet"
pet = Pet(nameOfPet, age, nextAgeCounter, neededEXP)

#Pet Menu
while True:
    try:
        pet.PetLevelUp()
        pet.EXPcheck()
        print(f"\nWhat would you like to do with {pet.petName}?")
        selector = int(input(f"1-Check {pet.petName}\'s stats, 2-Play with {pet.petName}, 3-Feed {pet.petName}, 4-Save and Quit"))
        #Lists pet's stats
        if selector == 1:
            print(f"\nPet name: {pet.petName}, \nAge: {pet.petAge}, \nCurrent EXP: {pet.petEXP}, \nEXP Until Next Age: {pet.EXPneeded - pet.petEXP}")
        #Calling Of PlayFunc
        elif selector == 2:
            pet.Play()
        #Calling of FeedFunc
        elif selector == 3:
            pet.Feed()
        #Saves and exits
        elif selector == 4:
            filename = f"DataSaves/{pet.petName}Save.json"
            with open(filename, "w") as f:
                json.dump(pet.__dict__, f, indent=4)
            print("You saved your game!\nGoodbye!")
            sys.exit()
        #Gambling...?
        elif selector == 15:
            print("\nDo you want to gamble...?")
            gambleConfirm = str(input(f"{pet.petName}\'s levels(age) is on the line!\ny/N?").strip().lower())
            if gambleConfirm in ["y", "yes"]:
                pet.gambling()
                
    #Error protection
    except ValueError:
        print(f"\nYou did not enter one of the available numbers! To interact with {pet.petName}, please try again and enter one of the defined numbers!")
        PlrStatsUpdater("TotalErrors", 1)