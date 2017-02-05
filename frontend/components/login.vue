<template>
<div class="login" v-if="state.login">
	<h3>Hi user {{ state.login.UID }}</h3>
	<button class="btn btn-default" v-on:click="logout">Log out</button>
</div>
<div class="login" v-else>
	<h3>Log in</h3>
	<form v-on:submit.prevent="login">
		<div class="form-group" :class="{'has-error': login_wrong == 'email'}">
			<input type="email" class="form-control" v-model="email" name="email" placeholder="Email">
		</div>
		<div class="form-group" :class="{'has-error': login_wrong == 'password'}">
			<input type="password" class="form-control" v-model="password" name="password" placeholder="Password">
		</div>
		<button type="submit" class="btn btn-default">Log in</button>
		<router-link to="/register"><button type="button" class="btn btn-default">Register</button></router-link>
	</form>
	
	<static_alert id="reg_alert" :status="login_status" :message="login_message"/>
</div>
</template>

<script>
import static_alert from './static_alert';

export default {
	data: () => {
		return {
			state: store,
			login_status: null,
			login_wrong: null,
			login_message: "",
			email: "",
			password: "",
		};
	},
	methods: {
		// Called when login button is clicked
		login: function() {
			this.login_status = null
			this.login_wrong = null
			let d = {"email": this.email, "password": this.password}
			
			this.$http.post("/_user/login", d).then(answer => {
				let body = JSON.parse(answer.body)
				
				if (body.login) {
					this.state.cookies.set("login", body.login)
					this.state.login = body.login
				} else if (body.error) {
					this.login_status = "warning"
					if (body.error.short == "wrong_password") {
						this.login_message = "Wrong password"
						this.login_wrong = "password"
					} else if (body.error.short == "not_single") {
						this.login_message = "Unknown email"
						this.login_wrong = "email"
					} else {
						this.login_message = body.error.long
					}
				}
			});
		},
		
		logout: function() {
			let d = {"login": this.state.login}
			this.$http.post("/_user/logout", this.state.add_login(d))
			this.state.login = undefined
			this.state.cookies.remove("login")
		}
	},
	components: {
		static_alert: static_alert
	}
}
</script>

<style lang="scss">
.login {
	padding: 1px 20px 20px 20px;

	h3 {
		padding-bottom: 10px;
	}
}
</style>
