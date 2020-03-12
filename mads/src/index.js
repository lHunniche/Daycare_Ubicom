const barcharts = require('./barchart.js')


function docReady(fn) {
    if (document.readyState === "complete" || document.readyState === "interactive") {
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

let initBtnListeners = () => {
    initChildSimBtn()
}

let initChildSimBtn = () => {
    let childBtn = document.getElementById("childBtn")
    childBtn.addEventListener("click", function() {
        $.ajax({
            url: "http://klevang.dk:8080/reset", success: function (result) {
                console.log(result)
            }
        });
    })
}

let addKinder = (kid) => {
    let kidContainer = document.getElementById("kid-container")
    let kidElement = createKidElement(kid)
    kidContainer.appendChild(kidElement)
}

let createKidElement = (kid) => {
    let kidElement = document.createElement("div")
    createElementAndAppend(kid.name, "span", kidElement)
    createElementAndAppend(kid.id, "span", kidElement)
    let check = kid.status ? "Checked in at " + getTime(kid.last_change): "Checked out at " + getTime(kid.last_change)
    createElementAndAppend(check, "span", kidElement)
    kidElement = setStatusColor(kid.status, kidElement)
    kidElement.className = "kid-element"
    return kidElement
}

let createElementAndAppend = (text,elementTag,parent) => {
    let textNode = document.createTextNode(text)
    let element = document.createElement(elementTag)
    element.appendChild(textNode)
    parent.appendChild(element)
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

let updateStats = (history) => {
    console.log(history)
    barcharts.setStats(history)
}

let pollKids = function () {
    $.ajax({
        url: "http://klevang.dk:8080/status", success: function (json) {
            addAllKids(json.children)
        }, dataType: "json", complete: pollKids, timeout: 30000
    });
}

let pollStats = () => {
    $.ajax({
        url: "http://klevang.dk:8080/stats", success: function (history) {
            updateStats(history)
        }, dataType: "json", complete: pollStats, timeout: 30000
    });
}

let initStats = () => {
    fetch('http://klevang.dk:8080/stats')
        .then(response => response.json())
        .then(history => console.log(history))
}



docReady(function () {
    initBtnListeners()
    fetchKids()
    initStats()
    pollKids()
    //pollStats()
    //barcharts.setStats()
});