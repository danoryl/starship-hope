from adventurelib import *

### GENERAL ###


Item.immovable = False
Item.drinkable = False
Item.eatable = False
Room.suggestions = ["look around", "look at", "list locations", "go to", "inventory", "take", "drop", "open", "use", "search", "eat", "drink", "save game", "load game", "reset game"]
Room.items = Bag() ### FAILSAFE

planet_list = ["eos"] ### ready for an expansion of the game




### START AND STARSHIP HOPE ###

space = Room("""
You are drifting in space. Luckily you have your spacesuit on, or it would be a very short adventure.

You see the familiar silhouette of the Starship Hope not far from your position. It seems completely dead, all lights off and no sign of power on your spacesuit scanner. The airlock is open like a silent invite to enter. It feels like a trap, or a hint from the game developer.
""")
space.name = 'space'
space.loc = 'space'
space.suggestions = ["look around", "look at", "list locations", "enter airlock", "inventory", "take", "drop", "save game", "load game", "reset game"]

## Deck 1

lab = Room("""The scientific lab is Ian's playground, so you should be careful what you touch. It's also where you can look at the stars, but not for romantic matters. There's an holographic astrometry station that can scan for nearby systems.
""")
lab.name = 'lab'
lab.loc = "deck 1"

bridge = Room("""
The bridge is where you fly the ship. Surprise! If you entered here, it means you must be a big shot in the ship. Or an Ensign in training. Or a cat, cats are always welcome here. Other than the captain's and first officer's chairs, there's the helm and a weapons console which you shouldn't really use. No really, don't.
""")
bridge.name ='bridge'
bridge.loc = "deck 1"
bridge.suggestions = ["set course to", "look around", "look at", "list locations", "go to", "inventory", "take", "drop", "open", "use", "eat", "drink", "save game", "load game", "reset game"]

briefing_room = Room("""
The briefing room is where all the meetings between the officers happen. You know, the historical stuff, like to plan the next strategy against Venster, or what to eat for lunch. There's a big round table (not <i>that</i> round table!) and a even bigger screen connected to the main computer.
""")
briefing_room.name = 'briefing room'
briefing_room.loc = "deck 1"

## Deck 2

airlock = Room("""
The airlock of the spaceship is shiny and white, with thousands
of small, red, blinking lights. They probably indicate that everything is safe and you can finally explore the ship. Red is good, right?
""")
airlock.name = 'airlock'
airlock.loc = "deck 2"

lift = Room("""
The fastest turbolift in the fleet. So fast that sometimes it starts before you choose the destination!
""")
lift.name = 'lift'
lift.loc = "deck 2"

crew_quarters = Room("""
I AM THE WAY INTO THE DOLEFUL CITY,<br>
I AM THE WAY INTO ETERNAL GRIEF...<br>
No, just kidding. It's the crew quarters corridor, where you can find all the private rooms. You shouldn't violate privacy, right? ;)
""")
crew_quarters.name = 'crew quarters'
crew_quarters.loc = "crew quarters"

aria_room = Room("""
The first officer room has all the feminine touch that you need. Racks of weapons, including her powerful silahas, are stacked on the walls. Oh, and flowers.
""")
aria_room.name = 'Aria room'
aria_room.loc = "officer room"


ian_room = Room("""
Ian's room is the image of his genius. It's a perfect, very tidy room, with pictures of Aria hanging on the wall and a lot of scientific books that he saved from destruction during the Venster invasion. You read some titles wondering which mysteries they might reveal: <i>"Sword Art Online", "Kimetsu no Yaiba", "One Piece"...</i>
""")
ian_room.name = 'Ian room'
ian_room.loc = "officer room"


buzz_room = Room("""
Buzz's room is almost completely empty. He's an Atarian, so he doesn't need a room. But if I didn't include one, players would ask "why there's no room for Buzz?", and I didn't want to code the function. But wait, maybe there's something useful here after all...
""")
buzz_room.name = 'Buzz room'
buzz_room.loc = "officer room"


