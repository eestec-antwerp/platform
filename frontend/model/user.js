
import Cache from './cache'

class User {
	constructor(d) {
		this.UID = d.UID
		this.email = d.email
		this.name = d.name
		this.level = d.level
	}

	get board() {
		return this.level == "BOARD" || this.level == "ADMIN"
	}

}

User.cache = new Cache(User, "/_user")

export default User;
