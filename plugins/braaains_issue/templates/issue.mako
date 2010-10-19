<a href="${controller.route("list", dict(project_id=issue.project.id))}">Back to Issues</a>
<h1>Issue: ${issue.id}</h1>
<h2>${issue.title}</h2>

<div class="issue-body">
    ${issue.body}
</div>

<div class="issue-comments">
    <h2>Comments</h2>
    ${comments}
</div>
