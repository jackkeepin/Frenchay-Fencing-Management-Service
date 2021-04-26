$( document ).ready(function() {
    let materials = $("#materials").html()
    
    let regex = /'|\[|\]/g;

    materials = materials.replace(regex, '')

    let split_mats = materials.split(", ");

    $("#materials").html("")
    split_mats.forEach(function (material, index) {
        $("#materials").append(material + "<br>");
    });
});

$("#sendInvoiceButton").click(function() {
    // show loading message
    $('.loader').show();
    $('#sendingEmail').show();

    $.post("/job/send-invoice", {'data': '{{object.id}}'}, function(data) {
        // hide loading message
        $('.loader').hide();
        $('#sendingEmail').hide();
        if (data['status'] == 'error') {
            let error_msg = "<h3 id='emailFeedback'>Failed to send email. Please check the customer email is correct.</h3>";

            $('#sendEmailError').html(error_msg);
            $('#sendEmailError').show();
        }
        else {
            let success_msg = "<h3 id='emailFeedback'>Invoice sent sucessfully</h3>";

            $('#sendEmailSuccess').html(success_msg);
            $('#sendEmailSuccess').show();
        }
    });
});