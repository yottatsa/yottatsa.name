#About Salt
<time datetime="2016-12-15"/>

It so happened that I come to Lehi, UT for two days, and colleague of mine 
said that SaltStack HQ is located just half mile away from Mirantis office. 
Here I should said, that I used to manage pretty big OpenStack installation 
using Salt back in Yandex, and right now I'm back to using it in TCPCloud 
(which was acquired by Mirantis recently). So I decided to come to SaltStack 
HQ to have a conversation with core people to get the idea which is meant 
behind all the stuff.

![Photo from my hotel](utah.jpg)

So, Salt is a configuration management tool, which is written with large 
spectre of possibilities in mind. Basically, it's a core engine that glues big 
components together and allows components on different servers to communicate, 
and provides with usual things like host-specific data (grains), bunch of 
environment settings (pillars), commands which interacts with systems, and 
states which describe system desired state. Many of this components are 
replaceable and extendable, like you could collect data from your scripts, or
pull configuration from REST API, or generate states from Python.

Salt allows you to do nice things, like to use your pillars and grains and some 
of Jinja templating to create data-driven infrastructure definition, like 
install right version of Nginx from right repository depends on environment 
settings and OS family and version. Like DRY and make a little for loop and 
iterate over parameters.

<p class="lead">
The problems, however, starts if somebody has no limits and he's read only the
tutorial.
</p>

Basically, templating was meant by Salt authors only for what I've 
listed above. But many of users are trying to write actually a code on Jinja 
(just because its default rendering engine), even Jinja is most awful 
templating language to program on it. There are many ways in Salt how to 
avoid doing heavy templating, like all python stuff was bubbled up to the 
surface to make writing execution modules and states and everything else 
easier, at last, even Mako is more suitable for programming (also it's favourite 
template engine for Salt authors).

That imbalance by overusing one tools and underusing another makes a problem 
with real-world usage, where system behaviour should be predictable. And 
there where conception of testing for formulas is coming forth. When I started 
using Salt for managing large production environment, I was really scared 
about applying changes, because if you apply all formulas at once on all the 
fleet, you might lose all your stuff in a minute. It ends up with partial 
apply, or some manual checking, or even avoidance of making changes in order 
to keep the system stable. On other side, if all the formulas and variants 
(Jinja!) will be covered by tests, what about amount of this tests and 
development velocity? It took me long time to realise that the only two 
parameters matters: development velocity, and service level objectives, which
is bounding factor.

<p class="lead">
So the idea behind all of extendability of Salt is to make things simple and 
well understandable. Going out of the balance will make the system not 
complicated but confusing.
</p>

Salt authors does not want to limit users ability to make whatever they want 
to, and actually it's not working this way (just look on Ansible programming).
But I'd really want from Salt users to make reasonable complications, and 
don't go to extremes, rather looks for another possibilities to make things 
right and understandable. In sake of stability and velocity.

<p class="license cc-by-sa">
This work is licensed under a 
<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>
