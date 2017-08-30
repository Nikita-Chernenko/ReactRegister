import React, {Component} from 'react'

export default class AbsenceList extends Component {
    loadBooksFromServer() {
        let auth_token = localStorage.getItem("auth_token")
        let headers = new Headers();
        headers.append('Authorization', 'Token '+ auth_token);
        fetch("/api/v0/absences",{headers:headers}).
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
            var absences = this.state.class_times.map(function (mark, index) {
                return <li key={index}>{mark.fields.value}
                </li>
            })
        }
        return (
            <div>
                <p>Absences</p>
                {absences}
            </div>
        )
    }
};