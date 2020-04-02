import tkinter as tk
from tkinter import Label, LabelFrame, Grid, Entry, messagebox, OptionMenu, StringVar
import os, random, collections, namedtuple


root = tk.Tk()





#frame = tk.Frame(root, bg ="white")
#frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

#Title

#List of Weapons

#List of damage Types (for use with resistances, to be implemented with damage calculation later on)
damageTypes = ["acid", "bludgeoning", "cold", "fire", "force", "lightning", "necrotic", "piercing", "poison", "psychic", "radiant", "slashing", "thunder"]
weapons = namedtuple('Weapon', 'numDice diceType damageType')

def getWeapons
#input box for skill modifiers
label_atkNum = Label(root, text="Number of Attacks")
atkNumInput = tk.Entry(root)
atkNumInput.insert(0, "1")

label_atkNum.grid(row = 1, column = 0,  pady = 2) 
atkNumInput.grid(row = 1, column = 1,  pady = 2) 

#input box for skill modifiers
label_Prof = Label(root, text="Proficiency")
profInput = tk.Entry(root)
profInput.insert(0, "0")

label_Prof.grid(row = 2, column = 0,  pady = 2) 
profInput.grid(row = 2, column = 1,  pady = 2) 


#input box for skill modifiers
label_Mod = Label(root, text="Skill Modifier")
modInput = tk.Entry(root)
modInput.insert(0, "0")

label_Mod.grid(row = 3, column = 0,  pady = 2) 
modInput.grid(row = 3, column = 1,  pady = 2) 


#input box for any extra modifiers
label_Etc = Label(root, text="Extra Modifiers")
etcInput = tk.Entry(root)
etcInput.insert(0, "0")

label_Etc.grid(row = 4, column = 0,  pady = 2) 
etcInput.grid(row = 4, column = 1,  pady = 2) 


#input box for the Target's Armor Class
label_Armor = Label(root, text="Armor Class")
armorInput = tk.Entry(root)
armorInput.insert(0, "0")

label_Armor.grid(row = 5, column = 0,  pady = 2) 
armorInput.grid(row = 5, column = 1,  pady = 2) 

#dropdown for weapon(to be implemented in the future)

#List of Dice for the rolling function. Any custom Die number entered here MUST start with D. 
#Example: "D16","D2"
diceList = ["D4","D6","D8","D10","D12","D20"]

#input for number of dice
label_Dice = Label(root, text="Roll")
diceNumInput = tk.Entry(root)
diceNumInput.insert(0, "1")


# Create a Tkinter variable for the dice kind
diceVar = StringVar(root)
diceKindInput = OptionMenu(root, diceVar, *diceList)
diceVar.set(diceList[0])



diceNumInput.grid(row = 3, column = 2,  pady = 10, padx = 10)
diceKindInput.grid(row = 3, column = 3,  pady = 2)

def hitCalc():
    rolls = range(19)
    armorClass = int(armorInput.get())
    count = len([i for i in rolls if i + int(profInput.get()) + int(modInput.get()) + int(etcInput.get()) > armorClass]) +1

    hitRate = (count / 20)**(int(atkNumInput.get())) * 100

    chanceMessage = StringVar(root)
    chanceMessage.set(f"There is a {hitRate}% chance to hit.")

    #changes message based on the number of hits.
    if int(atkNumInput.get())>1:
        chanceMessage.set(f"Each attack has a {count/20 * 100} chance to hit. \n The probability of all {int(atkNumInput.get())} attacks hitting is {hitRate}%.")

    messagebox.showinfo('Message', f"{chanceMessage.get()}")

def dmgCalc():
    #Multiply the number of dice variable with the kind of dice variable. Add or subtract weaknesses/resistance(to be added).
    totalDamage = 0
    diceSides = diceVar.get()[1:]
    rollList = []
    for i in range(int(diceNumInput.get())):
        rollResult = random.randint(1,int(diceSides))
        rollList.insert(i-1, rollResult)
        totalDamage = totalDamage + rollResult

    messagebox.showinfo('Message', f"Dealt {totalDamage} damage!")

#button to run program
runHitButton = tk.Button(root, text="Run", padx=10, pady=5, fg="white", bg="green", command=hitCalc)
runHitButton.grid(row = 6, column = 0, columnspan = 2, pady = 0)

runDmgButton = tk.Button(root, text="Calculate Damage", padx=10, pady=5, fg="white", bg="green", command=dmgCalc)
runDmgButton.grid(row = 6, column = 2, columnspan = 2, pady = 0)


root.mainloop()