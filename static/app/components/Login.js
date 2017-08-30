import React, { Component } from 'react'
// import ReactDOM from 'react-dom'
import {login, loggedIn, logout} from '../scripts/auth'
export default class Login extends Component {
    constructor(props){
        super(props);
        Login.loginCheck.bind(this)
    }
  handleSubmit(e) {
    e.preventDefault();
    var username = this.refs.username.value
        var pass = this.refs.password.value

        login(username, pass, (loggedIn) => {

        })
    // let formData = new FormData();
    // let csrftoken = Cookies.get('csrftoken');
    // let headers = new Headers();
    // headers.append("X-CSRFToken",csrftoken);
    // formData.append('username', ReactDOM.findDOMNode(this.refs.username).value);
    // formData.append('password', ReactDOM.findDOMNode(this.refs.password).value);
    // fetch("/api-token-auth",{
    //     method:"POST",
    //
    //     body: formData,
    //
    // }).then(res=>{console.log(res); return res.json()}).
    //     then(res=>{localStorage.setItem('auth_token',res.token); alert(localStorage.getItem('auth_token'))}).
    //     catch(alert)

  }
  static loginCheck(nextState, replace){
      if (!loggedIn()) {
        replace('/login')

      }
  }
  static logoutHandler(el) {
        logout();
        console.log(el);
        console.log(el.context);
        el.context.router.browser.replace('/login')


    }
  render() {
    return (
      <div className='row'>
        <div className='col-md-12'>Пожалуйста, введите логин:</div>
        <form className='col-md-4' onSubmit={this.handleSubmit.bind(this)}>
            <input type="text" ref="username" name="username"/>
            <input type="password" ref="password" name="password"/>
            <button type="submit">Отправить</button>
        </form>
      </div>
    )
  }
}