<h1>Projects</h1>
<ul>
    % for project in projects:
        <li>
            <a href="${controller.route("view", dict(id=project.id))}">${project.title}</a>
        </li>
    % endfor
</ul>
