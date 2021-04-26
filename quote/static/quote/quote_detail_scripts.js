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

$("#createJobButton").click(function() {
    $.post("/quote/create-job", {'data': '{{object.id}}'}, function(data) {
        if (data['error']) {
            let error_msg = ""

            if ('address' in data['error'] == true) {
                error_msg = "<h3>A job at this address already exists!</h3>"
            }
            else {
                error_msg = "<h3>You must fill out all fields before you can create a job!</h3>"
            }
            $('#createJobError').html(error_msg);
            $('#createJobError').show();
        }
        else {
            window.location.href = data['success'];
        }
    });
});