henry_room = Room("""
Henry's room is the biggest one. But not because he's the biggest gui, just because he's the captain, and there must be something good in being the captain, right? The room is a bit messy, but that's no sign of fight. It's always like this.
""")
henry_room.name = 'Henry room'
henry_room.loc = "officer room"


mess = Room("""
The mess hall is where the crew gathers to eat and have fun. There a latest (and also first) model of food replicator, an almost endless supply of Chicken flavored coke already replicated by Henry, and some tables, which I included for a reason, right?
""")
mess.name = 'mess'
mess.loc = "deck 2"
mess.suggestions = ["look around", "look at", "list locations", "go to", "inventory", "take", "drop", "open", "use", "replicate","eat", "drink", "save game", "load game", "reset game"]

## Deck 3

engineering = Room("""
The engineering room is where the HyperSphere can freely singurgle and you can hear it (because in space you can't, as everyone knows). 
""")
engineering.name = 'engineering'
engineering.loc = "deck 3"

hangar = Room("""
The hangar is where the only shuttle of the Hope is parked. You could directly land the Hope, but it's big and it would need a lot of space, or destroy part of the landing site. You could also use Buzz's teleportation skills, but...oh well, use the damn shuttle and don't complain!
""")
hangar.name = 'hangar'
hangar.loc = "hangar"

shuttle = Room("""
The best shuttle in the fleet. It has all you need: it can fly, you can land on a planet, and it does make a great coffee, but not now because the coffee maker is broken.
""")
shuttle.name = "shuttle"
shuttle.loc = "shuttle"
shuttle.suggestions = ["look around", "look at", "list locations", "enter airlock", "inventory", "take", "drop", "save game", "load game", "reset game", "land to"]



## Items

starship = Item("The Starship Hope", "starship hope", "hope")
starship.description = "The Starship Hope is a beautiful sight. It's silhouette is so famous that I really don't have to describe it to you. The only important thing here is the open airlock, but I've already told you."
starship.immovable = True

coke = Item("can of chicken flavored coke", "coke")
coke.drinkable = True
coke.description = "A nice cold chicken flavored coke. The favorite of Captain Shepard!"

map = Item("map of the Starship Hope", "map")
map.description = "The map shows the Starship Hope three decks, with all the available rooms. You can transfer it to your suit computer if you want, unless you want to blindly wander into the ship."


wrench = Item("simple positronic multifunction wrench", "wrench")
wrench.description = "A tool used by engineers to fix stuff. Engineers stuff, you know...but it seems there'a an empty space for...something."


ian_chip = Item("Ian custom chip", "chip", "ian chip")
ian_chip.description = "This is a custom chip designed by Ian to augment the capabilities of many tools. If you try use it on a tool, you'll see what I mean."


ian_tool = Item("Ian Volk super multitool", "multitool")
ian_tool.description = "A simple positronic multi-wrench enhanced by Ian Volk's genius"

ian_tool_coke = Item("Ian's super multitool coke enhanced", "coke multitool")
ian_tool_coke.description = "A simple positronic multi-wrench enhanced by Ian Volk's genius and the best drink in the universe: chicken flavored coke!"

food_replicator = Item("food replicator", "replicator")
food_replicator.description = "The best food replicator on the Starship Hope. Well, it's the only one, so... You can use it to replicate any kind of food. If you ask for anything that is not food, it will replicate food in the shape of what you ask. So you can't replicate a super weapon, sorry."
food_replicator.immovable = True

officer_badge = Item("officer badge")
officer_badge.description = "This badge is only for bridge officers. It's strictly forbidden to wear it if you are not allowed on the bridge! Strictly! I see you."

pile_uniforms = Item("pile of captain's uniforms on the bed","uniforms")
pile_uniforms.description = "A pile of Henry's uniforms casually spread out on the bed like a work of contemporary art."
pile_uniforms.immovable = True

