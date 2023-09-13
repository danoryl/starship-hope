function sendInput(userInput = document.getElementById('user_input').value) {
            fetch('/input', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `user_input=${encodeURIComponent(userInput)}`
            })
            .then(response => response.json())
            .then(data => {
                const guiData = data;
                displayGameData(guiData);
                
            })
            .catch(error => {
                console.error('Error:', error);
            });
             // Trigger the "Escape" key event to close the dropdown
 
            
        
        
        }

          
function displayGameData(data) {
    // Updates game data in the interface
    
    const outputDiv = document.getElementById('output');
    const roomDiv = document.getElementById('room');
    const roomItemsDiv = document.getElementById('room_items');
    const inventoryDiv = document.getElementById('inventory');
        
    outputDiv.innerHTML = data.game_response;
    roomDiv.innerHTML = "<h2>Room Description</h2>\n" + data.room_desc;
    roomItemsDiv.innerHTML = "<h2>Room Items</h2>\n" + data.room_items;
    inventoryDiv.innerHTML = "<h2>Inventory</h2>\n" + data.inventory;
    
    

      
    // Update the energy bar
      const energyBar = document.getElementById("energy-progress");
      const energyData = data.energy;
      
      // Update the energy bar width and color based on data
      energyBar.style.width = energyData + "%"; // Set the width based on data
      if (energyData <= 30) {
        energyBar.style.backgroundColor = "red";
        
      } else if (energyData > 30 && energyData < 60) {
        energyBar.style.backgroundColor = "orange";
        
      } else {
        energyBar.style.backgroundColor = "green";
       
    }

    // Update aria-valuenow attribute
    energyBar.setAttribute("aria-valuenow", energyData);
    
    // Update energyValue text
    energyBar.textContent = energyData;

    // Update command list
    const allCommands = document.getElementById("all_commands");
    allCommands.innerHTML = "Available commands: " + data.suggestions.join(", ") + "<br> Use help <i>command</i> to know more about a specific command.";

    // MAP
    updateMap(data.room_loc, data.room_name);

         
    // SUGGESTIONS
    const suggestionInput = document.getElementById("user_input");
  

  const suggestions = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: data.suggestions
  });

  $(suggestionInput).typeahead({
    hint: true,
    highlight: true,
    minLength: 1
  },
  {
    name: 'suggestions',
    source: suggestions
  });
  
 suggestionInput.value = '';
 suggestionInput.focus(); 

 
 }

function handleKeyPress(event) {
  // Check if the pressed key is the "Enter" key (key code 13)
  if (event.keyCode === 13) {
    
    // Call the sendInput() function to submit the form
    
    sendInput();
    
  }
}

// MAPS


const stage = new Konva.Stage({
  container: 'map-container',
  width: 500, 
  height: 300 
});

const layer = new Konva.Layer();
stage.add(layer);

