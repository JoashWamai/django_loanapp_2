$(document).ready(function(){


    const submit = $('#submit');


    submit.click(function(e){

        e.preventDefault();

        let name = $('#name').val();
        let phone = $('#phone').val();
        let amount = $('#amount').val();
        let type = $('#type').children('option:selected').val();

       $.ajax({
             method:'POST',
             headers: {'X-CSRFToken': csrftoken},
             url: '/payment/',
             dataType:'json',
             data:JSON.stringify({'name':name,'phone':phone,'amount':amount,'type':type}),
                success: function(response)
                    {
                        console.log(response);
                        swal('Success','Payment Succesfully Completed','success')
                    },
                 error: function(error,jqxhr,status)
                    {
                        swal('Error: '+error.status ,status ,'error')
                        console.log(error)
                        //location.reload();
                    }
        });

    });

});