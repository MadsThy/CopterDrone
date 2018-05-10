function clear(){
    document.getElementById('commandValue').clear;
    document.getElementById('command').clear;
};

function commandAlert(){
    alert("Command: " + document.getElementById('command') + " with value " + document.getElementById('commandValue') + " has been sent to the Drone. Time: ");
}