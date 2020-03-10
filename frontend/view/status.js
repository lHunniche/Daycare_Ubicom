function startCheck(callback) {
    setInterval(() => {
        var request = new XMLHttpRequest()

        request.open('GET', 'http://klevang.dk:8080/status', true)
        
        request.addEventListener('load', () => {
            var text = request.responseText;
            var response = JSON.parse(text);
            callback(response);
        });
        
        // Send request
        request.send()
        
    }, 5000);
}


json = `{"status": true}`

startCheck(response => {
    console.log(response);

    var isHere = /* Figure this out */

    var check = document.querySelector('#shs .check');
    check.classList.toggle('is-here', isHere);
    
})

function updateCheckIn(status) {

}