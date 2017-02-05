
import Vue from 'vue';

import front from './components/front';
import mainmenu from './components/mainmenu';
import news from './components/news';
import login from './components/login';
import register from './components/register';
import userdetails from './components/userdetails';
import static_alert from './components/static_alert';

var VueResource = require('vue-resource');
Vue.use(VueResource);

var VueRouter = require('vue-router');
Vue.use(VueRouter);

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
	login: undefined,
	add_login: function(d) {
		d["login"] = this.login
		return d
	}
}

store.login = JSON.parse(store.cookies.get("login"))

var App = new Vue({
	router: router,
	components: {
		front: front,
		mainmenu: mainmenu,
		login: login,
		static_alert: static_alert
	}
}).$mount('#app');
