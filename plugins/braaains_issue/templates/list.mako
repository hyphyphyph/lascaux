<h1>Issues for ${project.title}</h1>
<a href="${controller.route("new", dict(project_id=project.id))}">Create Issue</a>
% if not issues:
    <div>
        <p>You're in the clear, man.  You've done got yourself no issues.</p>
    </div>
% else:
    <ul>
        % for issue in issues:
            <li>
                <a href="${controller.route("view", dict(id=issue.id))}">
                    ${issue.title}
                </a>
                (${issue.type.title})
            </li>
        % endfor
    </ul>
% endif
