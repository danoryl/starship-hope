from adventurelib import *
from rooms_items import *
from flask_login import current_user
import random
import re



random_answers = {
  'random_lookaround' : ["You still have eyes. Luckily the Venster didn't rip them off your face. You look around in the room.", "Your eyes scan the room, and it looks back as if to say, \"Well, what do you think?\"", "You look around the room. You find the missing sock your are always looking for, but as soon as you look away, it's gone", "You look around the room. You have the strong feeling that a Venster is hidden behind the curtains, but luckily there are no curtains.", "You look around the room. You hope to find love here, but the room breaks your heart", "As you look around the room, you almost espect the Holographic Doctor to appear. But this ain't the Voyager, Einstein!", "You examine the room, secretly hoping you'll discover the <i>Instant Pizza</i> button hidden among the switches", "As you examine the room, you can't help but wonder how much would the furniture be worth on the black market."]
}

game_response_die_addon = "<br> Luckily this is just a game and you can restart.<br><br>" + str(space) # string to add everytime player dies and game must reset. One place to avoid to have to modify the string everytime

  
def create_html_list(list, nocount=False, inv=False):
    '''Iterate through rooms and bags and create a list for the GUI'''
    html_list = ""
    game_data = current_user.get_game_data()
    if nocount == False: # List of items in Bags. Items are objects
        html_list = "<ul>"
        if inv == False:
            for item in list:
                if item.name in game_data['unlisted']:
                    continue
                count = game_data['objects_count'][game_data['current_room'].name.lower()][item.name]
                html_list += "<li> " + str(count) + "x <a href='javascript:void(0);' onclick=\"sendInput('take " + str(item.aliases[-1]) + "')\" style=\"color: white\">" + str(item) + "</a> <i>(" + str(item.aliases[-1]) + ")</i></li>"
        else:
            for item in list:
                count = game_data['objects_count']['inventory'][item.name]
                html_list += "<li> " + str(count) + "x <a href='javascript:void(0);' onclick=\"sendInput('drop " + str(item.aliases[-1]) + "')\" style=\"color: white\">" + str(item) + "</a> <i>(" + str(item.aliases[-1]) + ")</i></li>"
        html_list += "</ul>"          
    if nocount == True: # List of rooms. Items are strings
        html_list = "<ul>"
        for item in list:
            if item == game_data['current_room'].name:
                continue
            html_list += "<li> " + str(item) + "</li>"
        html_list += "</ul>"  
    if html_list == "": html_list = "Empty"
  
    return html_list

def split_numbers_and_words(input_string):
    '''Takes a string in the form "number object" and return two separate variables number and item'''
    pattern = r'(\d+)\s+([A-Za-z]+)'

    # Use re.findall to find all occurrences of the pattern in the input string
    matches = re.findall(pattern, input_string)
    if matches == []:
        number = 1
        item = input_string
    else:
        number = int(matches[0][0])
        item = matches[0][1]
    
    return number, item
  

def find_room(room_name):
    '''Finds a room and return it as an object'''
    for variable_name, variable_value in globals().items():
        if isinstance(variable_value, Room) and variable_value.name.lower() == room_name.lower():
            return variable_value  # Return the room object if the name matches
  
    return None  # Return None if the room doesn't exist

def room_items():
    """
    Returns the correct room items object in game_data dictionary
    """
    
    game_data = current_user.get_game_data()
    return game_data[game_data['current_room'].name.lower() + " items"]

def energy(updown, number):
    '''Increases and decreases player energy'''
    game_data = current_user.get_game_data()
    if updown == 'up':
        if (game_data['player_energy'] + number) >= 100:
            game_data['player_energy'] = 100
            game_data['gui']['energy'] = game_data['player_energy']
        else:
            game_data['player_energy'] += number
            game_data['gui']['energy'] = game_data['player_energy']
    else:
        if (game_data['player_energy'] - number) <= 0:
            game_data['player_energy'] = 0
            reset_game(f"You lost all energy, so you are dead! <br> {game_response_die_addon}")
            return
        else:
            game_data['player_energy'] -= number
            game_data['gui']['energy'] = game_data['player_energy']
    current_user.set_game_data(game_data)  
    

@when("init gui")
def init_gui():
    '''Initializes GUI at first launch'''
    game_data = current_user.get_game_data()
    if game_data['start']:
        response = f"Welcome {current_user.username}<br>{str(space)}"
    else:
        response = "Welcome back, " + current_user.username
    if game_data['current_room'].name != "space" and not game_data['inventory'].find("map"):
        room_loc = "nomap"
    elif game_data['current_room'].name == "lift":
        room_loc = f"Lift {game_data['current_room'].loc}"
    else:  
        room_loc = game_data['current_room'].loc.capitalize()  
    game_data['gui'] = {
      'game_response': response,
      'room_loc': room_loc,
      'room_name': game_data['current_room'].name.capitalize(),
      'room_desc': game_data['current_room'].description,
      'inventory': create_html_list(game_data['inventory'], inv=True),
      'room_items': create_html_list(room_items()),
      'energy': game_data['player_energy'],
      'suggestions' : game_data['current_room'].suggestions,
      }
    game_data['start'] = False
    current_user.set_game_data(game_data) 
    return game_data['gui']


