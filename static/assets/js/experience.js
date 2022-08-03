function addExperience(){
    let experiences = document.getElementById("experience-container");
    let lenExp = experiences.childElementCount;
    
    let latestExperience = experiences.children[lenExp - 1];
    let newExperience = latestExperience.cloneNode(true);
    newExperience.className = `experience ${lenExp + 1}`;

    for(let i=0; i<newExperience.childElementCount; i++){
        let theInput = newExperience.children[i].children[0].children[0];
        console.log(theInput);
        let theName = theInput.name.split(' ')[0];
        let theNewName = `${theName} ${lenExp + 1}`;
        theInput.name = theNewName;
    }

    experiences.appendChild(newExperience);
    lenExp = experiences.childElementCount;
    if(lenExp > 1) {
        let delButton = document.getElementById("delete-button");
        delButton.removeAttribute("disabled");
    }
}

function deleteExperience(){
    let experiences = document.getElementById("experience-container");
    let lenExp = experiences.childElementCount;
    let latestExperience = experiences.children[lenExp - 1];
    experiences.removeChild(latestExperience);
    if(lenExp - 1 == 1) {
        let delButton = document.getElementById("delete-button");
        delButton.setAttribute("disabled", "");
    }
}