<template>
    <div class="container">
        <div class="login-form">
            <h3>Login</h3>
            <form v-on:submit.prevent="login">
                <div class="form-group">
                    <label for="exampleInputEmail1">Username</label>
                    <input type="text" class="form-control" id="email_input" name="username" placeholder="Username">
                </div>
                <div class="form-group">
                    <label for="exampleInputPassword1">Password</label>
                    <input type="password" class="form-control" id="password_input" name="password" placeholder="Password">
                </div>
                <button type="submit" class="btn btn-default">Log in</button>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    data: () => {
        return {
            state: store
        };
    },
    methods: {
        // Called when login button is clicked
        login: function() {
            let username = document.getElementById("email_input").value;
            let password = document.getElementById("password_input").value;
            let fd = new FormData();
            fd.append("username", username);
            fd.append("password", password);

            console.log("'Login' button clicked with ", {username, password});

            this.$http.post("/client/login", fd).then(answer => {
                console.log(answer);
                let body = JSON.parse(answer.body);
                console.log(body);

                if (body.login_session) {
                    Cookies.set("login_session", body.login_session);
                    this.state.login_session = body.login_session;
                    this.state.router.go("/admin");
                }
            });
        }
    }
}
</script>

<style lang="scss">
.login-form {
    width: 40%;
    padding: 10px 20px 20px 20px;
    margin: auto;

    h3 {
        padding-bottom: 10px;
    }
}
</style>
