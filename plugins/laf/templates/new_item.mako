<form method="post" class="lostAndFoundForm" action="${controller.route("new_%s" % form.mode)}">

<fieldset class="step what single-field">
                <span class="step-number">1</span>
                <div class="step-form">
                    <input type="text" name="group" value="Pet, phone, laptop..." />
                </div>
                <!--
                <div class="help">
                    <a href="" class="helpIcon">?</a>
                    <p>Curabitur dui neque, porta in imperdiet quis, scelerisque ac justo. Donec at nisl lacus. Nam ut convallis purus. </p>
                </div>-->
            </fieldset>
            
            
            <fieldset class="step where">
                <span class="step-number">2</span>
                <div class="step-form">
                    <h2>When &amp; where did you lose your object?</h2>
                
                    <input type="text" name="place" value="Put an address" />

                    <div class="map">
                        <img src="/images/map.jpg" alt="" />
                    </div>
                    
                    <div class="date">
                        <p>Date</p>
                        <input type="text" name="when_start" />
                        <input type="text" name="when_end" />
                    </div>
                </div>
                
            </fieldset>
            
            <fieldset class="step single-field">
                <span class="step-number">3</span>
                <div class="step-form">
                        <input type="file" name="" class="file" />
                </div>
            </fieldset>
            
            <fieldset class="step characteristics">
                <span class="step-number">4</span>
                <div class="step-form">
                    <h2>Create a set of questions that are gonna be used to identify the owner.</h2>
                
                    <div class="char-set">
                        <div class="widget textfield error textarea">
                            <label for="">Question</label>
                            <input type="text" name="" value="Example of a question: What is the color of the laptop?" />
                        </div>
                        <div class="widget textfield error textarea">
                            <label for="">Answer</label>
                            <input type="text" name="" value="Example of an answer: Blue" />
                        </div>
                    </div>
                    <div class="char-set">
                        <div class="widget textfield error textarea">
                            <label for="">Question</label>
                            <input type="text" name="" value="" />
                        </div>
                        <div class="widget textfield error textarea">
                            <label for="">Answer</label>
                            <input type="text" name="" value="" />
                        </div>
                    </div>
                </div>
            </fieldset>
            
            <input type="hidden" name="" value="${form.mode}" />

</form>
