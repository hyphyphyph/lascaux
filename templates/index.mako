<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Maxfindit</title>
    	<meta charset="UTF-8" />
        <link rel="stylesheet" type="text/css" href="/css/style.css" />
        <link rel="stylesheet" type="text/css" href="/css/smoothness/jquery-ui-1.8.5.custom.css" />
        <link rel="icon" type="image/x-icon" href="favicon.ico">
        <script type="text/javascript" src="/js/jquery-1.4.3.min.js"></script>
        <script type="text/javascript" src="/js/jquery-ui-1.8.5.custom.min.js"></script>
        <script type="text/javascript" src="/js/library.js"></script>
        <script type="text/javascript" src="/js/javascript.js"></script>
        ${head_style}
        ${head_script}
        <!--[if IE]>
    	    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    	<![endif]-->
    </head>
    <body>
        <div id="wrapper">
            <div id="header"></div>
            <div id="body">
                <div class="container">
                    <div class="selectType">
                        <span>You are a...</span>
                        <ul>
                            <li class="active"><a href="" class="loser-form">Loser</a></li>
                            <li><a href="" class="finder-form">Finder</a></li>
                        </ul>
                    </div>
                    ${content}
                </div>
            </div>
            <div id="footer">
                <div class="container">
                    <p class="copyright">&copy; Copyright 2010</p>
                </div>
            </div>
        </div>
    </body>
</html>
