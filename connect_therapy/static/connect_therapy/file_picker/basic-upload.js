$(function () {
    /* 1. OPEN THE FILE EXPLORER WINDOW */
    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
    $("#fileupload").fileupload({
        dataType: 'json',
        formData: {'text': 'hello'},
        done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
            if (data.result.is_valid) {
                // if valid data, then append it to the upload table
                var uploadedFiles = data.result.uploaded_files;
                document.getElementById("uploaded-table").style.display = "block";
                $("#uploaded-table").prepend(
                    "<tr><td><a target='_blank' href=" + uploadedFiles[1] + ">" + uploadedFiles[0] + "</a></td></tr>"
                )
            }
        },
        progressall: function (e, data) {
            // find and update the progress bar
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").html(strProgress);
        },
        start: function (e, data) {
            // reset the progress bar when a new upload starts
            $(".progress-bar").css({"width": "0%"});
            $(".progress-bar").html("0%");
        }

    });

});