def update_gui(response):
    '''Updates GUI data with game data and custom game response'''
    game_data = current_user.get_game_data()
    if game_data['current_room'].name != "space" and not game_data['inventory'].find("map"):
        game_data['gui']['room_loc'] = "nomap"
    elif game_data['current_room'].name == "lift":
        game_data['gui']['room_loc'] = f"Lift {game_data['current_room'].loc}"
    else:  
        game_data['gui']['room_loc'] = game_data['current_room'].loc.capitalize()
    game_data['gui']["game_response"] = response
    game_data['gui']["room_desc"] = game_data['current_room'].description
    game_data['gui']["room_items"] = create_html_list(room_items())
    game_data['gui']["inventory"] = create_html_list(game_data['inventory'], inv=True)
    game_data['gui']['energy'] = game_data['player_energy']
    game_data['gui']['suggestions'] = game_data['current_room'].suggestions
    game_data['gui']['room_name'] = game_data['current_room'].name.capitalize() 
    current_user.set_game_data(game_data) 
  
@when('reset game')
def reset_game_manual():
    '''Command to manually reset the game. Sends a custom response to main reset game function'''
    reset_game("You kill yourself. Did you know it was going to happen?" + game_response_die_addon)

def reset_game(game_response):
    '''Resets the game to initial state with a custom game response'''
    state_reset = dict(state)
    state_reset['start'] = False
    current_user.set_game_data(state_reset)
    update_gui(game_response)
        
 
@when('look around')
def look_around():
    ''' Describes the room and items inside with a random response'''
    game_data = current_user.get_game_data()  
    if game_data['current_room'].name == "space":
        update_gui(str(game_data['current_room'])+ "<br><br>Here you see:<br>" + create_html_list(room_items()))
        return
    update_gui(random.choice(random_answers['random_lookaround']) + "<br><br>" + str(game_data['current_room'])+ "<br><br>Here you see:<br>" + create_html_list(room_items()))
    

@when('look at ITEM')
def look_at(item):
    '''Describes an item and shows the short name to the user'''
    game_data = current_user.get_game_data()
    if game_data['current_room'].items.find(item):
        obj = game_data['current_room'].items.find(item)
        game_data['gui']["game_response"] = f"{obj.description}<br><br> Short name: {obj.aliases[-1]}"
    elif game_data['inventory'].find(item):
        obj = game_data['inventory'].find(item)
        game_data['gui']["game_response"] = f"{obj.description}<br><br> Short name: {obj.aliases[-1]}"
    else:
        game_data['gui']["game_response"] = f"There is no {item} here."

@when('enter airlock')
def enter_airlock():
    '''Enters the airlock from space'''
    game_data = current_user.get_game_data()
    if game_data['current_room'].name == "space":
        game_data['current_room'] = airlock
        current_user.set_game_data(game_data)
        update_gui("You enter the airlock" + "<br><br>Here you see:<br>" + create_html_list(room_items()))
        energy('down',2)
    else:
        game_data['gui']["game_response"] = "You are not in space"
     

@when('go to LOCATION')
def go(location):
    '''Move to any location available in the current location'''
    game_data = current_user.get_game_data()
    game_data['context'] = None
    if location.lower() not in [room.lower() for room in all_rooms[game_data['current_room'].loc]] and game_data['current_room'].name != "lift":
        game_data['gui']["game_response"] ="Location not available"
        return
    ## Context
    if location == "mess":
        game_data['context'] = "mess"
    elif location == "shuttle":
        if not game_data['inventory'].find('shuttle key'):
            game_data['gui']["game_response"] ="You cannot access the shuttle without a key"
            current_user.set_game_data(game_data)  
            return
        else:
            game_data['context'] = "shuttle"
    elif location == "bridge":
        if not game_data['inventory'].find('officer badge'):
            game_data['gui']["game_response"] ="You cannot access the bridge without an officer badge"
            current_user.set_game_data(game_data)  
            return
        else: 
            game_data['context'] = "bridge"
    ## LIFT ##
    if location in ["deck 1", "deck 2", "deck 3"] and game_data['current_room'].loc != location:
        game_data['current_room'].loc = location.lower()
        current_user.set_game_data(game_data) 
        update_gui(f"You arrive at {location}. These are all available locations: <br><br>" + create_html_list(all_rooms[game_data['current_room'].loc], nocount=True))
        return
    if location.lower() == "lift" and game_data['current_room'].loc in ["deck 1", "deck 2", "deck 3", "crew quarters", "hangar"]:
        if game_data['current_room'].loc == "crew quarters":
            location_saved = "deck 2"
        elif game_data['current_room'].loc == "hangar":
            location_saved = "deck 3"
        else:
            location_saved = game_data['current_room'].loc
        game_data['current_room'] = lift
        game_data['current_room'].loc = location_saved
        if game_data['current_room'].loc == "deck 1":
            update_gui("You enter the lift. <br> You are on deck 1, you can choose to go to deck 2 or 3")
        elif game_data['current_room'].loc == "deck 2":
            update_gui("You enter the lift. <br> You are on deck 2, you can choose to go to deck 1 or 3")  
        else:
            update_gui("You enter the lift. <br> You are on deck 3, you can choose to go to deck 1 or 2")  
        current_user.set_game_data(game_data)
        energy('down',1)
        return
    if location.lower() == "lift" and game_data['current_room'].loc not in ["deck 1", "deck 2", "deck 3", "crew quarters", "hangar"]:
        game_data['gui']["game_response"] ="Location not available"
        current_user.set_game_data(game_data)
        return
    ## END LIFT
    new_room = find_room(location)
    if new_room.name in game_data['locked']:
        game_data['gui']["game_response"] ="You are not authorized to enter this room. You might need something to bypass the lock..."
        return
    if game_data['current_room'].name == "space":
        enter_airlock()
        return
    if game_data['current_room'] == new_room:
        game_data['gui']["game_response"] = f"You are already in {location}"
    else:  
        game_data['current_room'] = new_room
        current_user.set_game_data(game_data)
        update_gui(f"You go to {location}<br><br>{str(game_data['current_room'])}" + "<br><br>Here you see:<br>" + create_html_list(room_items()))
        energy('down',1)
    

