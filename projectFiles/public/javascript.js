function clear(){
    document.getElementById('commandValue').value="";
    document.getElementById('command').value="";
};

//Time and Date
var currentdate = new Date(); 
var datetime = currentdate.getDate() + "/"
                + (currentdate.getMonth()+1)  + "/" 
                + currentdate.getFullYear() + " - "  
                + currentdate.getHours() + ":"  
                + currentdate.getMinutes() + ":" 
                + currentdate.getSeconds();

function commandAlert(){
    alert("Command: " + document.getElementById('command').value + " with value " + document.getElementById('commandValue').value + " has been sent to the Drone at: " + datetime);
}