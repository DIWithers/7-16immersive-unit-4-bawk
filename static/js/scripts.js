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
				// console.log("RESULT" + result)
			},
			error: function(error){
				console.log(error)
			}
		});

	});

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

		$.ajax ({
			url: "/edit_avatar",
			type: "post",
			data: {avatar:avatar},
			success: function(result) {
				console.log("Avatar changed!")
			}
		});
		console.log("doubleclick" + avatar)
	})

	return false;
});