---
layout: post
title: Isaac Hayes Wallpaper Generator - Volumetric light scattering, 2 of 2
date: 2017-05-03
icon: sun-o
comments: true
disqus_identifier: Shaft!
---

> Continuation of [Isaac Hayes Wallpaper Generator - Volumetric light scattering, 1 of 2]({% post_url 2017-04-30-light-shafts %})
> 
> If you're unfamiliar with computer graphics, I highly recommend you to watch [John Carmack's talk on lighting and rendering](https://youtu.be/IyUgHPs86XM).


{::comment}
## Formulae summary

Rendring equation:

$${L_{\text{o}}(\mathbf x,\, \omega_{\text{o}})} {\,=\,} {L_e(\mathbf x,\, \omega_{\text{o}})}  {\ +\,}  {\int_\Omega}  {f_r(\mathbf x,\, \omega_{\text{i}},\, \omega_{\text{o}})\,}  {L_{\text{i}}(\mathbf x,\, \omega_{\text{i}})\,}  {(\omega_{\text{i}}\,\cdot\,\mathbf n)\,}  {\operatorname d \omega_{\text{i}}}$$

Light intensity and extinction constant:

$$I=I_0 · e^{-\tau s}$$

Light scattering equation:

$${L(s,\theta)}  {=}  {L_0}  {e^{-\tau s}}  {+} \frac{1}{\tau}  {E_{sun}}  {S(\theta)}  {(1 - }  {e^{-\tau s}} {)}$$
{:/comment}

We covered theory, let's now jump into practice. 


Now that covered the basics of light rendering and volumetric light scattering, let's see how we don't do any of that and instead cheat to get an approximated result.

This is part of the beauty of computer graphics, a bit like impressionism as opposed to realism in paintings. We don't try to match physical light behaviour objectively, but to emulate what we see in an efficient way.

## Accounting for occlusion

Here's where we cheat. We need to account for all objects occluding each beam of light. For this rendering solution we use only screen space information, so we don't have any 3D information and cannot compute for each ray whether it was occluded or not. 

Note that while eq. 3 computes, for a whole ray, the accumulated light value based on the media it traverses. What we'll do is march on screen space, accumulating by sampling along the ray's path. 

{% include image.html file="cheating-shaft.png" description="Each dot represents a sample, we omit the samples that have an occluder. This makes the pixels with no ocluders (on screen space) be brighter." %}

## The sum

We want to compute the light at a given _fragment_, we will sum the energy values sampled along the ray from the light source towards our pixel. We will:

$$L(p) = \sum_{i=0}^n decay^i \times weight \times \frac{L(s,\theta)}{n}$$

The $$decay$$ term is a falloff, that attenuates the energy based on the distance to the light source. The $$weight$$ is the shaft's intensity[^1].

# The GLSL approach



# Application in games

This technique is quite easy to implement, and to the uneducated viewer it will be an amusing effect. This is why many games have overused it, and still do. It is based on physical effects, but is not by any means physically realistic. The effect is only valid when the light is very distant, and in screen space. The effect disappears completely when the light is either out of view or completely occluded.

But, should games aim for physical realism? I don't think so. As a means to transmitting emotions to the player, game developers should use any possible trick to do so, visual illusions such as this rather simplistic radial blur are very effective.

# Sample application - Wallpaper generator


[^1]: Note that we've dropped the exposure term use in Nvidia's formulation, it just provides more granularity on the $$weight$$ term.