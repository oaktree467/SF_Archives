
var data;
$.ajax({
    //Change URL below as needed; must be local file due to CORS issues
    url: "Issue Grid_ The Magazine of Fantasy and Science Fiction.html",
    dataType: "html",
    success: function( response ) {
        data = response;
        $("body").html(data);
    }
}).then( function () {
    console.log($("a"));
});