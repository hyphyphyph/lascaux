<ul>
    % for comment in comments:
        <li>
            <h1>${comment.title}</h1>
            <div class="comment-body">
                ${comment.body}
            </div>
        </li>
    % endfor
</ul>
