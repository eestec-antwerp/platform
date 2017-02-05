<template>
<transition name="fade" mode="out-in">
	<div class="login" v-if="state.current_user" key="loggedin">
		<h4>Hi {{ state.current_user.name }}!</h4>
		<button class="btn btn-default" v-on:click="logout">Log out</button>
		<router-link :to="'/userdetails/' + state.session.UID">
			<button class="btn btn-default">My Profile</button>
		</router-link>
	</div>
	<div class="login" v-else key="notloggedin">
		<h4>Log in</h4>
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
</transition>
</template>

<script>
import static_alert from './static_alert'

import User from '../model/user'

export default {
	data: () => {
		return {
			state: store,
			login_status: null,
			login_wrong: null,
			login_message: "",
			email: "",
			password: "",
			User: User
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
				
				if (body.session) {
					this.state.login(body.session)
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
			let d = {"login": this.state.session}
			this.$http.post("/_user/logout", this.state.add_session(d))
			this.state.logout()
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

	h4 {
		padding-bottom: 10px;
	}
	
	.alert {
		margin-top: 15px;
	}
}
</style>
