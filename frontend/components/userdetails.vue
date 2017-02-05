<template>
<div class="container">
	<div id="article">
		<static_alert id="reg_alert" :status="status" :message="message"/>
		<div v-if="user">
			<h2>{{ user.name }}</h2>
			<h4 v-if="user.board">Board member</h4>
			<h4 v-else>Member</h4>
			<div v-if="is_self">
				<hr/>
				<h2>Details</h2>
				<hr/>
				<h2>Account settings</h2>
				<p>To change any of these settings, you have to provide your old password.</p>
				<transition-group name="fade">
					<static_alert id="acc_alert" v-for="a in account_alerts" :status="a.status" :message="a.message" :key="a"/>
				</transition-group>
				<form v-on:submit.prevent="change_account">
					<div class="form-group">
						<label for="email">Email:</label>
						<input type="email" class="form-control" v-model="email" name="email">
					</div>
					<div class="form-group">
						<label for="name">Full name:</label>
						<input type="text" class="form-control" v-model="name" name="name">
					</div>
					<div class="form-group" :class="{'has-error': old_password_wrong}">
						<label for="old_password">Old password:</label>
						<input type="password" class="form-control" v-model="old_password" name="old_password">
					</div>
					<div class="form-group">
						<label for="new_password">New password:</label>
						<input type="password" class="form-control" v-model="new_password" name="new_password">
					</div>
					<button type="submit" class="btn btn-default">Change</button>
				</form>
			</div>
			<br/>
		</div>
	</div>
</div>
</template>

<script>
import static_alert from './static_alert'
import User from '../model/user'

export default {
	data() {
		return {
			status: null,
			message: "",
			state: store,
			user: null,
			is_self: false,
			
			// account settings
			email: "",
			name: "",
			old_password: "",
			new_password: "",
			account_alerts: [],
			old_password_wrong: false,
		}
	},
	components: {
		static_alert: static_alert
	},
	
	methods: {
		change_account: function() {
			this.old_password_wrong = false
			this.account_alerts = []
			
			var d = {email: this.email, name: this.name,
					old_password: this.old_password, new_password: this.new_password}
			
			this.$http.post("/_user/change_account", this.state.add_session(d)).then(answer => {
				let body = JSON.parse(answer.body)
				if (body.error) {
					this.account_alerts.push({status: "danger", message: body.error.long})
					if (body.error.short == "wrong_password") {
						this.old_password_wrong = true
					}
				} else {
					for (var k in body.changes) {
						this.account_alerts.push(body.changes[k])
					}
				}
				delete User.cache.cache[this.state.session.UID]
			})
		},
		
		change_details: function() {
			
		}
	},
	
	mounted: function() {
		if (this.$route.query.code) {
			let d = {"UID": this.$route.params.UID, "registration_code": this.$route.query.code}
			this.$http.post("/_user/complete_registration", d).then(answer => {
				let body = JSON.parse(answer.body)
				if (body.success) {
					this.status = "success"
					this.message = body.success.long
				} else {
					this.status = "danger"
					if (body.error) {
						this.message = body.error.long
					} else {
						this.message = "Something went wrong, please try again."
					}
				}
				
				if (body.session) {
					this.state.login(body.session)
				}
				
				// remove query
				this.$router.replace({path: this.$route.path, params: this.$route.params})
			})
		}
		
		User.cache.find_by_key(parseInt(this.$route.params.UID),
			user => {
				this.user = user
				this.email = user.email
				this.name = user.name
			},
			error => {
				this.status = "danger"
				this.message = error.long
			}
		)
		
		this.is_self = (this.state.session && this.user.UID == this.state.session.UID)
	}
}
</script>

<style lang="scss">
@import "./style/variables.scss";

</style>
