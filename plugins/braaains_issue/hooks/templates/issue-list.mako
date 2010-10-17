<h2>Issues</h2>
<a href="${controller.route("braaains_issue", "new", dict(project_id=project.id))}">New</a>
<ul>
    % for issue in issues:
        <li>
            <a href="${controller.route("braaains_issue", "view", dict(id=issue.id))}">${issue.title}</a>
            (${issue.type.title})
        </li>
    % endfor
</ul>
