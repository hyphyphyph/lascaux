<!DOCTYPE html>

<html lang="en">
<head>
    <title></title>
	<meta charset="UTF-8" />
	<meta name="viewport" content="user-scalable=no" />
    <link rel="stylesheet" type="text/css" href="css/style.css" />
    <link rel="icon" type="image/x-icon" href="favicon.ico">
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
        
        <form action="" class="lostAndFoundForm">
            
            <fieldset class="step what single-field">
                <span class="step-number">1</span>
                <div class="step-form">
                    <div class="widget textfield">
                        <label for="">I lost</label>
                        <input type="text" name="" value="Pet, phone, laptop..." />
                    </div>
                </div>
            </fieldset>
            
            
            <fieldset class="step where">
                <span class="step-number">2</span>
                <div class="step-form">
                    <h2>When &amp; where did you lose your object?</h2>
                
                    <div class="widget textfield">
                        <label for="">Search place</label>
                        <input type="text" name="" value="Put an address" id="searchLocation" />
                        <input type="hidden" name="" value="" id="locationLat" />
                        <input type="hidden" name="" value="" id="locationLng" />
                        <span class="errorLocating">!</span>
                    </div>
                    <div class="map" id="map">

                    </div>
                    
                    <div class="date">
                        <p>Date</p>
                        <div class="widget textfield">
                            <label for="">From</label>
                            <input type="text" name="" value="" />
                        </div>
                        <div class="widget textfield">
                            <label for="">To</label>
                            <input type="text" name="" value="" />
                        </div>
                    </div>
                </div>
                
            </fieldset>
            
            <fieldset class="step single-field">
                <span class="step-number">3</span>
                <div class="step-form">
                    <div class="widget textfield">
                        <label for="">Pictures?</label>
                        <input type="file" name="" class="file" />
                    </div>
                </div>
            </fieldset>
            
            <fieldset class="step characteristics">
                <span class="step-number">4</span>
                <div class="step-form">
                    <h2>Create a set of questions that are gonna be used to identify the owner.</h2>
                
                    <div class="char-set">
                        <div class="widget textfield">
                            <label for="char_attr_0">Question</label>
                            <input type="text" name="char_attr_0" value="Example of a question: What is the color of the laptop?" />
                        </div>
                        <div class="widget textfield">
                            <label for="char_val_0">Answer</label>
                            <input type="text" name="char_val_0" value="Example of an answer: Blue" />
                        </div>
                        <div class="actions"><a href="#" class="add">Add</a></div>
                    </div>

                    <input type="hidden" value="0" name="characteristics_highest_index" id="characteristics_highest_index" />
                </div>
            </fieldset>
            
            <input type="hidden" name="" value="loser" />
        </form>
        
    </div>
    </div>
    
    <div id="footer">
    <div class="container">
        <p class="copyright">&copy; Copyright 2010</p>
    </div>
    </div>
</div>

<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="jquery.js"></script>
<script type="text/javascript" src="library.js"></script>
<script type="text/javascript" src="javascript.js"></script>
</body>
</html>
