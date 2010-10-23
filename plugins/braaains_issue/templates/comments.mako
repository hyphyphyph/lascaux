<ul>
    % for comment in comments:
        <li>
            <h3>
                ${comment.title}
                <span class="comment-user">
                    <a href="${controller.route("user", "view", dict(uuid=comment.user.uuid))}">
                        (${comment.user.username})
                    </a>
                </span>
            </h3>
            <div class="comment-body">
                ${comment.body}
            </div>
        </li>
    % endfor
</ul>

<h2>Post a comment</h2>
${comment_form}
