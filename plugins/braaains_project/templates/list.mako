<h1>Projects</h1>
<a href="${controller.route("braaains_project", "new")}">New</a>
<ul>
    % for project in projects:
        <li>
            <a href="${controller.route("view", dict(id=project.id))}">${project.title}</a>
        </li>
    % endfor
</ul>
