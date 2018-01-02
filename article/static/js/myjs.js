$(document).ready(function($) {
    $("#btn-follow").click(function() {
        alert("Click!")
            $.getJSON("{% url 'ajax-follow' author.pk %}", function(ret){
                    if (ret == "Follow")
                        alert("Has follow");
                    else
                        alert("Not follow");
            });
    });
})