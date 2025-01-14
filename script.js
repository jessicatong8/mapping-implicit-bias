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

// State Map
d3.csv('https://raw.githubusercontent.com/jessicatong8/mapping-implicit-bias/main/data/old-csv-data/2020_state_fromcsv.csv').then(function(rows) {
    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    }
    // console.log(rows);

    var data = [{
        type: 'choropleth',
        locationmode: 'USA-states',
        locations: unpack(rows, 'State'),
        z: unpack(rows, 'Average Score'),
        text: unpack(rows, 'State'),
        colorscale: [
            [0, '#dfffe2'], [0.2, '#b3e3cf'],
            [0.4, '#69b8b0'], [0.6, '#3a91a1'],
            [0.8, '#21728e'], [1, '#123f5a']
        ],
        colorbar: {
                len:1, 
                title: "Average Score", 
                titleside:'right',
                // ticklabelposition: 'left',
                orientation:'v',
            },
    }];

    var layout = {
        title: { text: 'Implicit Racial Bias' },
        geo: {
            scope: 'usa',
            countrycolor: 'rgb(255, 255, 255)',
            showlakes: false,
            margin: { t: 0, b: 0, l: 0, r: 0 }
        },
    };

    Plotly.newPlot("stateMap", data, layout, { showLink: false });
}).catch(function(error) {
    console.error("Error loading CSV data:", error);
});

// County Map
d3.json('https://raw.githubusercontent.com/jessicatong8/mapping-implicit-bias/main/geojson/us-counties.json', function(myjson) {
    d3.csv('https://raw.githubusercontent.com/jessicatong8/mapping-implicit-bias/main/data/old-csv-data/2020_county_fromcsv.csv').then(function(rows) {
        function unpack(rows, key) {
            return rows.map(function(row) { return row[key]; });
        }
        console.log(rows);

        var data = [{
            type: 'choropleth',
            // locationmode: 'geojson-id',
            locations: unpack(rows, 'fips'),
            z: unpack(rows, 'avgScore'),
            // text: unpack(rows, 'State'),
            colorscale: [
                [0, '#dfffe2'], [0.2, '#b3e3cf'],
                [0.4, '#69b8b0'], [0.6, '#3a91a1'],
                [0.8, '#21728e'], [1, '#123f5a']
            ],
            colorbar: {
                    len:1, 
                    title: "Average Score", 
                    titleside:'right',
                    // ticklabelposition: 'left',
                    orientation:'v',
                },
            geojson: myjson,
            featureidkey: 'id'
        }];

        var layout = {
            title: { text: 'Implicit Racial Bias' },
            geo: {
                // scope: 'usa',
                countrycolor: 'rgb(255, 255, 255)',
                showlakes: false,
                margin: { t: 0, b: 0, l: 0, r: 0 }
            },
        };

        Plotly.newPlot("countyMap", data, layout, { showLink: false });
    }).catch(function(error) {
        console.error("Error loading CSV data:", error);
    });
});