<template>
<div class="login-form">
	<h3>Log in</h3>
	<form v-on:submit.prevent="login">
		<div class="form-group">
			<input type="email" class="form-control" id="email_input" name="email" placeholder="Email">
		</div>
		<div class="form-group">
			<input type="password" class="form-control" id="password_input" name="password" placeholder="Password">
		</div>
		<button type="submit" class="btn btn-default">Log in</button>
		<router-link to="/register"><button type="button" class="btn btn-default">Register</button></router-link>
	</form>
</div>
</template>

<script>
export default {
	data: () => {
		return {
			state: store
		};
	},
	methods: {
		// Called when login button is clicked
		login: function() {
			let email = document.getElementById("email_input").value;
			let password = document.getElementById("password_input").value;
			let d = {"email": email, "password": password}
			
			this.$http.post("/_user/login", d).then(answer => {
				console.log(answer);
				let body = JSON.parse(answer.body);
				console.log(body);
				
				if (body.login_session) {
					Cookies.set("login_session", body.login_session);
					this.state.login_session = body.login_session;
					//this.state.router.go("/");
				}
			});
		},
	}
}
</script>

<style lang="scss">
.login-form {
	padding: 1px 20px 20px 20px;

	h3 {
		padding-bottom: 10px;
	}
}
</style>
