import React, {Component} from 'react'

export default  class ClassTimeList extends Component {
    loadBooksFromServer() {
 let auth_token = localStorage.getItem("auth_token")
        let headers = new Headers();
        headers.append('Authorization', 'Token '+ auth_token);
        fetch("/api/v0/classtimes",{headers:headers}).
            then(res => res.json()).
            then(data => this.setState({class_times: data}))
    }

    constructor(props) {
        super(props);
        this.state = {
            class_times: []
        }
    }

    componentDidMount() {
        this.loadBooksFromServer()
    }

    render() {
        if (this.state.class_times) {
            var times = this.state.class_times.map(function (mark, index) {
                return <li key={index}>{mark.fields.value}
                </li>
            })
        }
        return (
            <div>
                <p>Times</p>
                {times}
            </div>
        )
    }
};