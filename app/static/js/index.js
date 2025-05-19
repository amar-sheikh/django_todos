$(function () {
    const submitData = async () => {
        let search = $('#search').val()
        let status = $('#status').val()

        let response = await fetch(`/?format=json&search=${search}&status=${status}`, {
            method: "GET",
        })

        todos = await response.json()

        $('#count').text(todos.length)
        $('#todo-list').empty()

        if (todos.length) {
            $("#no-item-text").hide()

            html = `
            <thead>
                <th class="item-space">#</th>
                <th class="item-space">Name</th>
                <th class="item-space">Description</th>
                <th class="item-space">Status</th>
                <th class="item-space">Actions<th>
            </thead>
            <tbody>`

            todos.forEach(todo => {
                html += `
                    <tr>
                        <td class="item-space">${todo.id}</td>
                        <td class="item-space">${todo.task_name}</td>
                        <td class="item-space">${todo.task_description}</td>
                        <td class="item-space">${todo.is_completed ? 'Completed' : 'Not completed'}</td>
                    </tr>
                    `
            });

            html += `</tbody>`

            $('#todo-list').append(html)
        }
        else {
            $("#no-item-text").show()
        }
    }

    submitData()

    $('#search').on('input', () => { submitData() })
    $('#status').on('change', () => { submitData() })
})