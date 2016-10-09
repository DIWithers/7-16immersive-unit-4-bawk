$(document).ready(function() {
	$(".vote").click(function(){
		var pid = $(this).attr("post_id")
		if $((this).hasClass("vote-up")) {
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

			}
		});

	});
	$(".avatar").click(function() {
		console.log("click!");
		if $((this).hasClass("alien")){
			var avatarImg = "alien.png";
		}
		if $((this).hasClass("chris")){
			var avatarImg = "chris_rock.png";
		}
		if $((this).hasClass("grandpa")){
			var avatarImg = "happy_grandpa.png" ;
		}
		if $((this).hasClass("man_red")){
			var avatarImg = "man_red_background.png";
		}
		if $((this).hasClass("man_sad")){
			var avatarImg = "man_sad.png";
		}
		if $((this).hasClass("vampire")){
			var avatarImg = "vampire.png" ;
		}
		if $((this).hasClass("wolverine")){
			var avatarImg = "wolverine.png" ;
		}
		if $((this).hasClass("woman_shades")){
			var avatarImg = "woman_shades.png";
		}
		if $((this).hasClass("woman_violet")){
			var avatarImg = "woman_violet.png";
		}
		if $((this).hasClass("zombie")){
			var avatarImg = "zombie.png" ;
		}
		if $((this).hasClass("woman_pink")){
			var avatarImg = "woman_pink_hair.png" ;
		}
		if $((this).hasClass("woman_grey_hair")){
			var avatarImg = "woman_grey_hair.png";
		}
		if $((this).hasClass("woman_grey")){
			var avatarImg = "woman_grey.png";
		}
		if $((this).hasClass("dead_bee")){
			var avatarImg = "dead_bee.png" ;
		}

		$.ajax ({
			url: "/edit_avatar",
			type: "post",
			data: {avatarImg:avatarImg},
			success: function(result) {

			}
		});
	})

	// ##########  AVATAR CLICKS  #####################
	// $("#alien.png").click(change_avatar("alien.png"));
	// $("#chris_rock.png").click(change_avatar("chris_rock.png"));
	// $("#happy_grandpa.png").click(change_avatar("happy_grandpa.png"));
	// $("#man_red_background.png").click(change_avatar("man_red_background.png"));
	// $("#man_sad.png").click(change_avatar("man_sad.png"));
	// $("#vampire.png").click(change_avatar("vampire.png"));
	// $("#wolverine.png").click(change_avatar("wolverine.png"));
	// $("#woman_shades.png").click(change_avatar("woman_shades.png"));
	// $("#woman_violet.png").click(change_avatar("woman_violet.png"));
	// $("#zombie.png").click(change_avatar("zombie.png"));
	// $("#woman_pink_hair.png").click(change_avatar("woman_pink_hair.png"));
	// $("#woman_grey_hair.png").click(change_avatar("woman_gray_hair.png"));
	// $("#woman_grey.png").click(change_avatar("woman_grey.png"));
	// $("#dead_bee.png").click(change_avatar("dead_bee.png"));
	// # # # # # #

});