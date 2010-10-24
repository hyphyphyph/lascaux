<form method="post" class="lostAndFoundForm" action="${controller.route("new_%s" % form.mode)}">
    <fieldset class="step what single-field">
        <span class="step-number">1</span>
        <div class="step-form">
            <input type="text" name="group" value="Pet, phone, laptop..." />
        </div>
    </fieldset>
    <fieldset class="step where">
        <span class="step-number">2</span>
        <div class="step-form">
            <h2>When &amp; where did you lose your object?</h2>
            <input type="text" name="place" value="Put an address" />
            <div class="map"><img src="/images/map.jpg" alt="" /></div>
            <div class="date">
                <p>Date</p>
                <input type="text" name="when_start" />
                <input type="text" name="when_end" />
            </div>
        </div>
    </fieldset>
    <fieldset class="step characteristics">
        <span class="step-number">4</span>
        <input type="hidden" name="characteristics_highest_index" value="0" />
        <div class="step-form">
            <h2>Tell me about the thing you've found.  What makes it amazing and special?</h2>
            <div class="char-set">
                <div class="widget textfield">
                    <label for="char_attr_0">Question</label>
                    <input type="text" id="char_attr_0" name="char_attr_0" value="What is the color of the laptop?" />
                </div>
                <div class="widget textfield">
                    <label for="char_val_0">Answer</label>
                    <input type="text" id="char_val_0" name="char_val_0" value="Black, blue, red, pink and white.  And Magenta." />
                </div>
            </div>
        </div>
    </fieldset>
    <fieldset>
        <div class="widget button">
            % if form.mode == "found":
                <input type="submit" value="Found It!" />
            % else:
                <input type="submit" value="Lost It!" />
            % endif
        </div>
    </fieldset>
</form>
