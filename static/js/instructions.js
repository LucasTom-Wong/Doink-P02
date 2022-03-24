// Doink!
// SoftDev pd1
// P02

// let loginClick = function(){
//   display("Error");
// }

let instructions = "No instructions yet, please wait.";

let displayInstruction = function(){
  console.log("Button pressed");
  display(instructions)
}

let display = function(n){
  let text = document.getElementById("instruction");
  text.innerHTML = n;
}

let login = document.getElementById("instruction");
login.addEventListener('click', displayInstruction);