@when('list locations')
def list_locs():
    '''Lists all available locations'''
    game_data = current_user.get_game_data()
    game_data['gui']["game_response"] = create_html_list(all_rooms[game_data['current_room'].loc], nocount=True)
    
    

@when('inventory')
def show_inventory():
    '''Lists items in user inventory'''
    game_data = current_user.get_game_data()
    if not game_data['inventory']:
        game_data['gui']['game_response'] = "You look at your bag, but sadly only a stowaway fly gets out."
        return
    update_gui(f"You open your bag and look at all the things you've got<br><br>{create_html_list(game_data['inventory'], inv = True)}")
    

@when('take WHAT')
def take_item(what):
    """Takes an item from the current room and places to inventory"""
    
    game_data = current_user.get_game_data()
    number, item = split_numbers_and_words(what)
    obj = room_items().find(item)
    if not obj or obj.name in game_data['unlisted']:
        game_data['gui']["game_response"] = f'There is no {item} in this room.'
        return
    if obj.immovable:
        game_data['gui']["game_response"] = f"You can't take {item}"
        return
    ## check if the user requested more item than available
    if number >= game_data['objects_count'][game_data['current_room'].name.lower()][obj.name]:
        number = game_data['objects_count'][game_data['current_room'].name.lower()][obj.name]
        room_items().take(item)
    else:
        game_data['objects_count'][game_data['current_room'].name.lower()][obj.name] -= number
    if not game_data['inventory'].find(item):
    #if an item is not in inventory it will add the item to the inventory and update the count
        game_data['inventory'].add(obj)
        game_data['objects_count']['inventory'][obj.name] = number
    else:
    #if the item is already in the inventory, it just updates the count  
        game_data['objects_count']['inventory'][obj.name] += number
    current_user.set_game_data(game_data)
    update_gui(f"You take {number} {item}<br> {obj.description}<br>Short name: {obj.aliases[-1]}")
   
@when('drop WHAT')
def drop_item(what):
    """Drops an item from the user inventory into the current room"""
  
    game_data = current_user.get_game_data()
    number, item = split_numbers_and_words(what)
    obj = game_data['inventory'].find(item)
    if not obj:
        game_data['gui']["game_response"] = f'There is no {item} in your inventory.'
        return
    # check if user requested more items than in inventory
    if number >= game_data['objects_count']['inventory'][obj.name]:
        obj = game_data['inventory'].take(item)
        number = game_data['objects_count']['inventory'][obj.name]
    else:
        game_data['objects_count']['inventory'][obj.name] -= number  
    if not room_items().find(item):
    #if the item is not in current room, adds it to the room bag 
        room_items().add(obj)
        game_data['objects_count'][game_data['current_room'].name.lower()][obj.name] = number
    else:        
    #if the item is already in current room, just updates the count
        game_data['objects_count'][game_data['current_room'].name.lower()][obj.name] += number
    current_user.set_game_data(game_data)          
    update_gui(f"You drop {number} {item}")
    
      
@when('drink WHAT')
def drink_item(what):
    '''Drinks an item from the user inventory'''
    game_data = current_user.get_game_data()
    number, item = split_numbers_and_words(what)
    obj = game_data['inventory'].find(item)
    if not obj:
        game_data['gui']["game_response"] = f'There is no {item} in your inventory.'
        return  
    if obj.drinkable:
        if number >= game_data['objects_count']['inventory'][obj.name]:
            obj = game_data['inventory'].take(item)
            number = game_data['objects_count']['inventory'][obj.name]
        else:
            game_data['objects_count']['inventory'][obj.name] -= number 
        current_user.set_game_data(game_data)  
        energy('up',number*20)
        update_gui(f'You drink {number} {item}. You feel very refreshed!')
    else:
        game_data['gui']["game_response"] = f"You can't drink {item}, you silly!"
    
            
      
