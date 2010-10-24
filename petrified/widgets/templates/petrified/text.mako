<%
    if title and not id:
        id_ = id and ' id="%s"' % name or ""
    else:
        id_ = id and ' id="%s"' % id or ""
    classes_ = classes and ' class="%s"' % classes or ""
    rows_ = rows and ' rows="%s"' % rows or ""
    cols_ = cols and ' cols="%s"' % cols or ""
    readonly_ = readonly and ' readonly="readonly"' or ""
    disabled_ = disabled and ' disabled="disabled"' or ""
    options_ = id_+classes_+rows_+cols_+disabled_+readonly_
%>
<div class="${rows and "textarea" or "textfield"}${error and " error" or ""}">
    % if error:
        <div class="error_message">
            ${error_message}
        </div>
    % endif
    % if title:
        <label for="${id or name}">${title}</label>
    % endif
    % if not rows:
        <input type="text" name="${name}"${options_}${value and ' value="%s"'%value or ""} />
    % else:
        <textarea name="${name}"${options_}>${value or ""|n}</textarea>
    % endif
    % if description:
        <div class="description">
            ${description}
        </div>
    % endif
</div>  
