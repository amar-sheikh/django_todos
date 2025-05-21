import { useEffect, useState } from 'react'
import { useNavigate, Link, useParams } from 'react-router-dom'
import TodoForm from './TodoForm'

const TodoEdit = () => {
	const [todo, setTodo] = useState({
		id: '',
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
	const params = useParams()

	useEffect(() => {
		const getTodo = async () => {
			try {
				const response = await fetch(`http://127.0.0.1:8000/api/v1/todos/${params.id}`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
					},
				})

				setTodo(await response.json())
			}
			catch {
				setError('Error fetching data')
			}
		}

		getTodo()
	}, [params])

	const handleSubmit = async (e) => {
		e.preventDefault();

		const response = await fetch(`http://127.0.0.1:8000/api/v1/todos/${params.id}/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(todo)
		})

		if (response.status === 200) {
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
			<h1>Update Todo</h1>
			<TodoForm
				handleSubmit={handleSubmit}
				todo={todo}
				setTodo={setTodo}
				errors={errors}
				submitButtonText='Update' />
			<hr />
			<Link to='/todos'>Cancel</Link>
		</div>
	)
}

export default TodoEdit