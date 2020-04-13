import tkinter as tk
from tkinter import Label, LabelFrame, Grid, Entry, messagebox, OptionMenu, StringVar, VERTICAL, ttk
from tkinter import ttk
import os, random, csv
import sqlite3
import pandas as pd
from pandas import DataFrame

root = tk.Tk()



#SECTION 1: VARIABLES

diceList = ["D4","D6","D8","D10","D12","D20"] #List of Dice for the rolling function. Any custom Die number entered here MUST start with D.

diceVar = StringVar(root) #to be used by the diceKindInput widget
diceVar.set(diceList[0])

weapons = ['Select A Weapon'] #Empty list of Weapons to be populated by SQLite
wepVar = StringVar(root) #to be used by the wepInput widget
wepVar.set(weapons[0])


damageTypes = ["Damage Type","acid","bludgeoning","cold","fire","force","lightning","necrotic","piercing","poison","psychic","radiant","slashing","thunder"]#List of damage Types
dmgVar = StringVar(root)
dmgVar.set(damageTypes[0])







#SECTION 2:  SQLite FUNCTIONS

wepDB = sqlite3.connect('DnDapp/weapons.db')#sqlite initiator
c = wepDB.cursor()

#reloads the csv into the database. uncomment if you made any changes to the csv. 
#read_weapons = pd.read_csv (r'DnDapp\weapons.csv')
#read_weapons.to_sql('WEAPONS', wepDB, if_exists='replace', index = False) # Insert the values from the csv file into the table 'CLIENTS' 


def readSqliteTable():  #reads the SQL table and populates the weapons[] list
    try:
        sqliteConnection = sqlite3.connect('DnDapp/weapons.db')
        c = sqliteConnection.cursor()
        print("Connected to Weapons Database")

        sqlite_select_query = """SELECT name from WEAPONS"""
        c.execute(sqlite_select_query)
        records = c.fetchall()
        for row in records:
            weapons.append(f"{row[0]}")
        c.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("The SQLite connection is closed")

def callback(*args): #callback function linked to wepInput used to update the diceNumInput and diceKindInput.
    try:
        sqliteConnection = sqlite3.connect('weapons.db')
        c = sqliteConnection.cursor()

        sqlite_select_query = f"""SELECT * from WEAPONS where name = '{wepVar.get()}'"""
        c.execute(sqlite_select_query)
        records = c.fetchall()
        for row in records:
            diceNumInput.delete(0)
            diceNumInput.insert(0, f'{row[1]}')
            diceVar.set(f'{row[2]}')
            dmgVar.set(f'{row[3]}')
        c.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
readSqliteTable()



# SECTION 3: INPUT BOXES AND UI

#input box for skill modifiers
label_atkNum = Label(root, text="Number of Attacks")
atkNumInput = tk.Entry(root)
atkNumInput.insert(0, "1")

label_atkNum.grid(row = 1, column = 0,  pady = 2, padx=5) 
atkNumInput.grid(row = 1, column = 1,  pady = 2, padx=5) 

#input box for skill modifiers
label_Prof = Label(root, text="Proficiency")
profInput = tk.Entry(root)
profInput.insert(0, "0")

label_Prof.grid(row = 2, column = 0,  pady = 2, padx=5) 
profInput.grid(row = 2, column = 1,  pady = 2, padx=5) 


#input box for skill modifiers
label_Mod = Label(root, text="Skill Modifier")
modInput = tk.Entry(root)
modInput.insert(0, "0")

label_Mod.grid(row = 3, column = 0,  pady = 2, padx=5) 
modInput.grid(row = 3, column = 1,  pady = 2, padx=5) 


#input box for any extra modifiers
label_Etc = Label(root, text="Extra Modifiers")
etcInput = tk.Entry(root)
etcInput.insert(0, "0")

label_Etc.grid(row = 4, column = 0,  pady = 2, padx=5) 
etcInput.grid(row = 4, column = 1,  pady = 2, padx=5) 


#input box for the Target's Armor Class
label_Armor = Label(root, text="Armor Class")
armorInput = tk.Entry(root)
armorInput.insert(0, "0")

label_Armor.grid(row = 5, column = 0,  pady = 2, padx=5) 
armorInput.grid(row = 5, column = 1,  pady = 2, padx=5) 

#separator
ttk.Separator(root,orient=VERTICAL).grid(row=0, column=2, rowspan=6,sticky="ns")

#input for number of dice
label_Dice = Label(root, text="Roll")
diceNumInput = tk.Entry(root)
diceNumInput.insert(0, "1")

diceNumInput.grid(row = 3, column = 3,  pady = 10, padx = 5)

#input for the kind of die used
diceKindInput = OptionMenu(root, diceVar, *diceList)

diceKindInput.grid(row = 3, column = 4,  pady = 2)


#input for the weapon type
wepInput = OptionMenu(root, wepVar, *weapons)
wepInput.grid(row=2, column=3, columnspan=3)
wepVar.trace("w", callback) # Updates the diceKindInput,diceNumInput and dmgInput based on the selected value of wepInput

#input for damage type
dmgInput = OptionMenu(root, dmgVar, *damageTypes)
dmgInput.grid(row=3, column=5) 


# SECTION 4: CALCULATION METHODS

def hitCalc(): #calculates hit chance based on the entered number of attacks, proficiency, and any other modifiers.
    rolls = range(19)
    armorClass = int(armorInput.get())
    count = len([i for i in rolls if i + int(profInput.get()) + int(modInput.get()) + int(etcInput.get()) > armorClass]) +1 #a 20 always hits, but a 1 always misses, leading to a maximum chance of 95%

    hitRate = (count / 20)**(int(atkNumInput.get())) * 100

    chanceMessage = StringVar(root)
    chanceMessage.set(f"There is a {hitRate}% chance to hit.")

    
    if int(atkNumInput.get())>1: #changes message based on the number of hits.
        chanceMessage.set(f"Each attack has a {count/20 * 100} chance to hit. \n The probability of all {int(atkNumInput.get())} attacks hitting is {hitRate}%.")

    messagebox.showinfo('Message', f"{chanceMessage.get()}") 

def dmgCalc(): #rolls the number of dice according to the entered dice kind and number of dice.
    totalDamage = 0
    diceSides = diceVar.get()[1:] #removes the 'D'. TODO: update this so that it removes the character 'D' specifically for the users' sake.
    rollList = []
    for i in range(int(diceNumInput.get())):
        rollResult = random.randint(1,int(diceSides))
        rollList.insert(i-1, rollResult)
        totalDamage = totalDamage + rollResult
    dmgType = StringVar(root)
    dmgType.set("")
    if dmgVar.get() != 'Damage Type':
        dmgType.set(" " + dmgVar.get())
    messagebox.showinfo('Message', f"Dealt {totalDamage}{dmgType.get()} damage!") #TODO: Implement damage type into the message if a weapon was selected.


#SECTION 5: BUTTONS


runHitButton = tk.Button(root, text="Will it Hit?", padx=10, pady=5, command=hitCalc) #button to run the hitCalc method
runHitButton.grid(row = 6, column = 0, columnspan = 2, pady = 0)

runDmgButton = tk.Button(root, text="Calculate Damage", padx=10, pady=5, command=dmgCalc) #button to run the dmgCalc method
runDmgButton.grid(row = 6, column = 3, columnspan = 3, pady = 0)


root.mainloop()