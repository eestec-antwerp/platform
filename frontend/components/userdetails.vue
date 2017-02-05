<template>
<div class="container">
	<div id="article">
		userdetails for {{ $route.params.UID }}
		<static_alert id="reg_alert" :status="status" :message="message"/>
	</div>
</div>
</template>

<script>
import static_alert from './static_alert'

export default {
	data() {
		return {
			status: null,
			message: "",
			is_self: false,
			state: store
		}
	},
	components: {
		static_alert: static_alert
	},
	methods: {},
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
				
				if (body.login) {
					Cookies.set("login", body.login);
					this.state.login = body.login;
				}
			})
		}
	}
}
</script>

<style lang="scss">
@import "./style/variables.scss";

</style>
