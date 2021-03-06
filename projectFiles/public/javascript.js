//Clear all inputs when command button is pressed
function commandClear(){
    document.getElementById('command').value="";
}

//Clear all input fields and textareas
function clearAll(){
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
    alert("Command: " + document.getElementById('command').value + " sent to drone at: " + datetime);
}