import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const TodoList = () => {
  const [todos, setTodos] = useState({
    count: 0,
    next: null,
    previous: null,
    results: []
  })
  const [filter, setFilter] = useState({
    search: '',
    status: 'completed'
  })
  const [error, setError] = useState('')

  useEffect(() => {
    const getTodos = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/v1/todos/?search=${filter.search}&status=${filter.status}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
        setTodos(await response.json());
      }
      catch {
        setError('Error fetching data')
      }
    }

    getTodos()
  }, [filter])

  const handlePagination = async (url) => {
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      setTodos(await response.json());
    }
    catch {
      setError('Error fetching data')
    }
  }

  return (
    <div>
      <h1>Todo List</h1>
      <Link to='/todos/add'>Add Todo</Link>
      <h3>Filter results</h3>
      <div className='form-field-group'>
        <label htmlFor='search'>Search</label>
        <input
          name='search'
          value={filter.search}
          onChange={(e) => setFilter({...filter, search: e.target.value})}
          placeholder='Search by task name' />
      </div>
      <div className='form-field-group'>
        <label htmlFor='status'>Status</label>
        <select
          name='status'
          defaultValue='completed'
          onChange={(e) => setFilter({...filter, status: e.target.value})}
          >
            <option value='all'>All</option>
            <option value='completed'>Completed</option>
            <option value='not-completed'>Not completed</option>
        </select>
      </div>
      <hr />
      <hr />
      <div>Number of Todos found: {todos.count}</div>
      <hr />
      <div className='error'>{error}</div>
      {
        todos ? (
          <table>
            <thead>
              <tr>
                <th className="item-space">#</th>
                <th className="item-space">Name</th>
                <th className="item-space">Description</th>
                <th className="item-space">Status</th>
                <th className="item-space">Actions</th>
              </tr>
            </thead>
            <tbody>
              {
                todos.results.map(todo => (
                  <tr key={todo.id}>
                    <td className="item-space">{todo.id}</td>
                    <td className="item-space">{todo.task_name}</td>
                    <td className="item-space">{todo.task_description}</td>
                    <td className="item-space">{todo.is_completed ? 'Complete' : 'Not complete'}</td>
                    <td className="item-space">
                      <Link to={`/todos/edit/${todo.id}`}>Edit</Link>
                      <span>|</span>
                      <Link to={`/todos/delete/${todo.id}`}>Delete</Link>
                    </td>
                  </tr>
                ))
              }
            </tbody>
            {
              todos.previous && <button onClick={() => handlePagination(todos.previous)}>Go to previous</button>
            }
            {
              todos.next && <button onClick={() => handlePagination(todos.next)}>Go to next</button>
            }
          </table>
        ) :
          (
            <p>No Todo found...</p>
          )
      }
    </div>
  )
}

export default TodoList