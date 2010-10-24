<div class="page_headline_message">
    <h1>Yeah?  Tell me about it...</h1>
    <p>No, seriously <em>tell me about it.</em></p>
</div>
${form_content}

% if len(results):
    <h2>We've found ${len(results)} matches.</h2>
    <p>When you think you might have found your <strong>${group.name}</strong>, send a message to the finders.</p>
    ## ${contact_form}
% endif
