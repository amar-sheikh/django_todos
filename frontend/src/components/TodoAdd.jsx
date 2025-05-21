import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import TodoForm from './TodoForm'

const TodoAdd = () => {
	const [todo, setTodo] = useState({
		task_name: '',
		task_description: '',
		is_completed: false
	})
	const [errors, setErrors] = useState({
		task_name: '',
		task_description: '',
		is_completed: false
	})
	const navigate = useNavigate()

	const handleSubmit = async (e) => {
		e.preventDefault();

		const response = await fetch('http://127.0.0.1:8000/api/v1/todos/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(todo)
		})

		if (response.status === 201) {
			navigate('/todos')
		}
		else {
			const data = await response.json()

			Object.entries(data).forEach(([item, item_errors]) => {
				setErrors(prevErrors => ({
					...prevErrors,
					[item]: item_errors.join(', ')
				}));
			});
		}
	}

	return (
		<div>
			<h1>Add Todo</h1>
			<TodoForm
				handleSubmit={handleSubmit}
				todo={todo}
				setTodo={setTodo}
				errors={errors}
				submitButtonText='Create' />
			<hr />
			<Link to='/todos'>Cancel</Link>
		</div>
	)
}

export default TodoAdd