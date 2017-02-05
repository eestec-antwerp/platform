
import Vue from 'vue'

import front from './components/front'
import mainmenu from './components/mainmenu'
import news from './components/news'
import login from './components/login'
import register from './components/register'
import userdetails from './components/userdetails'
import static_alert from './components/static_alert'

import Cache from './model/cache'
import User from './model/user'

var VueResource = require('vue-resource')
Vue.use(VueResource)

var VueRouter = require('vue-router')
Vue.use(VueRouter)

var router = new VueRouter({
	mode: 'history',
	routes: [
		{path: '/', component: front},
		{path: '/news', component: news},
		{path: '/register', component: register},
		{path: '/userdetails/:UID', component: userdetails},
	]
});

global.store = {
	cookies: require('js-cookie'),
	session: undefined,
	add_session: function(d) {
		d["session"] = this.session
		return d
	},
	
	current_user: undefined,
	login: function(session, error = (e => console.log(e))) {
		this.session = session
		this.cookies.set("session", session)
		Vue.http.post("/_user/check_session", this.add_session({})).then(answer => {
			var body = JSON.parse(answer.body)
			if (body.error) {
				console.log("Session not recognized by server, logging out.")
				this.logout()
			}
		})
		User.cache.find_by_key(session.UID, u => {
			this.current_user = u
		}, error)
	},
	logout: function() {
		this.session = undefined
		this.current_user = undefined
		this.cookies.remove("session")
	}
}

if (store.cookies.get("session")) {
	store.login(JSON.parse(store.cookies.get("session")))
}

var App = new Vue({
	router: router,
	components: {
		front: front,
		mainmenu: mainmenu,
		login: login,
		static_alert: static_alert
	},
	mounted: function() {
		router.afterEach((to, from) => {
			//console.log(jQuery)
			jQuery('.navbar-collapse').collapse('hide')
		})
	}
}).$mount('#app')
