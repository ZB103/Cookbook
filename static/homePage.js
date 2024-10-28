let currPageNum = 0;

async function pageLeft(){
  if(currPageNum == 0){
    return;
  } else {
    currPageNum--;
    getPosts();
  }
}

async function pageRight(){
  currPageNum++;
  getPosts();
}

// thanks to https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch for help with fetch
async function getPosts() {
  const url = "/loadPostsPg" + currPageNum;
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const postJson = await response.json();
    console.log(postJson);

    for(let i = 0; i < 3; i++){
      let id = "p" + i;
      let post = document.getElementById(id);
      let postChildren = post.children;
      postChildren[0].textContent = postJson[i]["title"];
      postChildren[1].textContent = postJson[i]["description"];
    }

  } catch (error) {
    console.error(error.message);
  }
}