hypersphere_console = Item("Hypersphere control console", "hypersphere console")
hypersphere_console.description = "A lot of shiny buttons. Does anyone of them starts the Hypersphere?"
hypersphere_console.immovable = True

tools_cabinet = Item("Engineering tools cabinet", "tools cabinet")
tools_cabinet.description = "A cabinet where Engineers should put all the tools they need. Sometimes they forget, though..."
tools_cabinet.immovable = True

buzz_locker = Item("Buzz private locker", "buzz locker")
buzz_locker.description = "Buzz private locker. Since an Atarian doesn't really need a locker, it's usually unlocked and empty. But you shoud try..."
buzz_locker.immovable = True

buzz_phaser = Item("phaser")
buzz_phaser.description = "A powerful phaser. You know what a phaser is, don't you?"

photos_pile = Item("Pile of AI generated sexy images of Aria", "images pile")
photos_pile.description = "A pile of AI generated images of Aria Marconi in sexy outfits. Oh Ian, better not to tell Aria you make this stuff..."
photos_pile.immovable = True

chips_pile = Item("pile of used microchips", "pile of chips")
chips_pile.description = "A pile of used microchips. Maybe there's something useful inside?"
chips_pile.immovable = True

ipod = Item("iPod")
ipod.description = "An old iPod from Earth. Try listen to it, it might contain good music!"


astrometry_console = Item("Astrometry console", "astrometry console")
astrometry_console.description = "This console allows you to search for planets and explore the universe, all from the comfort of your spaceship. Convenient, uh?"
astrometry_console.immovable = True

venster = Item("big, ugly, potato shaped Venster", "venster")
venster.description = "A big, ugly, potato shaped Venster. He's trying to access the Hypersphere from the console. You are the only one who can stop him!"
venster.immovable = True

venster_dead = Item("dead Venster", "dead venster")
venster_dead.description = "A Venster in his best form: dead!"
venster_dead.immovable = True


venster_digital_map = Item("digital map of a planetary system", "venster planetary map", "venster map")
venster_digital_map.description = "This map shows a planetary system controlled by Venster. Maybe it could be useful to use it in the Astrometry lab?"


silaha = Item("powerful and scary looking pair of silaha", "silaha")
silaha.description = "Aria Marconi's favorite weapon. Silahas can be used in close combat, similar to lightsabers, but also as ranged energy weapons. Deadly, in the right hands."

ian_room_keypad = Item("Ian's room keypad", "ian keypad")
ian_room_keypad.description = "Keypad to control access to Ian's Room"
ian_room_keypad.immovable = True

aria_room_keypad = Item("Aria's room keypad", "aria keypad")
aria_room_keypad.description = "Keypad to control access to Aria's Room"
aria_room_keypad.immovable = True

buzz_room_keypad = Item("Buzz's room keypad", "buzz keypad")
buzz_room_keypad.description = "Keypad to control access to Buzz's Room"
buzz_room_keypad.immovable = True

henry_room_keypad = Item("Henry's room keypad", "henry keypad")
henry_room_keypad.description = "Keypad to control access to Henry's Room"
henry_room_keypad.immovable = True

briefing_room_computer = Item("Briefing Room computer", "briefing computer")
briefing_room_computer.description = "This is the main terminal of the Briefing Room. Usually stores missions and crew logs, as well as other data that you really shouldn't look at."
briefing_room_computer.immovable = True

mess_tables = Item("mess tables", "tables")
mess_tables.description = "There are 10 tables in the little mess of the Starship Hope. Are them here only as support for the food?"
mess_tables.immovable = True

nav_console = Item("Navigation console", "navigation", "helm")
nav_console.description = "The navigation console, or helm, is used to fly the ship. Not a really surprising information."
nav_console.immovable = True

weapon_console = Item("Weapons and security console", "weapons")
weapon_console.description = "This is where you can fire the powerful Hope weapons. You really shouldn't do it. Really."
weapon_console.immovable = True

