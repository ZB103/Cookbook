// JS page written by Connor Ettinger

// Function to check and make sure that a file is not too large
function checkFileSize(){
  // get the thing that was uploaded
  let upload = document.getElementById("pic");
  const MAX_FILE_SIZE = 5242880; // according to stack overflow, 1MB = 1,048,576, so 5MB = 5,242,880
  // check the size of the file
  if(upload.files[0].size > MAX_FILE_SIZE){
    alert("Your file is too large. The max file size is 5MB.");
    upload.value = "";
  }
  else{console.log(upload.files[0].size);}
}

// Function to check and make sure that a user isn't exceeding the character limit
function limitCharLen(id,maxLen){
  let element = document.getElementById(id);
  if(element.value.length >= maxLen){
    alert("The max character length for this field is " + maxLen +".");
  }
}

// Function to dynamically add a new ingredient field
function addIngredient(){
  // first get text from the input
  let ingredientInput = document.getElementById("ingredientInput").value;
  console.log(ingredientInput);
  // second make sure the user doesn't try to submit an empty tag
  if(ingredientInput.trim().length < 1 || ingredientInput === null){
    alert("Please enter text in the ingredient");
    return; // exit the funtion
  }
  // third make sure someone doesn't implement multiple of the same ingredient
  // NOTE: I don't think there's really any way to prevent someone from putting in multiple of the same ingredient but just changing the measurement amount. I would love to be proven wrong though.
  const MAX_INGREDIENTS = 20;
  let prevIngredients = document.getElementById("ingredientList").children;
  for(let i = 0; i < prevIngredients.length; i++){
    if(prevIngredients[i].textContent === ingredientInput){
      alert("Please don't enter duplicate ingredients");
      return;
    } else if(i >= (MAX_INGREDIENTS - 1)){
      alert("Ingredient cap reached. A recipe can't have more than 20 ingredients.");
      return;
    }
  }
  // fourth create a new list element
  let newIngredient = document.createElement("li");
  newIngredient.textContent = ingredientInput;
  // fifth add that list element to the ul
  document.getElementById("ingredientList").appendChild(newIngredient);
  // finally, add that to the hidden input that will actually be turned in
  hiddenList = document.getElementById("hiddenIngredientList");
  let hiddenText;
  if(hiddenList.value == ""){
    hiddenText = ingredientInput;
  } else{
    hiddenText = hiddenList.value + ", " + ingredientInput;
  }
  hiddenList.setAttribute("value", hiddenText);
  console.log(hiddenList.value);
}

// function to dynamically add a tag to the page
function addTag(){
  // first make sure we haven't hit the tag limit
  const MAX_TAGS = 15
  let tagNum = document.getElementById("numOfTags");
  if(Number(tagNum.value) >= MAX_TAGS){
    alert("Tag cap reached. Your post can't have more than 15 tags.");
    return;
  }
  // second get text from the input
  let tagInput = document.getElementById("tagInput");
  console.log(tagInput.value);
  // third check and make sure the tag text is acceptable
  tagInput.value = tagInput.value.replaceAll(" ", ""); // remove spaces
  // make sure the user doesn't try to submit an empty tag
  if(tagInput.value.length < 1){
    alert("Please enter text in the tag");
    return;
  }
  // make sure all tags start with "#"
  if(!tagInput.value.startsWith("#")){
    tagInput.value = "#".concat(tagInput.value);
  }

  // now that the tag has been verified, let's start the process of adding the tag to the field
  let tagField = document.getElementById("tagField"); // tagField is where the tags are displayed to the user. Doesn't exist until the user adds a tag
  
  // check if the tagField exists. if it doesn't, it will return null, which is evaluated as false in js
  // so we'll create it
  if(tagField){
    // if it exists, make sure the tag isn't already there
    if(tagField.value.includes(tagInput.value)){
      alert("Please don't enter duplicate tags");
      return;
    }
    // then add the tag to the input field
    let tagText = tagField.value + ", " + tagInput.value;
    tagField.setAttribute("value", tagText);
  } else {
    // if it doesn't exist...
    // create a new input tag
    tagField = document.createElement("input");
    // set its attributes
    tagField.setAttribute("type","text");
    tagField.setAttribute("id","tagField");
    tagField.setAttribute("name","tagField");
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
  // finally, update the number of tags
  tagNum.value = Number(tagNum.value) + 1;
}