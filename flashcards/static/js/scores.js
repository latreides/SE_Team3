google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Rank', 'Count'],
        ['Rank 1', 1],
        ['Rank 2', 2],
        ['Rank 3', 3],
        ['Rank 4', 4],
        ['Rank 5', 5],
        ['Unranked', 6]
    ]);

    var options = {
        width: 400,
        height: 300,

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