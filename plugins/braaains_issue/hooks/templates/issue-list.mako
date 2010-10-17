<h2>Issues</h2>
<ul>
    % for issue in issues:
        <li>
            <a href="${controller.route("braaains_issue", "view", dict(id=issue.id))}">${issue.title}</a>
            (${issue.type.title})
        </li>
    % endfor
</ul>
