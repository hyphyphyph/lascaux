<%
    if title and not id:
        id_ = id and ' id="%s"' % name or ""
    else:
        id_ = id and ' id="%s"' % id or ""
    classes_ = classes and ' class="%s"' % classes or ""
    size_ = size and ' size="%s"' % size or ""
    readonly_ = readonly and ' readonly="readonly"' or ""
    disabled_ = disabled and ' disabled="disabled"' or ""
    options_ = id_+classes_+size_+disabled_+readonly_
%>
<div class="widget password${error and " error" or ""}">
    % if error:
        <div class="error_message">
            ${error_message}
        </div>
    % endif
    % if title:
        <label for="${id or name}">${title}</label>
    % endif
    <input type="password" name="${name}"${options_}${value and ' value="%s"'%value or ""} />
    % if description:
        <div class="description">
            ${description}
        </div>
    % endif
</div>
