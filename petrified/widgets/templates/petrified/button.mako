<%
    id_ = id and ' id="%s"' % id or ""
    classes_ = classes and ' class="%s"' % classes or ""
    disabled_ = disabled and ' disabled="disabled"' or ""
    options_ = id_+classes_+disabled_
%>
<div class="widget button">
    <input type="submit" name="${name}"${options_}${title and ' value="%s"' % title or ""} />
    % if description:
        <div class="description">
            ${description}
        </div>
    % endif
</div>
