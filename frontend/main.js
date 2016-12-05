
import app from './app';

global.store = {
	session: undefined,
	cookies: require('js-cookie'),
	login_session: undefined,
	// Cache for job results
	jobs: [],
	router: new VueRouter({
		history: true
	})
}

store.router.map({
	'/login': {
		component: Login
	},
});


store.router.redirect({
	'/a': '/b',
});

store.router.start(app, 'app');
