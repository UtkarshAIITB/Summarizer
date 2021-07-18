document.getElementById("button_copy").onclick = function(){
    document.getElementById("output").select();
    document.execCommand('copy');
}