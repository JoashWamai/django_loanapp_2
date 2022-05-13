$(document).ready(function(){

    /*** LOAN STATUS PIECHART ***/

    let piechart = $('#piechart_status');

    $.ajax({
    url:piechart.data('url'),
    success:function(data)
    {
        let ctx = piechart[0].getContext("2d");

        new Chart(ctx,{
            type:'doughnut',
            data:{
                labels:data.labels,
                datasets:[{
                label:'Loans',
                backgroundColor:['red','blue','black','orange','green'],
                data:data.data
                }]
            },
            options:{
                responsive:true,
                legend:{
                    position:'right'
                },
                title:{
                display:true,
                text:'Loans Status'
                }
            }
        })
    }

    });

    /*** BUSINESS TYPE BAR GRAPH ***/

   let bargraph = $('#bargraph_type');

    $.ajax({
    url:bargraph.data('url'),
    success:function(data)
    {
        let ctx = bargraph[0].getContext("2d");

        new Chart(ctx,{
            type:'bar',
            data:{
                labels:data.labels,
                datasets:[{
                label:'Loans',
                backgroundColor:['red','blue','black','orange','green'],
                data:data.data
                }]
            },
            options:{
                responsive:true,
                legend:{
                    position:'right'
                },
                title:{
                display:true,
                text:'Levels of enterprises',
                },
                scales:{
                    y:{
                       // beginAtZero:true
                        min:0
                    }
                  }
            }
        })
    }

    });


});