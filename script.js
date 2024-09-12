document.getElementById('stateButton').addEventListener('click', function() {
    console.log("stateButton clicked");
    document.getElementById('stateMap').classList.remove('hidden');
    document.getElementById('countyMap').classList.add('hidden');
});

document.getElementById('countyButton').addEventListener('click', function() {
    document.getElementById('countyMap').classList.remove('hidden');
    document.getElementById('stateMap').classList.add('hidden');
});