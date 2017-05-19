---
layout: post
title: Isaac Hayes Wallpaper Generator - Volumetric light scattering, 2 of 2
date: 2017-04-30
icon: sun-o
comments: true
disqus_identifier: Shaft!
---

> Continuation of [Isaac Hayes Wallpaper Generator - Volumetric light scattering, 1 of 2]({% post_url 2017-04-30-light-shafts %})

Now that covered the basics of light rendering and volumetric light scattering, let's see how we don't do any of that and instead cheat to get an approximated result.

This is part of the beauty of computer graphics, a bit like impressionism as opposed to realism in paintings. We don't try to match physical light behaviour objectively, but to emulate what we see in an efficient way.

## Accounting for occlusion

Here's where we cheat. We need to account for all objects occluding each beam of light. For this rendering solution we use only screen space information, so we don't have any 3D information and cannot compute for each ray whether it was occluded or not. 

Note that while eq. 3 computes, for a whole ray, the accumulated light value based on the media it traverses. What we'll do is march on screen space, accumulating **manually** by sampling along the ray's path. 

{% include image.html file="cheating-shaft.png" description="Each dot represents a sample, we omit the samples that have an occluder. This makes the pixels with no ocluders (on screen space) be brighter." %}

# The GLSL approach



# Application in games

This technique is quite easy to implement, and to the uneducated viewer it will be an amusing effect. This is why many games have overused it, and still do. It is based on physical effects, but is not by any means physically realistic. The effect is only valid when the light is very distant, and in screen space. The effect disappears completely when the light is either out of view or completely occluded.

But, should games aim for physical realism? I don't think so. As a means to transmitting emotions to the player, game developers should use any possible trick to do so, visual illusions such as this rather simplistic radial blur are very effective.

# Sample application - Wallpaper generator

# References

