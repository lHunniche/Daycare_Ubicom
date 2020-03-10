function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}


let addKinder = (kid) => {
    console.log(kid)
    let kidContainer = document.getElementById("kid-container")
    let kidElement = createKidElement(kid)
    kidContainer.appendChild(kidElement)
}

let createKidElement = (kid) => {
    let kidElement = document.createElement("div")
    let name = document.createTextNode(kid.name)
    let id = document.createTextNode(kid.id)
    let nameSpan = document.createElement("span")
    nameSpan.appendChild(name)
    let idSpan = document.createElement("span")
    idSpan.appendChild(id)
    kidElement = setStatusColor(kid.status, kidElement)
    kidElement.appendChild(nameSpan)
    kidElement.appendChild(idSpan)
    kidElement.className = "kid-element"
    return kidElement
} 

let setStatusColor = (status, element) => {
    if(status == false){
        element.style.backgroundColor = "red"
    }else {
        element.style.backgroundColor = "green"
    }
    return element
}

let addAllKids = (allKids) => {

    for(kid of allKids) {
        addKinder(kid)
    }
}

let fetchKids = () => {
    fetch('http://klevang.dk:8080/status')
        .then(response => response.json())
        .then(json => addAllKids(json.children))
}


docReady(function () {
    fetchKids()
});