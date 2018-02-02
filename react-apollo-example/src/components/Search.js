import React, { Component } from 'react'
import { withApollo } from 'react-apollo'
import gql from 'graphql-tag'
import Employee from './Employee'

class Search extends Component {

  constructor(props){
    super(props)

    this.state = {
      employees: [],
      filter: ''
    }
  }

  executeSearch = async() => {

    const filter  = this.state.filter
    const result = await this.props.client.query({
      query: SEARCH_QUERY,
      variables: {filter}
    })

    const employees = result.data.search
    console.log(employees)
    this.setState({ employees })
  }

  render() {
    return (

      <div>
        <div>
          Search
          <input
            type='text'
            onChange={(e) => this.setState({filter: e.target.value})}
          />
          <button onClick={() => this.executeSearch()}>
            OK
          </button>
        </div>
        {this.state.employees.map((emp, index) => <Employee key={emp.id} employee={emp} />)}
      </div>

    )
  }

}

const SEARCH_QUERY = gql`
  query SearchQuery($filter:String){
    search(filter: $filter){
        id
        name
        hiredOn
        department{
          id
          name
        }
    }
  }
`

export default withApollo(Search)
