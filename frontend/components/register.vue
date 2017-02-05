<template>
<div class="container">
	<div id="article" class="register">
		<div class="article-title">Register</div>
		<hr>
		<div class="post">
		Blablabla short intro on eestec membership
		<hr>
		
		<form v-on:submit.prevent="register">
			<div class="form-group">
				<input type="email" class="form-control" v-model="email" name="email" placeholder="Email">
			</div>
			<div class="form-group">
				<input type="text" class="form-control" v-model="name" name="name" placeholder="Full name">
			</div>
			<div class="form-group">
				<input type="password" class="form-control" v-model="password" name="password" placeholder="Password">
			</div>
			<button type="submit" class="btn btn-default">Register</button>
		</form>
		
		<static_alert id="reg_alert" :status="reg_status" :message="reg_message"/>
		
		</div>
	</div>
</div>
</template>

<script>
import static_alert from './static_alert';

export default {
	data() {
		return {
			reg_status: null,
			reg_message: "",
			email: "",
			password: "",
			name: "",
		}
	},
	
	methods: {
		// Called when login button is clicked
		register: function() {
			this.reg_status = null;
			let d = {"email": this.email, "name": this.name, "password": this.password}
			
			this.$http.post("/_user/register", d).then(answer => {
				let body = JSON.parse(answer.body);
				console.log(body);
				
				if (body.error) {
					this.reg_status = "danger"
					this.reg_message = body.error.long
				} else {
					this.reg_status = "success"
					this.reg_message = "Success! Please check your email to complete the registration."
				}
			});
		},
	},
	
	components: {
		static_alert: static_alert
	}
}

</script>

<style lang="scss">
@import "./style/variables.scss";

.register .alert {
	margin-top: 15px;
}
</style>