@when('eat WHAT')
def eat_item(what):
    '''Eats an item from the user inventory'''
    game_data = current_user.get_game_data()
    number, item = split_numbers_and_words(what)
    obj = game_data['inventory'].find(item)
    if not obj:
        game_data['gui']["game_response"] = f'There is no {item} in your inventory.'
        return  
    if obj.drinkable:
        if number >= game_data['objects_count']['inventory'][obj.name]:
            obj = game_data['inventory'].take(item)
            number = game_data['objects_count']['inventory'][obj.name]
        else:
            game_data['objects_count']['inventory'][obj.name] -= number 
        current_user.set_game_data(game_data)  
        energy('up',number*20)
        update_gui(f'You eat {number} {item}. You feel full!')
    else:
        game_data['gui']["game_response"] = f"You can't eat {item}, you silly!"

@when('replicate FOOD')
def replicate_food(food):
    '''Function used by the food replicator in the Mess'''
    game_data = current_user.get_game_data()
    if game_data['context'] != "mess": 
        game_data['gui']["game_response"] = "Replicator not available"
        return
    number, item = split_numbers_and_words(food)
    if not game_data['inventory'].find(item):
        game_data['user_food'][item] = Item(item)
        game_data['user_food'][item].eatable = True
        game_data['user_food'][item].drinkable = True
        game_data['objects_count']['inventory'][item] = number
        game_data['inventory'].add(game_data['user_food'][item])
    else:
        game_data['objects_count']['inventory'][item] += number
    current_user.set_game_data(game_data)  
    update_gui(f"You replicated {number} {item}")

@when("open WHAT")
def open_item(what):
    '''Open objects in the game'''
    game_data = current_user.get_game_data()
    if room_items().find(what):
        obj = room_items().find(what)
    elif game_data['inventory'].find(what):
        obj = game_data['inventory'].find(what)
    else:
        game_data['gui']['game_response'] = f"{what} not found"
        return
    # cases  
    if obj.name == tools_cabinet.name:
        try: 
            game_data['unlisted'].remove(wrench.name)
            update_gui(f"You open the tools cabinet, that reveals it's content.<br>You found a {wrench.name}")
        except ValueError:
            update_gui("The tools cabinet is already open.")
    elif obj.name == buzz_locker.name:
        try: 
            game_data['unlisted'].remove(buzz_phaser.name)
            update_gui(f"You open Buzz's locker, that reveals it's content.<br>You found a {buzz_phaser.name}")
        except ValueError:
            update_gui("Buzz's locker is already open.")
    elif obj.name == shuttle_key_cab.name:
        if game_data['inventory'].find("security badge"):
            try:
                game_data['unlisted'].remove(shuttle_key.name)
                update_gui(f"You open the shuttle key cabinet, that reveals it's content.<br>You found a {shuttle_key.name}")  
            except ValueError:
                update_gui("The shuttle key cabinet is already open.")
        else:
            update_gui("You need a security key to open this cabinet. Where did you see this word before?")
            
        
        
    else: 
        game_data['gui']["game_response"] = f"{what} can't be opened"
    current_user.set_game_data(game_data) 

