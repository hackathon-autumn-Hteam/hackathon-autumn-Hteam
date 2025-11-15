
var modal = document.getElementById("logoutModal");
var openBtn = document.getElementById("openModal");
var closeBtn = document.getElementById("closeModalButton");
var closeSpan = document.getElementsByClassName("close")[0];

openBtn.onclick = function() {
    modal.style.display = "block";
}

closeSpan.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
