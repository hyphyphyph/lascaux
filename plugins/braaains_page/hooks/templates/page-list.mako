<h2>Pages</h2>
<a href="${controller.route("braaains_page", "new", dict(project_id=project.id))}">New Page</a>
<ul class="page-list">
    % for page in pages:
        <li>
            <a href="${controller.route("braaains_page", "view", dict(id=page.id))}">${page.version.title}</a>
        </li>
    % endfor
</ul>
