google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

var rankArray = []
var rankData = [
        ['Rank', 'Count'],
        ['Rank 1', 0],
        ['Rank 2', 0],
        ['Rank 3', 0],
        ['Rank 4', 0],
        ['Rank 5', 0],
        ['Unranked', 0]
    ]

/* Dynamically adjust the pie chart weight for the rank data */
function calculateRankData()
{
    for (var i = 0; i < cardRanks.length; i++) {
        rankData[cardRanks[i]][1]++;

    }
}

function drawChart() {
    calculateRankData();
    var data = google.visualization.arrayToDataTable(rankData);

    var options = {
        width: 400,
        height: 300,
        sliceVisibilityThreshold: 0,

        title: 'Card Rankings',
        titleTextStyle: {
            color: 'white',
            fontName: 'Microsoft Sans Serif',
            fontSize: 24
        },
                
        tooltip: {
            textStyle: {
                fontName: 'Microsoft Sans Serif',
                fontSize: 14
            }
        },

        chartArea : {
            'width': '95%',
            'height': '81%',
        },

        colors: ['#00F2FF', '#45FF45', 'yellow', 'orange', 'red', '#000000'],
        backgroundColor: '#383838',
        fontName: 'Microsoft Sans Serif',
        legend : {
            position: 'right',
            textStyle : {
                color: 'white',
                fontSize: 14
            }
        },

        pieSliceTextStyle: {
            color: 'black',
            fontName: 'Microsoft Sans Serif',
            fontSize: 14
        },

        slices: {
            5: {
                textStyle: {
                    color: 'white'
                }
            }
        }
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}