@when("use WHAT")
def use(what):
    '''Use an object. If the input contains two items in the form "item1 on item2" or "item 1 with item2" redirects to another function'''
    pattern = r'\b(on|with)\b'
    if re.search(pattern, what):
        items = re.split(pattern, what, maxsplit=1)
        item1, item2 = items[0].strip(), items[2].strip()
        use_with(item1,item2)
        return
    
    game_data = current_user.get_game_data()
    obj = check_items(what)
    if not obj:
        game_data['gui']["game_response"] = f"{what} not found"
        return
    
    ## iPod  
    if obj.name == ipod.name:
        game_data['gui']["game_response"] = "You put your headphones on, anticipating the beautiful music stored on this old iPod. But the only track available is named \"Not really important message, do not listen if you are a Venster\". You press play, and a message starts playing:<br><br> <i>This is Ian Volk, of the Starship Hope. If you found this message, you probably boarded the Hope after we were taken away. Or I forgot to delete it and gave it to you. In this case you should not listen to it. But if you are on the Hope and you need to repair the Hypersphere that we sabotaged...well, I don't want to help the Venster by giving you the exact instructions. Just know that Henry's chicken flavored coke is not good only as a drink...ok, now end recording. Oh wow, I recorded it in one go. I didn't know I was able to. Now back to hiding, I hope the Venster will not find us and they will not understand the secret message I've hidden in the recording. It would be so bad if they knew that to repair the Hypersphere it's enough to add coke into...</i> <br><br>The recording ends abruptly. Can you figure out what to do?"
    ## Astrometry console  
    elif obj.name == astrometry_console.name:
        if game_data['venster_map'] == False:
            game_data['gui']["game_response"] = "You scan for nearby habitable worlds, but you find nothing. You need a hint to pinpoint the right planet to set course to, but how?"
        else:
            if game_data['briefing_diary'] == False:
                game_data['gui']["game_response"] = "The holographic display shows again the map of a far solar system appears, with a planet marked as Eos. Why is this system so important that a Venster carried a map on himself? Maybe a trip to the briefing room might clarify..."
            else:
                game_data['gui']["game_response"] = "The holographic display shows again the map of a far solar system, with a planet marked as Eos. Is this where the Venster brought the crew of the Hope? What are you still doing here? Go investigate!"
      
    ## Briefing room computer  
    elif obj.name == briefing_room_computer.name:      
        game_data['briefing_diary'] = True
        game_data['gui']["game_response"] = "The computer screen shows a video of Henry Shepard, whispering a message. <br><br><i>Hello. This is Henry Shepard, captain of the Starship Hope. I don't have much time. The Venster are coming for me and my first officer, they've already captured Ian and confined Buzz to a special quantum antienergy cage, whatever it is. Before being captured, Ian disabled the Hypersphere so that the Venster couldn't use the ship. I don't know why the Venster want the Hope, but at least this bought us some time. I've heard they want to take us on some planet to interrogate us. If you find this message, please alert the Fleet. Do not, I repeat do not try to repair the Hope and come to get us. Unless you are an hero of a game, then please come and save us...</i><br><br>The message suddenly stops. What will you do now?"
    ## Activate navigation control in Bridge
    elif obj.name == nav_console.name:
        if game_data['hypersphere_status'] == False:
            game_data['gui']["game_response"] = "The Hypersphere is offline. You need to repair it first."
            return
        game_data['nav console'] = True
        game_data['gui']["game_response"] = "You activated the navigation console of the Starship Hope. You can now set a course to wherever you want!"
    elif obj.name == weapon_console.name:
        if game_data['hypersphere_status'] == False:
            game_data['gui']["game_response"] = "The Hypersphere is offline. You need to repair it first."
            return
        game_data['gui']["game_response"] = "You fire the powerful weapons of the Hope, killing some subspace lifeform. Are you happy?"  
    
    else:
        game_data['gui']["game_response"] = f"You can't use {what}"

    current_user.set_game_data(game_data) 

