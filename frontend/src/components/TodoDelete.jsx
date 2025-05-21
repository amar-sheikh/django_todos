import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'

const TodoDelete = () => {
	const [taskName, setTaskName] = useState('')
	const [error, setError] = useState('')
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
				const data = await response.json()
				setTaskName(data.task_name)
			}
			catch {
				setError('Error fetching data')
			}
		}

		getTodo()
	}, [params])

	const handleClick = async (e) => {
		const response = await await fetch(`http://127.0.0.1:8000/api/v1/todos/${params.id}/`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
			}
		})
		if (response.status === 204) {
			navigate('/todos')
		}
		else {
			setError('Error deleting todo item')
		}
	}

	return (
		<div>
			{
				error ? (
					<>
						<div className='error'>{error}</div>
						<Link to='/'>Go to Back</Link>
					</>
				) : (
					<>
						<h1>Delete Todo</h1>
						<div>Are you sure you want to delete task '{taskName}'?</div>
						<button onClick={handleClick} >Delete</button>
						<hr />
						<Link to='/todos'>Cancel</Link>
					</>
				)
			}
		</div>
	)
}

export default TodoDelete