$(document).ready(function() {
	$(".vote").click(function(){
		var pid = $(this).attr("post_id")
		if $((this).hasClass("vote-up")) {
			var voteType = 1;
		}
		else {
			var voteType = -1;
		}
		$.ajax ({
			url: "/process_vote",
			type: "post",
			data: {pid:pid, vote_type:vote_type},
			success: function(result) {

			}
		});

	});
});