def use_with(item1, item2):
    '''Function to handle use of multiple objects'''
    game_data = current_user.get_game_data()
    obj1, obj2 = check_items(item1, item2) #check if item is in inventory or an immovable object in the room
    if not obj1 and not obj2:
        game_data['gui']["game_response"] = f"{item1} and {item2} not found"
        return
    if not obj1:    
        game_data['gui']["game_response"] = f"{item1} not found"
        return
    if not obj2:
        game_data['gui']["game_response"] = f"{item2} not found"
        return
    if obj1.name == obj2.name:
        game_data['gui']["game_response"] = f"You cannot use {obj1.name} on itself!"
        return
    
    # If the Venster is still alive, any attempt to fix the Hypersphere will result in an attack from the Venster
    if (obj1.name == hypersphere_console.name or obj2.name == hypersphere_console.name) and venster_dead.name in game_data['unlisted']: 
        lost_phealth = random.randint(10,15)
        game_data['player_energy'] -= lost_phealth
        if game_data['player_energy'] <= 0:
            reset_game(f"Haven't you seen the big ugly Venster in front of the console? Well, he saw you and shot you with his potato phaser. You loose {lost_phealth} and you die horribly while the Vensters laughs at you!<br> {game_response_die_addon}") 
            return
        current_user.set_game_data(game_data)  
        update_gui(f"Haven't you seen the big ugly Venster in front of the console? Well, he saw you and shoots you with his potato phaser. You loose {lost_phealth} and you now have {game_data['player_energy']} health points. You run away to hide!")    
        return
    # Create Ian multitool wrench. Using .name instead of checking simple objects from now on to temporary fix a bug with reset_game() function  
    if obj1.name in [wrench.name, ian_chip.name] and obj2.name in [wrench.name, ian_chip.name]:
        # Now that we checked the objects that can be inserted in any order by the user, we can "fix" the order for simplicity
        item1 = ian_chip.name
        item2 = wrench.name
        game_data['inventory'].take(item1)
        game_data['inventory'].take(item2)
        game_data['inventory'].add(ian_tool)
        game_data['objects_count']['inventory'][ian_tool.name] = 1
        update_gui(f"You combine {item1} with {item2} and you get a super shiny {ian_tool.name}! <br> {ian_tool.description}")
    # Add coke to Ian multi-tool to create the super tool to fix Hypersphere
    elif obj1.name in [ian_tool.name, coke.name] and obj2.name in [ian_tool.name, coke.name]:
        item1 = ian_tool.name
        item2 = coke.name
        game_data['inventory'].take(item1)
        game_data['inventory'].take(item2)
        game_data['inventory'].add(ian_tool_coke)
        game_data['objects_count']["inventory"][ian_tool_coke.name] = 1
        update_gui(f"You combine {item1} with {item2} and you get a powerful {ian_tool_coke.name}! <br> {ian_tool_coke.description}") 
    # Creates a simple battle system where player and opponent has both chances to hit or miss for every shoot. Handles both Venster's and Player's death
    elif obj1.name in [silaha.name, venster.name] and obj2.name in [silaha.name, venster.name]:
        lost_vhealth = 0
        lost_phealth = 0
        random_pfight = random.choice(["hit", "miss"])
        if random_pfight == "hit":
            lost_vhealth = random.randint(25,50)
            game_data['venster_energy'] -= lost_vhealth  
        if game_data['venster_energy'] <= 0:
            room_items().take(venster.name)
            game_data['unlisted'].remove(venster_dead.name)
            current_user.set_game_data(game_data)
            update_gui(f"You shoot the venster with your silaha. You {random_pfight}, and he looses {lost_vhealth} health points. He's finally dead!")
            return
        random_vfight = random.choice(["hit", "misses"])
        if random_vfight == "hit":
            lost_phealth = random.randint(10,15)
            game_data['player_energy'] -= lost_phealth
        if game_data['player_energy'] <= 0:
            reset_game(f"You shoot the venster with your silaha. You {random_pfight}, and he looses {lost_vhealth} health points. He now has {game_data['venster_energy']} health points.<br> Unfortunately he shoots back with his potato phaser, and he {random_vfight} you. You loose {lost_phealth} and you die horribly while the Vensters laughs at you!" + game_response_die_addon) 
            return
        update_gui(f"You shoot the venster with your silaha. You {random_pfight}, and he looses {lost_vhealth} health points. He now has {game_data['venster_energy']} health points.<br> Unfortunately he shoots back with his potato phaser, and he {random_vfight} you. You loose {lost_phealth} and you now have {game_data['player_energy']} health points.")      
    # Unlock crew doors with multitool
    elif obj1.name in [ian_tool.name] and obj2.name in [henry_room_keypad.name, aria_room_keypad.name, buzz_room_keypad.name, ian_room_keypad.name]:
        room_name = obj2.name.split("'")[0].lower() + " room"
        room = find_room(room_name)
        try:
            game_data['locked'].remove(room.name)
            game_data['gui']['game_response'] = f"You have unlocked {room.name} door! You can enter now."
        except ValueError:
            game_data['gui']['game_response'] = f"{room.name} door is already unlocked! You can enter now."
    # Unlock crew doors with coke multitool
    elif obj1.name in [ian_tool_coke.name] and obj2.name in [henry_room_keypad.name, aria_room_keypad.name, buzz_room_keypad.name, ian_room_keypad.name]:
        room_name = obj2.name.split("'")[0].lower() + " room"
        room = find_room(room_name)
        try:
            game_data['locked'].remove(room.name)
            game_data['gui']['game_response'] = f"You have unlocked {room.name} door! You can enter now."
        except ValueError:
            game_data['gui']['game_response'] = f"{room.name} door is already unlocked! You can enter now."      
    # Using normal wrench or multi-tool with Hypersphere console result in failure
    elif obj1.name in [wrench.name, hypersphere_console.name] and obj2.name in [wrench.name, hypersphere_console.name]:  
        game_data['gui']["game_response"] = "A normal positronic wrench to fix an Hypersphere? Are you serious?"
    elif obj1.name in [ian_tool.name, hypersphere_console.name] and obj2.name in [ian_tool.name, hypersphere_console.name]:  
        game_data['gui']["game_response"] = f"{ian_tool.name} can fix everything...except an Hypersphere! But wait...if you examine the multi-tool closely, there's an empty space...maybe you should try adding something..."
    # Repairs the Hypersphere with Ian multi-tool enhanced by coke  
    elif obj1.name in [ian_tool_coke.name, hypersphere_console.name] and obj2.name in [ian_tool_coke.name, hypersphere_console.name]:
        game_data['hypersphere_status'] = True
        game_data['gui']["game_response"] = "You hear a loud noise, and then the Hypersphere starts singurgling again. It's like a symphony made in heaven mixed with a bad toilet drain. The Starship Hope can fly again!"
    # Inserts the Venster digital map to the astrometry console
    elif obj1.name in [astrometry_console.name, venster_digital_map.name] and obj2.name in [astrometry_console.name, venster_digital_map.name]:
        game_data['venster_map'] = True
        if game_data['briefing_diary'] == False:
            game_data['gui']["game_response"] = "You insert the Venster chip with the digital map in the astrometry console. After a while, the map of a far solar system appears, with a planet marked as Eos. Why is this system so important that a Venster carried a map on himself? Maybe a trip to the briefing room might clarify..."
        else:
            game_data['gui']["game_response"] = "You insert the Venster chip with the digital map in the astrometry console. After a while, the map of a far solar system appears, marked as Eos. Is this the system where the Venster brought the crew of the Hope? You should investigate!"
    elif obj1.name == buzz_phaser.name or obj2.name == buzz_phaser.name:
        game_data['inventory'].take(buzz_phaser.name)
        update_gui("You try to fire the phaser, but as soon as you press the trigger, it turns into a slimy liquid that stinks. It's a classic Buzz's prank. Did you really think an Atarian would need a phaser?")          




  
    else:
        game_data['gui']['game_response'] = f"You can't use {item1} on {item2}"
        return
    current_user.set_game_data(game_data)

