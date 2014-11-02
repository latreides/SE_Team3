google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable([
        ['Rank', 'Count'],
        ['Rank 1', 5],
        ['Rank 2', 8],
        ['Rank 3', 7],
        ['Rank 4', 6],
        ['Rank 5', 15],
        ['Unranked', 4]
    ]);

    var options = {
        width: 400,
        height: 300,

        title: 'Deck Rankings',
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
            'height': '81%'
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
        }
    };

    var chart = new google.visualization.PieChart(document.getElementById('piechart'));

    chart.draw(data, options);
}

(function($){
    $.fn.displaydecks = function(){
        return this.each(function(){
            obj = $(this)
            obj.find('.button').click(function() {
                obj.find('.menu').fadeIn(400);
                
                obj.find('.menu').hover(function(){ },
                    function(){
                        $(this).fadeOut(400);
                    }
                );
            });
            
            obj.find('.menu li').click(function() {
            obj.find('.button')
                
                
            obj.find('.menu').fadeOut(400);
            });
        });
    };
})(jQuery);
        
$(function(){
    $('.switch').displaydecks();
});