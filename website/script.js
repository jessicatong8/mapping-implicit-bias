document.getElementById('stateButton').addEventListener('click', function() {
    document.getElementById('stateMap').classList.remove('hidden');
    document.getElementById('countyMap').classList.add('hidden');
    document.getElementById('stateButton').classList.add('disabled');
    document.getElementById('countyButton').classList.remove('disabled');
});

document.getElementById('countyButton').addEventListener('click', function() {
    document.getElementById('countyMap').classList.remove('hidden');
    document.getElementById('stateMap').classList.add('hidden');
    document.getElementById('countyButton').classList.add('disabled');
    document.getElementById('stateButton').classList.remove('disabled');
});