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
    //console.log(kid)
    let kidContainer = document.getElementById("kid-container")
    let kidElement = createKidElement(kid)
    kidContainer.appendChild(kidElement)
}

let createKidElement = (kid) => {
    let kidElement = document.createElement("div")
    let name = document.createTextNode(kid.name)
    let id = document.createTextNode(kid.id)
    let check = kid.status ? "Checked in at " : "Checked out at "
    //let timestamp = document.createTextNode(check + getTime())
    let timestamp = document.createTextNode(check + getTime(kid.last_change))
    let nameSpan = document.createElement("span")
    nameSpan.appendChild(name)
    let idSpan = document.createElement("span")
    idSpan.appendChild(id)
    let timestampSpan = document.createElement("span")
    timestampSpan.appendChild(timestamp)
    kidElement = setStatusColor(kid.status, kidElement)
    kidElement.appendChild(nameSpan)
    kidElement.appendChild(idSpan)
    kidElement.appendChild(timestampSpan)
    kidElement.className = "kid-element"
    return kidElement
}

let getTime = (timestamp) => {
    if (timestamp == "") {
        return "No changes yet"
    } else {
        return timestamp
    }
}

let setStatusColor = (status, element) => {
    if (status == false) {
        element.style.backgroundColor = "red"
    } else {
        element.style.backgroundColor = "green"
    }
    return element
}

let clearKids = () => {
    var e = document.querySelector("#kid-container");
    if (e.childElementCount > 0) {
        var child = e.lastElementChild;
        while (child) {
            e.removeChild(child);
            child = e.lastElementChild;
        }
    }

}

let addAllKids = (allKids) => {
    clearKids()
    for (kid of allKids) {
        addKinder(kid)
    }
}

let fetchKids = () => {
    fetch('http://klevang.dk:8080/status')
        .then(response => response.json())
        .then(json => addAllKids(json.children))
}

let poll = function () {
    $.ajax({
        url: "http://klevang.dk:8080/status", success: function (json) {
            addAllKids(json.children)
        }, dataType: "json", complete: poll, timeout: 30000
    });
}

docReady(function () {
    fetchKids()
    poll()
});