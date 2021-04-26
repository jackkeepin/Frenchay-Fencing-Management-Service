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
