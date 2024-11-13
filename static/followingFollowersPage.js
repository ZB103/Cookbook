// load followers and following upon opening the page
function getFollow() {
    let follower = document.getElementById("Followers");
    follower.textContent = fetchFollowers();

    let following = document.getElementById("Following");
    following.textContent = fetchFollowing();
}

// thanks to https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch for help with fetch
// recieve followers from backend
async function fetchFollowers() {
    const followerUrl = ""
    try {
        const response = await fetch(followerUrl);
        if (!response.ok) {
            throw new Error('Response status: ${response.status}');
        }

        const followerJson = await response.json();
        console.log(followerJson);
    } catch (error) {
        console.error(error.message);
    }
}

// recieve following from backend
async function fetchFollowing() {
    const followingUrl = ""
    try {
        const response = await fetch(followingUrl);
        if (!response.ok) {
            throw new Error('Response status: ${response.status}');
        }

        const followingJson = await response.json();
        console.log(followingJson);
    } catch (error) {
        console.error(error.message);
    }
}

// thanks to https://www.w3schools.com/howto/howto_js_tabs.asp for help with tabs
// make tabs show correct data
function openFollow(evt, follows) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(follows).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();