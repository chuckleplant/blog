---
layout: post
title: Isaac Hayes Wallpaper Generator - Volumetric light scattering, 2 of 2
date: 2017-12-04
icon: sun-o
comments: true
disqus_identifier: Shaft!
image:
    path: "images/red-dead-shaft.png"
---

> Continuation of [Isaac Hayes Wallpaper Generator - Volumetric light scattering, 1 of 2]({% post_url 2017-05-28-light-shafts %})
>
> You can go straight to the [Wallpaper Generator](/emscripten/isaac_hayes_wg/IsaacWallpaper.html) tool (works best with chrome last I tested)

Now that covered the basics of light rendering and volumetric light scattering, let's see how we don't do any of that and instead cheat to get an approximated result.

A bit like in impressionism, we don't try to match physical light behaviour objectively, but to emulate what we see in an efficient way. That's computer graphics in a nutshell.

## Formulae summary

Rendring equation:

$${L_{\text{o}}(\mathbf x,\, \omega_{\text{o}})} {\,=\,} {L_e(\mathbf x,\, \omega_{\text{o}})}  {\ +\,}  {\int_\Omega}  {f_r(\mathbf x,\, \omega_{\text{i}},\, \omega_{\text{o}})\,}  {L_{\text{i}}(\mathbf x,\, \omega_{\text{i}})\,}  {(\omega_{\text{i}}\,\cdot\,\mathbf n)\,}  {\operatorname d \omega_{\text{i}}}$$

Light intensity and extinction constant:

$$I=I_\text{o} · e^{-\tau s}$$

Light scattering equation:

$${L(s,\,\theta)}  {\,=\,}  {L_\text{o}}  {e^{-\tau s}}  {\,+\,} \frac{1}{\tau}  {\,E_{sun}}  {\,S(\theta)}  {(1 \,-\, }  {e^{-\tau s}} {)}$$

Occlusion:

$$L(s,\,\theta,\,\phi) = (1 \,-\, D(\phi)) \,L(s,\,\theta)$$

## Accounting for occlusion

We need to account for all objects occluding each beam of light. For this rendering solution we use only screen space information, so we don't have any 3D information and cannot compute for each ray whether it was occluded or not. Also keep in mind, that each pixel on screen represents us, the viewer.

Eq. 3 computes, for a whole ray, the accumulated light value based on the media it traverses. What we'll do is march on screen space, accumulating by sampling along the ray's path towards any given pixel.

{% include image.html file="cheating-shaft.png" description="Each dot represents a sample, we omit the samples that have an occluder. This makes the pixels with no ocluders (on screen space) be brighter." %}

## The sum

We want to compute the light at a given _fragment_ (each small square in the image above), we will sum the energy values sampled along the ray from the light source towards our pixel. We will:

$$L(p) = \sum_{i=0}^n decay^i \times weight \times \frac{L(s,\theta)}{n}$$

The $$decay$$ term is a falloff, that attenuates the energy based on the distance to the light source. The $$weight$$ is the shaft's intensity[^1].

The further the pixel is from the light source, the dimmer light accumulation is. 


{% include image.html file="red-dead-blackness.png" description="In our first render pass we render just the scene in black and the light source. Note that we paint the sun red in this case so that the light shifts from white at maximum intensity to a dim red (What I like to call dead red)." %}

{% include image.html file="red-dead-scene.png" description="Our second render pass draws the scene as we want it, in this case just a silhouette with the sun behind it. Note that we draw the sun as a white circle too without the shafts." %}

{% include image.html file="red-dead-shaft.png" description="Last we run a final pass that samples for each fragment the brightness energy in the direction of the light source. This results in the shafts of light passing through the occluders." %}


# Application in games

It is based on physical effects, but is not by any means physically realistic. The effect is only valid when the light in screen space. The effect disappears completely when the light is either out of view or completely occluded.

But, should games aim for physical realism? I don't think so. As a means to transmitting emotions to the player, game developers should use any possible trick to do so, visual illusions such as this rather simplistic radial blur are very effective.

# Isaac Hayes Wallpaper Generator


<video autoplay="autoplay" loop="loop" width="100%">
    <source src="/videos/rdrgif.mp4" type="video/mp4">
</video>

Whithout further ado I present the [Isaac Hayes Wallpaper Generator](/emscripten/isaac_hayes_wg/IsaacWallpaper.html)[^2]. You can tweak light intensity, background color. You can also upload your own image (with transparency) to play with it and pierce your own eyes with the power of the sun, or not, your call.[^3]$$^,$$[^4]

It was also an experiment using Emscripten to port C++ code to JavaScript, the toughest was loading files from disk and saving them back. Apparently browsers are not cool with you merrily accessing the file system!

Find all the relevant in the github [repository](https://github.com/chuckleplant/IsaacHayesWG). 

-------------

[^1]: Note that we've dropped the exposure term use in Nvidia's formulation, it just provides more granularity on the $$weight$$ term.
[^2]: [Recommended soundtrack](https://www.youtube.com/watch?v=nFvRvSxsW-I)
[^3]: [Coded using openFrameworks.](https://github.com/openframeworks/openFrameworks)
[^4]: [Based on Julien Moreau-Mathis: God Rays? What’s that?](https://medium.com/community-play-3d/god-rays-whats-that-5a67f26aeac2)
