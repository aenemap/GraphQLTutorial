import React, { Component } from 'react'

export default class Employee extends Component{
  render(){
    return (
      <div>
        <div>
          {this.props.employee.id} {this.props.employee.name} {this.props.employee.hiredOn}
        </div>
      </div>
    )
  }
}
