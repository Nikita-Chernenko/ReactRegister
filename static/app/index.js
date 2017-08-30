import React, {Component} from 'react'
import {render} from 'react-dom'
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom'
import MarkList from './components/MarkList'
import ClassTimeList from './components/ClassTimeList'
import AbsenceList from './components/AbsenceList'
import Login from './components/Login'
import {logout} from './scripts/auth'


class Lists extends Component {
    render() {
       return <main>
            <Switch>
                <Route path='/classtime' component={ClassTimeList} onEnter={Login.loginCheck}/>
                <Route path='/mark' component={MarkList} onEnter={Login.loginCheck}/>
                <Route path='/absence' component={AbsenceList} onEnter={Login.loginCheck}/>
                <Route path='/login' component={Login}/>
            </Switch>
        </main>
    }
}

class Header extends Component {

    render() {
        return <header>
            <nav>
                <ul>
                    <li><Link to='/classtime'>ClassTimeList</Link></li>
                    <li><Link to='/mark'>MarkList</Link></li>
                    <li><Link to='/absence'>AbsenceList</Link></li>
                    <li><Link to='/login'>Login</Link></li>
                    <li><button onClick={() => Login.logoutHandler(this)}>Log out</button></li>
                </ul>
            </nav>
        </header>
    }

}

const App = () => (
    <div>
        <Header/>
        <Lists/>
    </div>
)
render(
    <BrowserRouter>
        <App/>
    </BrowserRouter>,
    document.getElementById('root')
);