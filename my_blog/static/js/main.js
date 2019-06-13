$(document).ready(function () {

    console.log("it's working")
    
	$("#forms").css("height", $(window).height());
	$("#forms").css('height', $(window).height());
	$(".profile").css("min-height", $(window).height());

});


$(document).ready(function() {

	// show hide delete

	$(".main_post #delete_button").click(function (event) { 

		event.preventDefault(); // prevent the browser to browse this link [href="#"]
		$("#delete_post").toggle();
	});

	// show replay comment

	$(".comment_section #reply_comment").click(function (event) { 
		
		event.preventDefault();  // prevent the browser to browse this link [href="#"]
		$(this).parent().parent().toggleClass("active");
	});

	// inserting img-fluid 

	$(".post_content img, .post .card-body img").addClass("img-fluid");

	// make our [Create] content real time preview

    var titleItem = $("#post_create input#id_title"),
		content = $("#post_create #id_content"),
		previewTitle = $("#post_create #preview_title"), 
		previewContent = $("#post_create #preview_content");
	
	previewTitle.text(titleItem.val());

	titleItem.keyup(function () {
		previewTitle.text(titleItem.val());
	});
	
	function setContent(value) {
		var markedContent = marked(value)
		previewContent.html(markedContent)
		$("#post_create #preview_content img").each(function () {
			$(this).addClass("img-fluid")
		})
	}

	setContent(content.val());

	content.keyup(function() { 
		var new_content = $(this).val()
		setContent(new_content)	
	});

});

