import React, { Component } from 'react'
import Header from './Header'
import EmployeeList from './EmployeeList'
import CreateEmployee from './createEmployee'
import Login from './Login'
import Search from './Search'
import { Switch, Route } from 'react-router-dom'


class App extends Component {
  render() {
    return (
      <div className='center w85'>
        <Header />
        <div className='ph3 pv1 background-gray'>
          <Switch>
            <Route exact path='/login' component={Login} />
            <Route exact path='/create' component={CreateEmployee} />
            <Route exact path='/' component={EmployeeList} />
            <Route exact path='/search' component={Search} />
          </Switch>

        </div>
      </div>
    )
  }
}

export default App
