<%
    if title and not id:
        id_ = id and ' id="%s"' % name or ""
    else:
        id_ = id and ' id="%s"' % id or ""
    classes_ = classes and ' class="%s"' % classes or ""
    disabled_ = disabled and ' disabled="disabled"' or ""
    options_ = id_+classes_+disabled_
%>
<div class="widget select${error and " error" or ""}">
    % if error:
        <div class="error_message">
            ${error_message}
        </div>
    % endif
    % if title:
        <label for="${id or name}">${title}</label>
    % endif
    <select name="${name}"${options_}>
        % for option in options:
            % if option[0] == value:
                <option value="${option[0]}" selected="selected">${option[1]}</option>
            % else:
                <option value="${option[0]}">${option[1]}</option>
            % endif
        % endfor
    </select>
    % if description:
        <div class="description">
            ${description}
        </div>
    % endif
</div>  
