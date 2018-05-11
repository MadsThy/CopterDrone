//Clear all inputs when command button is pressed
function commandClear(){
    document.getElementById('commandValue').value="";
    document.getElementById('command').value="";
};

function clearAll(){
    document.getElementById('commandValue').value="";
    document.getElementById('command').value="";
    document.getElementById('UserCommands').value="";
    document.getElementById('DroneStatus').value="";
}

//Time and Date
var currentdate = new Date(); 
var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " - "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();

//Send an alert that the command has been sent
function commandAlert(){
    alert("Command: " + document.getElementById('command').value + " with value " + document.getElementById('commandValue').value + " has been sent to the Drone at: " + datetime);
}