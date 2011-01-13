%if not form.is_open():
<%
    final_attributes = list()
    for key in form.attributes:
        final_attributes.append('%s="%s"' % (key, form.attributes[key]))
    final_attributes = final_attributes and " " + " ".join(final_attributes) or ""
%>
<form method="${form.method}" action="${form.action}"${final_attributes}>
%endif
%if not only_header:
    %for widget in form.unrendered_widgets:
        ${widget}
    %endfor
</form>
%endif
