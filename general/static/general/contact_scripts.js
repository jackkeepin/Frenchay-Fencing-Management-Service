$(document).ready(function () {
    $('#submitButton').click(function () {

        var name = $("#name").val();
        var email = $("#email").val();
        var number = $("#number").val();
        var message = $("#message").val();

        $.post("/contact", {
            name: name,
            email: email,
            number: number,
            message: message
        }, function(data) {
            if (data['status'] == 'error') {
                let error_msg = "Sorry, there was a problem sending your message. Please make sure all fields have been filled out. If the problem continues, please contact us directly using the details above."
                $('#errorMessage').html(error_msg);
                $('#errorMessage').show();
            }
            else {
                window.location.href = data['success'];
            }
        });
    });
});