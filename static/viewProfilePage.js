function runStartFunctions() {
    getUsername();
    getPosts();
}

async function getUsername() {
    const url = "/getUsername";
    console.log(url);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const postResponseText = await response.text();
      console.log(postResponseText);
      let un = document.getElementById("username");
      un.textContent = postResponseText;
    } catch (error) {
        console.log(error.message);
      }
}

async function getPosts() {
    const url = "/loadUserPosts";
    console.log(url);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const postJson = await response.json();
      console.log(postJson);
  
      for(let i = 0; i < 6; i++){
        let id = "p" + i;
        let post = document.getElementById(id);
        let postChildren = post.children;
        
        if (postJson[i]["description"] == "") {
          postChildren[0].textContent = postJson[i]["username"]
          postChildren[1].textContent = postJson[i]["title"];
          postChildren[2].textContent = "";
          let moreChildren = document.getElementById("more"+i).children;
          moreChildren[0].textContent = "Ingredients: ";
          moreChildren[1].textContent = postJson[i]["ingredients"];
          moreChildren[3].textContent = "Instructions: ";
          moreChildren[4].textContent = postJson[i]["instructions"];
          moreChildren[6].textContent = "Tags: ";
          moreChildren[7].textContent = postJson[i]["tags"];
          postChildren[4].textContent = postJson[i]["id"];
        }
        else {
          postChildren[0].textContent = postJson[i]["username"]
          postChildren[1].textContent = postJson[i]["title"];
          postChildren[2].textContent = postJson[i]["description"];
          let moreChildren = document.getElementById("more"+i).children;
          moreChildren[0].textContent = "Ingredients: ";
          moreChildren[1].textContent = postJson[i]["ingredients"];
          moreChildren[3].textContent = "Instructions: ";
          moreChildren[4].textContent = postJson[i]["instructions"];
          moreChildren[6].textContent = "Tags: ";
          moreChildren[7].textContent = postJson[i]["tags"];
          postChildren[4].textContent = postJson[i]["id"];
        }
      }
  
    } catch (error) {
      console.log(error.message);
    }
  }
  
  function showExcessText(num) {
    var dots = document.getElementById("dots"+num);
    var moreText = document.getElementById("more"+num);
    var btnText = document.getElementById("showMore"+num);
  
    if (dots.style.display === "none") {
      dots.style.display = "inline";
      btnText.innerHTML = "Show More"
      moreText.style.display = "none";
    }
  
    else {
      dots.style.display = "none";
      btnText.innerHTML = "Show less"; 
      moreText.style.display = "inline";
    }
  }

function deletePost() {
    alert("deletePost called");
}