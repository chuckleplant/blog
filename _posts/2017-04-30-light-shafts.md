---
layout: post
title: Rendering equation, blue skies and cool wallpapers
date: 2017-04-30
icon: sun-o
comments: true
disqus_identifier: McShafty
---

Often there's one rendering effect that has me in awe everytime I see it. The first one I remember was normal mapping. While playing videogames I used to walk towards a wall that had a light bulb nearby, and then I spent a good 10 minutes just moving near the wall, seeing how the light behaved. 

Lately I found myself doing the same thing while playing The Witcher 3, I just forwarded time until the sun was low enough so I could just toy with the light shaft effects between the trees. And then again, I spend a shameful amount of time just walking back and forth seeing how these patterns would unfold. 

For the sake of me actually playing videogames instead of just being mesmerized by technical feats, I decided to understand how light shafts are generated and what's the theory behind it.

# Rendering equation review

$$

\definecolor{steadyblue}{RGB}{0,76,212} %004CD4
\definecolor{lobster}{RGB}{185,138,162} %B98AA2
\definecolor{mars}{RGB}{255,165,44} %FFA52C
\definecolor{rosamund}{RGB}{198,73,255} %C649FF
\definecolor{gold}{RGB}{255,206,63} %FFCE3F
\definecolor{bleu}{RGB}{73,214,255} %49D6FF
\definecolor{pistacho}{RGB}{118,163,39} %76A327

\color{steadyblue}{L_{\text{o}}(\mathbf x,\, \omega_{\text{o}})} \color{black}{\,=\,} \color{mars}{L_e(\mathbf x,\, \omega_{\text{o}})} \color{black}{\ +\,} \color{bleu}{\int_\Omega} \color{gold}{f_r(\mathbf x,\, \omega_{\text{i}},\, \omega_{\text{o}})\,} \color{rosamund}{L_{\text{i}}(\mathbf x,\, \omega_{\text{i}})\,} \color{pistacho}{(\omega_{\text{i}}\,\cdot\,\mathbf n)\,} \color{bleu}{\operatorname d \omega_{\text{i}}}$$

To find <font color="#004CD4">the light towards the viewer from a specific point</font>, we sum the <font color="#FFA52C">light emitted from such point</font> plus <font color="#49D6FF">the integral within the unit hemisphere</font> of <font color="#C649FF">the light coming from a any given direction</font> multiplied by the <font color="#FFCE3F">chances of such light rays bouncing towards the viewer</font> and also by <font color="#76A327">the irradiance factor over the normal at the point</font>.[^1]$$^,$$[^2]

Note how <font color="C649FF">incoming light</font> is also computed by that very formula, which makes this exhaustingly recursive.


DRAWING HERE, OR ABOVE, HAND DRAWN BUT WITH SOME SENSE OF STYLE, SERGIO PLS

# Volumetric light scattering equations

Light, as the electromagnetic radiation it is, interacts with matter mainly in two ways:

* Absorption (The photons disappear)
* Scattering (The photons change their direction)

In both cases the **transmitted intensity** decreases exponentially. Being $$\tau$$ the extinction constant composed of light absortion and out-scattering, and $$s$$ the thickness of the medium we traverse. And, as all things that grow or shrink[^3], we beautifully represent it as:

$$I=I_0 · e^{-\tau s}$$

This helps us understand how scattering is first modelled in Nvidia's GPU gem on volumetric light scattering[^4].

* Rayleigh and Mie, the wavelength (frequency) of the scattered light is the same as the incident light. 

# The GLSL approach

# Application in games

This technique is quite easy to implement, and to the uneducated viewer it will be an amusing effect. This is why many games have overused it, and still do. It is based on physical effects, but is not by any means physically realistic. The effect is only valid when the light is very distant, and in screen space. The effect disappears completely when the light is either out of view or completely occluded.

But, should games aim for physical realism? I don't think so. As a means to transmitting emotions to the player, game developers should use any possible trick to do so, visual illusions such as this rather simplistic radial blur are very effective.

# Sample application - Wallpaper generator

Physically unrealistic, only good for distant lights that are in screen space. 

# References



[^1]: [Rendering equation](https://en.wikipedia.org/wiki/Rendering_equation)
[^2]: [Colorful equations with MathJax](http://adereth.github.io/blog/2013/11/29/colorful-equations/)
[^3]: [Why number $$e$$ is so sexy](https://www.youtube.com/watch?v=AuA2EAgAegE)
[^4]: [Light Scattering Demystified - Theory and Practice, Lars Øgendal](http://www.nbi.dk/~ogendal/personal/lho/lightscattering_theory_and_practice.pdf)