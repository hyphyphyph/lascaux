<!DOCTYPE html>

<html lang="en">
<head>
    <title>Maxfindit</title>
	<meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="/css/style.css" />
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    ${head_style}
    ${head_script}
    <!--[if IE]>
	<script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
	<![endif]-->
</head>

<body>

<div id="wrapper">
    <div id="header">
    </div>
    
    <div id="body">
    <div class="container">
        
        <div class="selectType">
        <ul>
            <span>You are a...</span>
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

<script type="text/javascript" src="/js/jquery-1.4.2.min.js"></script>
<script type="text/javascript" src="/js/library.js"></script>
<script type="text/javascript" src="/js/javascript.js"></script>
</body>
</html>
