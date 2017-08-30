import React, {Component} from 'react'

export default class MarkList extends Component {
    loadBooksFromServer() {
        let auth_token = localStorage.getItem("auth_token")
        let headers = new Headers();
        headers.append('Authorization', 'Token '+ auth_token);
        fetch("/api/v0/marks",{headers:headers}).
            then(res => {console.log(res); return res.json()}).
            then(data =>{console.log(data); this.setState({marks: data})})
    }

    constructor(props) {
        super(props);
        this.state = {
            marks: []
        }
    }

    componentDidMount() {
        this.loadBooksFromServer()
    }

    render() {
        if (this.state.marks) {
            var marks = this.state.marks.map(function (mark, index) {
                return <li key={index}>{mark.value}
                </li>
            })
        }
        return (
            <div>
            {marks}
            <p>sdosodsdosodso</p>
            </div>
        )
    }
};