$(document).ready(function() {
	
	$(".vote").click(function(){
		console.log("click!")
		var pid = $(this).attr("post-id")
		if ($(this).hasClass("vote-up")) {
			var vote_type = 1;
		}
		else {
			var vote_type = -1;
		}
		$.ajax ({
			url: "/process_vote",
			type: "post",
			data: {pid:pid, vote_type:vote_type},
			success: function(result) {
					if(result.message == 'voteChanged'){
						console.log("vote changed!")
					
					$("div[up-down-id='" + pid + "']").html(result.vote_total)
					}
					else if(result.message == 'alreadyVoted'){
				
					$("#vote_msg").html('Already voted')
					console.log("Already voted!")
				}
			},
			error: function(error){
				console.log(error)
			}
		});
		// location.reload();

	});

	//FOLLOW OR UNFOLLOW
	$("#followOrUnfollow").click(function() {
		console.log("followed clicked")
		userID = $(this).attr("user-id")
		if ($(this).hasClass("follow-button")) {
			$.ajax ({
			url: "/follow_user",
			type: "post",
			data: {userID:userID},
			success: function(result) {
				
				if (result.message == 'userFollowed') {
					console.log("User followed!")
					$("div[user-name='" + userID + "']").html("<button class='btn btn-caution unfollow-button'>Unfollow</button>")
				}

			}
		});
		}
	
	})

	// PICK YOUR AVATAR
	$(".avatar").click(function() {
	
		if ($(this).hasClass("alien")){
			var avatar = "alien.png";
			console.log("click!");
		}
		else if ($(this).hasClass("chris")){
			var avatar = "chris_rock.png";
		}
		else if ($(this).hasClass("grandpa")){
			var avatar = "happy_grandpa.png" ;
		}
		else if ($(this).hasClass("man_red")){
			var avatar = "man_red_background.png";
		}
		else if ($(this).hasClass("man_sad")){
			var avatar = "man_sad.png";
		}
		else if ($(this).hasClass("vampire")){
			var avatar = "vampire.png" ;
		}
		else if ($(this).hasClass("wolverine")){
			var avatarI = "wolverine.png" ;
		}
		else if ($(this).hasClass("woman_shades")){
			var avatar = "woman_shades.png";
		}
		else if ($(this).hasClass("woman_violet")){
			var avatar = "woman_violet.png";
		}
		else if ($(this).hasClass("zombie")){
			var avatar = "zombie.png" ;
		}
		else if ($(this).hasClass("woman_pink")){
			var avatar = "woman_pink_hair.png" ;
		}
		else if ($(this).hasClass("woman_grey_hair")){
			var avatar = "woman_grey_hair.png";
		}
		else if ($(this).hasClass("woman_grey")){
			var avatar = "woman_grey.png";
		}
		else if ($(this).hasClass("dead_bee")){
			var avatar = "dead_bee.png" ;
		}
		// location.reload();
		$.ajax ({
			url: "/edit_avatar",
			type: "post",
			data: {avatar:avatar},
			success: function(result) {
				console.log("Avatar changed!")
			}
		});
		
		

	})

	return false;
});