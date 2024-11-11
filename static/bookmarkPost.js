// thanks to https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch for help with fetch
async function bookmarkPost(num) {
  // send the id of the post that we want to bookmark
  // note: the username is stored on the backend so we don't need to send it

  // generate the link to send to
  let post = document.getElementById("p"+num);
  let postAttributes = post.children;
  let postID = postAttributes[2];
  const url = "/bookmarkPost" + postID.textContent;

  // actually send the id
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    console.log(response);

    // now update the bookmark button to let the user unbookmark the post
    let bookmarkBttns = document.getElementsByClassName("bookmarkBttn");
    bookmarkBttns[num].setAttribute("onclick", "unbookmarkPost("+num+")");
    bookmarkBttns[num].textContent = " Remove Bookmark ";

  } catch (error) {
    console.error(error.message);
  }
}

async function unbookmarkPost(num) {
  // send the id of the post that we want to bookmark
  // note: the username is stored on the backend so we don't need to send it

  // generate the link to send to
  let post = document.getElementById("p"+num);
  let postAttributes = post.children;
  let postID = postAttributes[2];
  const url = "/unbookmarkPost" + postID.textContent;

  // actually send the id
  console.log(url);
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    console.log(response);

    // now update the bookmark button to let the user unbookmark the post
    let bookmarkBttns = document.getElementsByClassName("bookmarkBttn");
    bookmarkBttns[num].setAttribute("onclick", "bookmarkPost("+num+")");
    bookmarkBttns[num].textContent = " Bookmark ";

  } catch (error) {
    console.error(error.message);
  }
}