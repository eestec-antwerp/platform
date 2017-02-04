
import Vue from 'vue';

import front from './components/front';
import mainmenu from './components/mainmenu';
import news from './components/news';
import login from './components/login';
import register from './components/register';
import userdetails from './components/userdetails';

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
		{path: '/userdetails', component: userdetails},
	]
});

global.store = {
	session: undefined,
	cookies: require('js-cookie'),
	login_session: undefined,
	router: router,
}

var App = new Vue({
	router: router,
	components: {
		"front": front,
		"mainmenu": mainmenu,
		"login": login,
	}
}).$mount('#app');
