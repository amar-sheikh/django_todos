const TodoForm = ({ handleSubmit, todo, setTodo, errors, submitButtonText }) => {
	return (
		<form onSubmit={handleSubmit}>
			<div className='form-field-group'>
				<label htmlFor='task_name'>Task name</label>
				<input
					name='task_name'
					type='text'
					value={todo.task_name}
					onChange={(e) => setTodo({ ...todo, task_name: e.target.value })}
					placeholder='Enter task name...' />
				<div className='error'>{errors.task_name}</div>
			</div>
			<div className='form-field-group'>
				<label htmlFor='task_description'>Task descripton</label>
				<textarea
					name='task_description'
					value={todo.task_description}
					onChange={(e) => setTodo({ ...todo, task_description: e.target.value })}
					placeholder='Enter description...' />
				<div className='error'>{errors.task_description}</div>
			</div>
			<div className='form-field-group'>
				<label htmlFor='is_completed'>Task Completed</label>
				<input
					name='is_completed'
					type='checkbox'
					checked={todo.is_completed}
					onChange={(e) => setTodo({ ...todo, is_completed: e.target.checked })} />
				<div className='error'>{errors.is_completed}</div>
			</div>
			<button type='submit'>{submitButtonText ?? 'Save'}</button>
		</form>
	)
}

export default TodoForm