<%
    properties_ = []
    for key in properties:
        properties_.append('%s="%s"' % (key, properties[key]))
    properties_ = properties_ and " " + " ".join(properties_) or ""
%>
<form method="${method}" action="${action}"${properties_}>
    ${content}
</form>
