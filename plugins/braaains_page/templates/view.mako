<h1>${page.version.title}</h1>
<a href="${controller.route("braaains_project", "view", dict(id=page.project.id))}">Back to Project</a>
<a href="${controller.route("edit", dict(id=page.id))}">Edit</a>
% if page.version.format == "html":
    ${page.version.body |n}
% else:
    <pre>
${page.version.body}
    </pre>
% endif
