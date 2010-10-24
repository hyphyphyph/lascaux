<h1>Thanks, ${item.kind == "found" and "Finder" or "Loser"}</h1>
<p>We've put your ${item.group.name} into our infinite, dark and dusty bin of lost and found relics.</p>
% if item.kind == "found":
    <p>We'll let you know if anyone tries to claim the item.</p>
% else:
    <p>We'll let you know if anyone posts something that looks like it might be what you've lost.</p>
% endif
