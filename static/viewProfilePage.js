function runStartFunctions() {
    getUsername();
    getPosts();
}

function getUsername() {
    let un = document.getElementById("username");
    un.textContent = "[Username]";
}

function getPosts() {
    let p1 = document.getElementById("post1");
    p1.textContent = "Fresh Fish";

    let p2 = document.getElementById("post2");
    p2.textContent = "Fresh Ifsh";

    let p3 = document.getElementById("post3");
    p3.textContent = "Fresh Shift";
}

function deletePost() {
    alert("deletePost called");
}