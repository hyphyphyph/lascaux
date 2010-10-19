<a href="${controller.route("braaains_project", "list")}">Back to Projects</a>
<h1>${project.title}</h1>
% if project.desc:
    <p class="project-desciption">${project.desc}</p>
% endif
<div class="blocks">
    % for block_name in blocks:
        <div class="block" id="block-${block_name}">
            ${blocks[block_name]}
        </div>
    % endfor
</div>
