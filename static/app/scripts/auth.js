
    function login (username, pass, cb) {
        if (localStorage.token) {
            if (cb) cb(true);
            return
        }
        getToken(username, pass, (res) => {
            if (res.authenticated) {
                localStorage.setItem('auth_token',res.token);
                if (cb) cb(true)
            } else {
                if (cb) cb(false)
            }
        })
    }

    function logout() {
        delete localStorage.auth_token
    }

     function loggedIn() {
        return !!localStorage.auth_token
    }

     function getToken(username, pass, cb) {
        $.ajax({
            type: 'POST',
            url: '/auth_token/',
            data: {
                username: username,
                password: pass
            },
            success: function(res){
                cb({
                    authenticated: true,
                    token: res.token
                })
            }
        })
    }
export {login,loggedIn,logout}