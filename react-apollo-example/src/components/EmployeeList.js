import React, { Component } from 'react'
import Employee from './Employee'
import gql from 'graphql-tag'
import { graphql } from 'react-apollo'

class EmployeeList extends Component{

  render(){
    if (this.props.feedQuery && this.props.feedQuery.loading){
      return <div>Loading...</div>
    }

    if (this.props.feedQuery && this.props.feedQuery.error){
      return <div>Error</div>
    }

    const employeesToRender = this.props.feedQuery.employees
    return(
      <div>
        {employeesToRender.map(emp => <Employee key={emp.id} employee={emp}/>)}
      </div>
    )
  }
}

export const FEED_QUERY = gql`
  query FeedQuery {
      employees{
        id
        name
        hiredOn
      }
  }
`

export default graphql(FEED_QUERY, {name: 'feedQuery'}) (EmployeeList)
