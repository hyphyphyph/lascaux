<h1>Workflow Set: ${set.title}</h1>
<a href="${controller.route("edit_set", dict(id=set.id))}">Edit</a>
<h2>States</h2>
<a href="${controller.route("new_state", dict(set_id=set.id))}">New State</a>
% if not states:
    <div>
        <p>There are no defined states for this workflow.</p>
    </div>
% else:
    <ul>
        % for state in states:
            <li>
                <a href="${controller.route("edit_state", dict(id=state.id))}">${state.title}</a>
            </li>
        % endfor
    </ul>
% endif
