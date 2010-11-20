<%
    from lascaux.sys import config
%>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Lascaux Framework</title>
    	<meta charset="utf-8" />
        <link rel="icon" type="image/x-icon" href="favicon.ico">
        <link rel="stylesheet" type="text/css" href="/style.css" />
        <script type="text/javascript" src="/jquery-1.4.3.min.js"></script>
        <script type="text/javascript" src="/lascaux.js"></script>
        ${head_style}
        ${head_script}
    </head>
    <body>
        <div>
            ${content}
        </div>
        % if config['debug']:
            <div class="lascaux debug-panel">
                <div class="header">
                    <h2>Debug Info</h2>
                    <div class="actions">
                        <ul>
                            <li class="close"><a href="#" class="hide">hide</a><a href="#" class="show">show</a></li>
                        </ul>
                    </div>
                </div>
                <div class="body">
${debug}
                </div>
            </div>
        % endif
    </body>
</html>
