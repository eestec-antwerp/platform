
import Vue from 'vue'

// Despite the name, this does more than just caching and is a general way to get
// several types of classes (i.e. those in 'model') from the server
class Cache {
	constructor(cls, path, state) {
		this.cls = cls
		this.path = path
		this.state = state
		this.cache = {}
	}
	
	find_by_key(key, found, error = (e => console.log(e))) {
		var d = {key: key}
		if (this.state.login) {
			d.login = this.state.login
		}
		
		var obj = this.cache[key]
		if (obj) {
			return func(obj)
		} else {
			Vue.http.post(this.path + "/get", d).then(answer => {
				let body = JSON.parse(answer.body)
				if (body.error) {
					error(body.error)
				} else {
					obj = new this.cls(body.what)
					this.cache[key] = obj
					found(obj)
				}
			})
		}
	}
}

export default Cache