def check_items(item1, item2 = None):
    '''Check if an object is in the inventory OR if it's an immovable room object on which an inventory object can be used'''
    game_data = current_user.get_game_data()
    obj1 = None
    obj2 = None
    if game_data['inventory'].find(item1):
        obj1 = game_data['inventory'].find(item1)
    elif room_items().find(item1) and room_items().find(item1).immovable:
        obj1 = room_items().find(item1)
    # Item 2 can either be a real item, or None if this function is used with a single object  
    if item2 == None:
        return obj1
    if game_data['inventory'].find(item2):
        obj2 = game_data['inventory'].find(item2)
    elif room_items().find(item2) and room_items().find(item2).immovable:
        obj2 = room_items().find(item2)

    return obj1, obj2

@when("set course to WHERE")
def set_course(where):
    '''Fly the ship!'''
    game_data = current_user.get_game_data()
    if game_data['context'] != "bridge": 
        game_data['gui']["game_response"] = "You need to be on the Bridge to fly the Hope!"
        return
    if game_data['hypersphere_status'] == False:
        game_data['gui']["game_response"] = "The Hypersphere is offline. You need to repair it first."
        return  
    if game_data['nav console'] == False:
        game_data['gui']["game_response"] = "You need to activate the navigation console before you can fly the ship!"
        return
    if where.lower() in planet_list:
        game_data['gui']["game_response"] = f"The Hypersphere emits a loud and happy singurgle, and the Hope jumps to {where.capitalize()}."
        game_data['planet'] = where.lower()
    else:
        game_data['gui']["game_response"] = f"You don't have the coordinates of {where.capitalize()} in the navigational computer."
        return
    current_user.set_game_data(game_data) 

@when("search WHAT")
def search(what):
    '''Search in particular items'''
    game_data = current_user.get_game_data()
    obj = check_items(what)
    if not obj:
        game_data['gui']["game_response"] = f"{what} not found"
        return
    # Search Aria's sexy images
    if obj.name == photos_pile.name:
        try:
            game_data['unlisted'].remove(ipod.name)
            update_gui("You searched the photos pile and you found an old iPod!")
        except ValueError:
            update_gui("You have already searched the photos pile")
    # Search pile of chips
    elif obj.name == chips_pile.name:
        game_data['gui']["game_response"] = f"You searched the pile of chips and you found nothing. It's just a pile of scrapped chips put here as a decoy for you. Ha! You have to search somewhere less obvious. Maybe some food will help your brain?"

    # Search dead Venster
    elif obj.name == venster_dead.name:
        try:
            game_data['unlisted'].remove(venster_digital_map.name)
            update_gui(f"You searched the dead venster and you found a suspicious Venster digital map chip!")
        except ValueError:
            update_gui("You have already searched the dead venster")

    # Search mess tables to find ian chip
    elif obj.name == mess_tables.name:
        try:
            game_data['unlisted'].remove(ian_chip.name)
            update_gui(f"You searched the mess tables and you found a custom chip made by Ian Volk himself!")
        except ValueError:
            update_gui("You have already searched the mess tables")  
    # Search Henry pile of uniforms
    elif obj.name == pile_uniforms.name:
        try:
            game_data['unlisted'].remove(officer_badge.name)
            update_gui(f"You searched the pile of uniforms and you found an officer badge!") 
        except ValueError:
            update_gui("You have already searched the pile of uniforms")  
    # Search weapons console
    elif obj.name == weapon_console.name:
        try:
            game_data['unlisted'].remove(security_badge.name)
            update_gui(f"You searched the Weapons and Security console and you found a security badge!")   
        except ValueError:
            update_gui("You have already searched the Weapons and Security console")

    else:
        game_data['gui']["game_response"] = f"You can't search {obj.name}."
        return
        
    current_user.set_game_data(game_data) 
  
@when("land to WHERE")
def land(where):
    '''Land the shuttle'''
    game_data = current_user.get_game_data()
    if game_data['context'] != "shuttle": 
        game_data['gui']["game_response"] = "You need to be on the Shuttle to land!"
        return
    if where.lower() != game_data['planet'].lower():
        game_data['gui']["game_response"] = f"I'm sorry, we are not orbiting the planet {where.capitalize()}"
        return
    
    update_gui(f"You take a short flight and land on the planet {where.capitalize()}. Will you find the Starship Hope Crew and save them? Well, you will never know, because this was just a short demo and it ends here. Bye bye!<br> No really. You completed the demo. Yay! You can reset it now and start over.")

