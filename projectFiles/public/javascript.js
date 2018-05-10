function clear(){
    document.getElementById('commandValue').clear;
    document.getElementById('command').clear;
};

function commandAlert(){
    alert("Command: " + document.getElementById('command').value + " with value " + document.getElementById('commandValue').value + " has been sent to the Drone. Time: ");
}