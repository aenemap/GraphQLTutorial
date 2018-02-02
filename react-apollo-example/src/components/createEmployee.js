import React, { Component } from 'react'
import { graphql } from 'react-apollo'
import gql from 'graphql-tag'

import { FEED_QUERY } from './EmployeeList'

class CreateEmployee extends Component {

  constructor(props){
    super(props)
    this.state = {
      name: '',
      hiredOn: '',
      departmentId: ''
    }
  }

  create_employee = async () => {
    const {name, hiredOn, departmentId } = this.state
    const depId = parseInt(departmentId, 10)
    console.log(name, hiredOn, depId)

    await this.props.postMutation({
      variables: {
        name,
        hiredOn,
        departmentId: depId
      },
      update: (store, {data: { createEmployee }}) => {
        const data = store.readQuery({
          query: FEED_QUERY
        })

        data.employees.push(createEmployee)

        store.writeQuery({query: FEED_QUERY, data})
      }
    })

    this.props.history.push(`/`)
  }

  render(){

    return(
      <div>
        <div className='flex flex-column mt3'>
          <input
            className='mb2'
            value={this.state.name}
            onChange={e => this.setState({name:e.target.value})}
            type='text'
            placeholder='Name'
          />
          <input
            className='mb2'
            value={this.state.hiredOn}
            onChange={e => this.setState({hiredOn:e.target.value})}
            type='text'
            placeholder='hired On'
          />
          <input
            className='mb2'
            value={this.state.departmentId}
            onChange={e => this.setState({departmentId:e.target.value})}
            type='numeric'
            placeholder='departmentId'
          />

          <button onClick={() => this.create_employee()}>Submit</button>

        </div>
      </div>
    )
  }
}


const POST_MUTATION = gql`
  mutation PostMutation($name: String, $hiredOn: String, $departmentId:Int){
    createEmployee(name: $name, hiredOn: $hiredOn, departmentid: $departmentId){
      id
      name
      hiredOn
      departmentid
    }
  }
`


export default graphql(POST_MUTATION, {name: 'postMutation'})(CreateEmployee)