const mapsData = {
  "Space": [
    { x: 150, y: 0, width: 100, height: 100, color: 'lightblue', label: 'Airlock' },
    { x: 20, y: 80, width: 40, height: 40, color: 'lightblue', label: 'You' }
  ],
  "Deck 1": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Lab' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 90, height: 120, color: 'lightblue', label: 'Briefing room' },
    { x: 220, y: 0, width: 130, height: 120, color: 'lightblue', label: 'Bridge' },
  ],
  "Deck 2": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Airlock' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 150, height: 120, color: 'lightblue', label: 'Crew quarters' },
    { x: 280, y: 0, width: 70, height: 120, color: 'lightblue', label: 'Mess' },
  ],
  "Deck 3": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Engineering' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 220, height: 120, color: 'lightblue', label: 'Hangar' },
  ],
  "Crew quarters": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Airlock' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 150, height: 120, color: 'lightblue', label: 'Crew quarters' },
    { x: 280, y: 0, width: 70, height: 120, color: 'lightblue', label: 'Mess' },
    { x: 110, y: 120, width: 45, height: 120, color: 'lightblue', label: 'Aria room' },
    { x: 155, y: 120, width: 45, height: 120, color: 'lightblue', label: 'Ian room' },
    { x: 200, y: 120, width: 45, height: 120, color: 'lightblue', label: 'Buzz room' },
    { x: 245, y: 120, width: 55, height: 120, color: 'lightblue', label: 'Henry room' },
  ],
  "Hangar": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Engineering' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 220, height: 120, color: 'lightblue', label: 'Hangar' },
    { x: 200, y: 120, width: 80, height: 120, color: 'lightblue', label: 'Shuttle' },
  ],
  "Officer room": [
    { x: 0, y: 0, width: 350, height: 80, color: 'lightblue', label: 'Crew quarters' },
    { x: 100, y: 80, width: 150, height: 160, color: 'lightblue', label: 'Room' },
  ],
  "Shuttle": [
    { x: 0, y: 0, width: 350, height: 80, color: 'lightblue', label: 'Hangar' },
    { x: 100, y: 80, width: 150, height: 160, color: 'lightblue', label: 'Shuttle' },
  ],
  "Lift deck 1": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Lab' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 90, height: 120, color: 'lightblue', label: 'Briefing room' },
    { x: 220, y: 0, width: 130, height: 120, color: 'lightblue', label: 'Bridge' },
    { x: 65, y: 130, width: 80, height: 40, color: 'lightblue', label: 'Deck 2' },
    { x: 65, y: 180, width: 80, height: 40, color: 'lightblue', label: 'Deck 3' },
  ],
  "Lift deck 2": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Airlock' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 150, height: 120, color: 'lightblue', label: 'Crew quarters' },
    { x: 280, y: 0, width: 70, height: 120, color: 'lightblue', label: 'Mess' },
    { x: 65, y: 130, width: 80, height: 40, color: 'lightblue', label: 'Deck 1' },
    { x: 65, y: 180, width: 80, height: 40, color: 'lightblue', label: 'Deck 3' },
  ],
  "Lift deck 3": [
    { x: 0, y: 0, width: 80, height: 120, color: 'lightblue', label: 'Engineering' },
    { x: 80, y: 0, width: 50, height: 120, color: 'lightblue', label: 'Lift' },
    { x: 130, y: 0, width: 220, height: 120, color: 'lightblue', label: 'Hangar' },
    { x: 65, y: 130, width: 80, height: 40, color: 'lightblue', label: 'Deck 1' },
    { x: 65, y: 180, width: 80, height: 40, color: 'lightblue', label: 'Deck 2' },
  ],
};

// Function to create or update the map
function updateMap(mapName, roomName) {
  layer.destroyChildren(); // Clear the layer
  const mapTitleElement = document.getElementById('map-title');
  if (mapName == "nomap") { // Check if users has the map
    mapTitleElement.innerHTML = '<p>You have no map.</p>'
    return
  };
  
  mapTitleElement.innerHTML = `<h4>${mapName}</h4> Click on a room to teleport directly to that location (if available)`;
  
  
  mapsData[mapName].forEach(room => {
    // Create the rectangle
    
    if (room.label === roomName) {
      room.color = "#FF0000"; // Temporary color for the current room
    } else {
      room.color = 'lightblue'; // Revert to original color for other rooms
    };
    const rect = new Konva.Rect({
      x: room.x,
      y: room.y,
      width: room.width,
      height: room.height,
      fill: room.color,
      stroke: 'black',
      strokeWidth: 2
    });

    // Create the label
    const label = new Konva.Text({
      x: room.x + room.width / 2,
      y: room.y + room.height / 2,
      text: room.label,
      fontSize: 14,
      fontFamily: 'Arial',
      fill: 'black',
      align: 'center',
      width: room.width
    });
    label.offsetX(label.width() / 2);
    label.offsetY(label.height() / 2);

    rect.on('click tap', () => {
      
      sendInput('go to ' + room.label);
    });

    label.on('click tap', () => {
      
      sendInput('go to ' + room.label);
    });

    layer.add(rect);
    layer.add(label);
  });

  stage.batchDraw(); // Redraw the stage
}



  