shuttle_key_cab = Item("Shuttle key cabinet")
shuttle_key_cab.description = "Contains the key to open the shuttle. You need a security badge to open it."
shuttle_key_cab.immovable = True

shuttle_key = Item("Shuttle key")
shuttle_key.description = "This key is necessary to open the shuttle hatch."

security_badge = Item("Security badge")
security_badge.description = "This badge allows you to open restricted areas and objects."

inventory = Bag()

# Dictionary used by the food replicator in the Mess
user_food = {}


## Room items

space.items = Bag([
    coke, starship,
])


airlock.items = Bag([
    map,
])

mess.items = Bag([
    food_replicator, coke, ian_chip, mess_tables
])

lab.items = Bag([
    chips_pile, astrometry_console
])

engineering.items = Bag([
    wrench, tools_cabinet, hypersphere_console, venster, venster_dead, venster_digital_map,
])

crew_quarters.items = Bag([
    ian_room_keypad, aria_room_keypad, buzz_room_keypad, henry_room_keypad,
  
])

ian_room.items = Bag([
    photos_pile, ipod,
  
])

henry_room.items = Bag([
    officer_badge, pile_uniforms
  
])

aria_room.items = Bag([
    silaha,
  
])

buzz_room.items = Bag([
  buzz_locker, buzz_phaser,
])

briefing_room.items = Bag([
  briefing_room_computer,

])

hangar.items = Bag([
  shuttle_key_cab, shuttle_key,
])

bridge.items  = Bag([
  nav_console, weapon_console, security_badge,
])



### OBJECTS IN ROOMS / INVENTORY COUNT ###

objects_count = {
  'space': {
      coke.name: 1,
      starship.name : 1,
            
    },
  
  'airlock': {
      map.name : 1,
    },

  'mess': {
      food_replicator.name : 1,
      coke.name : 20,
      mess_tables.name: 1,
      ian_chip.name: 1,
   
    },

  'lab': {
      astrometry_console.name : 1,
      chips_pile.name : 1,
      
    },

  'engineering': {
      wrench.name : 1,
      tools_cabinet.name : 1,
      hypersphere_console.name : 1,
      venster.name : 1,
      venster_dead.name: 1,
      venster_digital_map.name: 1,
      
  },

  'ian room': {
      photos_pile.name : 1,
      ipod.name : 1,
  
  },

  'henry room': {
      officer_badge.name : 1,
      pile_uniforms.name: 1,
  
  },

  'aria room': {
      silaha.name : 1,
  
  },

  'buzz room': {
      buzz_locker.name : 1,  
      buzz_phaser.name : 1,
  },

  "crew quarters" : {
    ian_room_keypad.name : 1,
    aria_room_keypad.name : 1,
    buzz_room_keypad.name : 1,
    henry_room_keypad.name : 1,
  },

  'briefing room': {
      briefing_room_computer.name : 1,
  
  },

  'hangar': {
      shuttle_key_cab.name: 1,
      shuttle_key.name: 1,
  },

  'bridge': {
    nav_console.name : 1,
    weapon_console.name : 1,
    security_badge.name: 1,
  },

  'lift': {
    
  },

  'shuttle': {
    
  },
  
  'inventory': {
      
  },
}

### ALL ROOMS AND AVAILABLE ROOMS FOR A LOCATION ###
## Dictionary to control which rooms are available in a certain location

all_rooms = {"space":["airlock"], "deck 1": ["lab", "lift", "briefing room", "bridge"], "deck 2": ["airlock", "lift", "crew quarters", "mess"], "crew quarters": ["Aria room", "Ian room", "Buzz room", "Henry room", "airlock", "lift", "Mess"], "officer room" : ["crew quarters"], "deck 3": ["engineering", "lift", "hangar"], "hangar": ["engineering", "lift", "shuttle"], "shuttle": ["hangar"] }
