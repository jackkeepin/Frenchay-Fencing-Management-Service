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


!function(d,s,id) {
    var js,fjs=d.getElementsByTagName(s)[0];
    if (!d.getElementById(id)){
        js=d.createElement(s);
        js.id=id;
        js.src='https://weatherwidget.io/js/widget.min.js';
        fjs.parentNode.insertBefore(js,fjs);
    }
}
(document,'script','weatherwidget-io-js');