@when("help COMMAND")
def help(command):
    '''Gives info about commands'''
    game_data = current_user.get_game_data()
    if command == "look at":
        game_data['gui']["game_response"] = "Looks at an object and describes it.<br> Usage: look at <i>object name</i>"
    elif command == "look around":
        game_data['gui']["game_response"] = "Looks around in the room and returns the room description.<br> Usage: look around"
    elif command == "list locations":
        game_data['gui']["game_response"] = "Lists all the locations you can move to from the current room. You can also look at the map for the same result.<br> Usage: list locations"
    elif command == "go to":
        game_data['gui']["game_response"] = "Moves to a new location, if available. You can also click on the map for the same result.<br> Usage: go to <i>room name</i>"      
    elif command == "inventory":
        game_data['gui']["game_response"] = "Lists all the items in your inventory, and updates your inventory tab in case it's not.<br> Usage: inventory"
    elif command == "take":
        game_data['gui']["game_response"] = "Takes an item from a room, and places into your inventory. You can use the item full name, or the short name (the one between brackets). You can also specify the number of items. <br> Usage: take <i>number item</i>" 
    elif command == "drop":
        game_data['gui']["game_response"] = "Drops an item from your inventory into the current room. You can use the item full name, or the short name (the one between brackets). You can also specify the number of items.<br> Usage: drop <i>number item</i>"
    elif command == "open":
        game_data['gui']["game_response"] = "Opens an item, if possible (for example, a cabinet) and reveals its content.<br> Usage: open <i>item</i>"   
    elif command == "use":
        game_data['gui']["game_response"] = "Uses an item by itself OR uses an item on another item OR combines an item with another one.<br> Usage:<br>use <i>item</i> <br>use <i>item on item</i><br>use <i>item with item</i>"
    elif command == "eat":
        game_data['gui']["game_response"] = "Eats food and gives you some energy.<br> Usage: eat <i>food</i>"
    elif command == "drink":
        game_data['gui']["game_response"] = "Drinks a beverage and gives you some energy.<br> Usage: drink <i>beverage</i>" 
    elif command == "save game":
        game_data['gui']["game_response"] = "Saves game into the save game slot (only one at the moment). Use it before trying something that could make you die!<br> Usage: save game"
    elif command == "load game":
        game_data['gui']["game_response"] = "Loads the last saved game.<br> Usage: load game"
    elif command == "reset game":
        game_data['gui']["game_response"] = "Resets the game to the initial state. Let's restart the adventure!<br> Usage: reset game"
    elif command == "enter airlock":
        game_data['gui']["game_response"] = "Just a fancy command to enter the airlock at the beginning of the game. Same of \"go to airlock\".<br> Usage: enter airlock"
    elif command == "set course to":
        game_data['gui']["game_response"] = "Flies the ship to a destination. It can be used only on the bridge, after activating the helm.<br> Usage: set course to <i>destination</i>"
    elif command == "replicate":
        game_data['gui']["game_response"] = "Uses the food replicator in the mess all. It can only replicate food or drinks, so if you ask for a nuclear bomb, it will give you a very cute nuclear bomb shaped cake.<br> Usage: replicate <i>food/drink</i>" 
    elif command == "land to":
        game_data['gui']["game_response"] = "Lands the shuttle to a planet surface. Therefore can only be used only while inside the shuttle.<br> Usage: land to <i>planet</i>"
    elif command == "search":
        game_data['gui']["game_response"] = "Searches inside or on an item, if possible, to reveal hidden items.<br> Usage: search <i>item</i>"  

    else:
        game_data['gui']["game_response"] = "Command not available"
    
      

@when("save game")
def save_game():
    '''Saves the game'''
    current_user.save_game_data()
    update_gui("Game saved")

@when("load game")
def load_game():
    '''Loads the latest savegame'''
    current_user.load_game_data()
    update_gui("Game loaded")


      
# INITIAL GAME STATE


state = {
  'current_room' : space,
  'player_energy' : 100,
  'venster_energy': 100,
  'hypersphere_status' : False,
  'planet' : False,
  'briefing_diary' : False,
  'venster_map' : False,
  'start' : True,
  'context' : None,
  'nav console' : False,
  'inventory' : inventory,
  'shuttle.loc' : shuttle.loc,
  'user_food' : user_food,
  'space items' : space.items,
  'airlock items' : airlock.items,
  'mess items' : mess.items,
  'lab items' : lab.items,
  'engineering items' : engineering.items,
  'crew quarters items' : crew_quarters.items,
  'ian room items' : ian_room.items,
  'henry room items' : henry_room.items,
  'buzz room items' : buzz_room.items,
  'aria room items' : aria_room.items,
  'briefing room items' : briefing_room.items,
  'hangar items' : hangar.items,
  'bridge items' : bridge.items,
  'lift items' : lift.items,
  'shuttle items' : shuttle.items,
  'objects_count' : objects_count,
  'gui' : {},
  'locked' : [henry_room.name, aria_room.name, ian_room.name, buzz_room.name],
  'unlisted' : [wrench.name, ian_chip.name, officer_badge.name, ipod.name, venster_dead.name, venster_digital_map.name, buzz_phaser.name, shuttle_key.name, security_badge.name]
}








    


    