// JS page written by Connor Ettinger
// Function to dynamically add a new ingredient field
function addIngredient(){
  // first get text from the input
  let ingredientInput = document.getElementById("ingredientInput").value;
  console.log(ingredientInput);
  // second create a new list element
  let newIngredient = document.createElement("li");
  newIngredient.textContent = ingredientInput;
  // third add that list element to the ul
  document.getElementById("ingredientList").appendChild(newIngredient);
}

// function to dynamically add a tag to the page
function addTag(){
  // first get text from the input
  let tagInput = document.getElementById("tagInput");
  console.log(tagInput.value);
  // second check if it starts with a #, and if not add it
  if(!tagInput.value.startsWith("#")){
    tagInput.value = "#".concat(tagInput.value);
  }
  // next add to current tags
  let tagField = document.getElementById("tagField"); // tagField is where the tags are displayed to the user. Doesn't exist until the user adds a tag
  
  // check if the tagField exists. if it doesn't, it will return null, which is evaluated as false in js
  if(tagField){
    // if it exists, add the new tag the user put in to the tag field
    let tagText = tagField.value + ", " + tagInput.value;
    tagField.setAttribute("value", tagText);
  } else {
    // if it doesn't exist...
    // create a new input tag
    tagField = document.createElement("input");
    // set its attributes
    tagField.setAttribute("type","text");
    tagField.setAttribute("id","tagField");
    /* readonly is weird. you can't just set it, because setAttribute expects the value to be set to something. (e.g., id=tagField)
    So instead, you have to create a readonly attribute, and add it to the tagFireld.
    Very odd...*/
    const readOnlyAttr = document.createAttribute("readonly");
    tagField.setAttributeNode(readOnlyAttr);
    // add it to the webpage below the tag submit button (add a line break first)
    // tagHolder is the fieldset element that all of the tag stuff is in
    let tagHolder = document.getElementById("tagHolder");
    let br = document.createElement("br");
    tagHolder.appendChild(br);
    tagHolder.appendChild(tagField);
    // add the new tag the user put in to the tag field
    tagField.setAttribute("value", tagInput.value);
  }
}