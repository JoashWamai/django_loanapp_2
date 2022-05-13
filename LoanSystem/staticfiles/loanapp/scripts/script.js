$(document).ready(function(){

    let button = $('.action-btn');
    let close = $('#closeBtn');
    let form = $('.action-form');

        button.click(function(){
            form.addClass('active');
        });

        close.click(function(){
            form.removeClass('active');
        })

            /** Approval/Denial **/

    let approveBtn = $("#approve-btn");
    let rejectBtn = $("#reject-btn");

    approveBtn.click(function(e){
        e.preventDefault();
        let text = $('#text').val();
        let action = $(this).data('action');
        let customer = $(this).data('customer');


            $.ajax({
                    method:'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    url: '/loanaction/',
                    dataType:'json',
                    data:JSON.stringify({'action':action,'text':text,'customer':customer}),
                    success: function(response)
                        {
                           //swal('Success','Loan Successfully Approved','success');
                            window.location.href='/'
                        },
                     error: function()
                        {
                            alert('Error occured')
                        }
                })

    })

    rejectBtn.click(function(e){
        e.preventDefault();
        let text = $('#text').val();
        let action = $(this).data('action');
        let customer = $(this).data('customer');


            $.ajax({
                    method:'POST',
                    headers: {'X-CSRFToken': csrftoken},
                    url: '/loanaction/',
                    dataType:'json',
                    data:JSON.stringify({'action':action,'text':text,'customer':customer}),
                    success: function(response)
                        {
                            window.location.href='/'
                           // window.reload();
                        },
                     error: function()
                        {
                            alert('Error occured')
                        }
                })

    })

    /** Search **/


    let search = $('#term');

     search.keypress(function(e){

     let searchterm = $('#term').val();

     if(e.which == 13)
     {
          $.ajax({
          method:'post',
          headers: {'X-CSRFToken': csrftoken},
          url: '/search/',
          dataType:'json',
          data:JSON.stringify({'term':searchterm}),
          success: function(data)
            {
              // $("#searchres").html('<li>'+data+'</li>');

              if(data.length > 0)
              {
                 for(let i =0; i < data.length; i++)
                  {
                    $('#customertable tbody').
                    html('<tr>'+
                     '<td>'+ data[i].FirstName + ' '+ data[i].LastName +'</td>'+
                     '<td>'+ data[i].Id_Passport + '</td>'+
                     '<td>' + data[i].Email +'</td>'+
                     '<td> '+ data[i].Phone +'</td>'+
                     '<td>' + data[i].Gender +'</td>'+
                     '<td> '+ data[i].Location +'</td>'+
                     '<td>' + data[i].Dob + '</td>'+
                     '</tr>');
                  }
                }
               else
               {
                    swal.fire(title="Error",text="Customer not found", icon = "error");
                    search.val(' ');
               }


               console.log(data);
            },
          error: function(error,status)
            {
                //alert('Error occured')
                swal.fire(title="Error",text=status,icon="error")
                console.log(status)
            }
          });
        }
     });




});
