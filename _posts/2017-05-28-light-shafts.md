---
layout: post
title: Isaac Hayes Wallpaper Generator - Volumetric light scattering, 1 of 2
date: 2017-05-28
icon: eye
comments: true
disqus_identifier: McShafty
image:
    path: "img/600/red-dead-shaft.png"
---

> This post is greatly based on the [Nvidia GPU Gem on volumetric light scattering](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch13.html). Here I walk you through the formulae and core concepts. I highly recommend reading that one instead, and come back only if you couldn't follow, or for fun.
> 
> If you're unfamiliar with computer graphics, I highly recommend you to watch [John Carmack's talk on lighting and rendering](https://youtu.be/IyUgHPs86XM).


{% include image.html file="red-dead-shaft.png" description="Light shafts sample image, generated with the *Isaac Hayes Wallpaper Generator* tool, available in the second part of this entry. The image is from Rockstar's Red Dead Redemption 2 concept art." %}

Often there's one rendering effect that has me in awe everytime I see it. The first one I remember was normal mapping. While playing videogames I used to walk towards a wall that had a light bulb nearby, and then I spent a good 10 minutes just moving near the wall, seeing how the light behaved. 

Lately I found myself doing the same thing while playing The Witcher 3, I just forwarded time until the sun was low enough so I could just toy with the light shaft effects between the trees. And then again, I spend a shameful amount of time just walking back and forth seeing how these patterns would unfold. 

For the sake of me actually playing videogames instead of just being mesmerized by technical feats, I decided to understand how light shafts are generated and what's the theory behind it.

My hope here is to give any reader a shallow but thorough overview of computer graphics rendering and physically based rendering effects. These two concepts are rather tangent, in the sense that computer graphics will not use the actual physical formulae, but hacky approximations.



## Rendering equation review

![renderineq]({{site.baseurl}}/images/rendering-equation-drawing.png)


$$
\definecolor{steadyblue}{RGB}{0,76,212} %004CD4
\definecolor{lobster}{RGB}{185,138,162} %B98AA2
\definecolor{mars}{RGB}{255,165,44} %FFA52C
\definecolor{rosamund}{RGB}{198,73,255} %C649FF
\definecolor{gold}{RGB}{255,206,63} %FFCE3F
\definecolor{bleu}{RGB}{73,214,255} %49D6FF
\definecolor{pistacho}{RGB}{118,163,39} %76A327
\definecolor{sea}{RGB}{41,153,124}  %29997C 
\definecolor{flower}{RGB}{255,85,149} %FF5595

\color{steadyblue}{L_{\text{o}}(\mathbf x,\, \omega_{\text{o}})} \color{black}{\,=\,} \color{mars}{L_e(\mathbf x,\, \omega_{\text{o}})} \color{black}{\ +\,} \color{bleu}{\int_\Omega} \color{flower}{f_r(\mathbf x,\, \omega_{\text{i}},\, \omega_{\text{o}})\,} \color{rosamund}{L_{\text{i}}(\mathbf x,\, \omega_{\text{i}})\,} \color{pistacho}{(\omega_{\text{i}}\,\cdot\,\mathbf n)\,} \color{bleu}{\operatorname d \omega_{\text{i}}}$$

To find <font color="#004CD4">the light towards the viewer from a specific point</font>, we sum the <font color="#FFA52C">light emitted from such point</font> plus <font color="#49D6FF">the integral within the unit hemisphere</font> of <font color="#C649FF">the light coming from a any given direction</font> multiplied by the <font color="#FF5595">chances of such light rays bouncing towards the viewer</font>[^100] and also by <font color="#76A327">the irradiance factor over the normal at the point</font>.[^1]$$^,$$[^2]

Note that <font color="C649FF">incoming light</font> is also computed by that very formula, which makes this exhaustingly recursive.

So, think about the pixel you're reading right now, your screen is probably emitting more light than it transmits from other sources, if you have a glossy screen, then you see your own reflection. Meaning that for every point in your screen, light is reflected along the surface normal (perpendicular to your screen) in a **specular** fashion. 

If you have a non-glossy screen, then the light bouncing from other light sources is more evenly distributed over the reflection hemisphere, hence not forming a clear image as a result, but a **diffuse** image instead.


## Volumetric light scattering equations

Light, as the electromagnetic radiation it is, interacts with matter mainly in two ways[^4]:

* Absorption (The photons disappear)
* Scattering (The photons change their direction)

In both cases the **transmitted intensity** $$I$$ decreases exponentially. Being $$\tau$$ the extinction coefficient composed of light absortion and out-scattering, and $$s$$ the thickness of the medium we traverse, we use an exponential function over $$e$$ to represent the extinction coefficient[^3]:

$$I=I_\text{o} · e^{-\tau s}$$

This helps us understand how scattering is first modelled in Nvidia's GPU gem on volumetric light scattering[^7]. Let $$s$$ be the distance through the media and $$\theta$$ the angle between the viewer and the light beam:

![scattering-terms]({{site.baseurl}}/images/rendering-scatter-terms.png)

$$
\definecolor{steadyblue}{RGB}{0,76,212} %004CD4
\definecolor{lobster}{RGB}{185,138,162} %B98AA2
\definecolor{mars}{RGB}{255,165,44} %FFA52C
\definecolor{rosamund}{RGB}{198,73,255} %C649FF
\definecolor{gold}{RGB}{255,206,63} %FFCE3F
\definecolor{bleu}{RGB}{73,214,255} %49D6FF
\definecolor{pistacho}{RGB}{118,163,39} %76A327
\definecolor{sea}{RGB}{41,153,124}  %29997C 
\definecolor{greenbean}{RGB}{76,153,0}  %4C9900 

\color{red}{L(s,\,\theta)} \color{black}{\,=\,} \color{steadyblue}{L_\text{o}} \color{rosamund}{\,e^{-\tau s}} \color{black}{\,+\,} \frac{1}{\tau} \color{orange}{\,E_{sun}} \color{greenbean}{\,S(\theta)} \color{black}{\,(1 \,-\, } \color{rosamund}{e^{-\tau s}}\color{black}{)}$$

The <font color="FF0000">light accounting for volumetric scattering</font> is a linear interpolation <font color="C649FF">weighed by the extinction constant</font>. Note how we interpolate between the <font color="004CD4">light computed at a given point</font> and the light due to scattering, which is a product of the <font color="FFAF00">source illumination</font> from the sun (or light source) and the <font color="4C9900">angular scattering term</font> according to Rayleigh and Mie properties.

Let's talk a bit about the <font color="4C9900">Rayleigh and Mie term</font>, it's a function of particle size, shape and composition of the medium we traverse. This component and the extinction coefficient model the atmosphere or space through which light scatters. 

In a nutshell, smaller particles scatter according to the Rayleigh model, and larger particles according to Mie. In this context we consider smaller particles the ones much smaller than the wavelength of incoming light. 

This means Rayleigh scattering bounces off smaller wavelengths, such as the blue spectrum. Mie on the other hand, is not dependent on wavelength, and it scatters the whole spectrum of light. Clouds are white because sunlight is white.

{% include image.html file="rayleigh-meow.png" description="Rayleigh and Mie scattering describes how light scatters off of molecules in a medium depending on the size of those molecules. Smaller molecules respond to Mie scattering more than Rayleigh and viceversa.[^44]" %}

## Occlusion

Last but not least, we need to take occluders into the equation. Let $$\phi$$ represent the ray from the light emitter towards the observed point:

$$L(s,\,\theta,\,\phi) = (1 \,-\, \color{orange}{D(\phi)}\color{black}{)} \color{red}{\,L(s,\,\theta)}$$

Is the light accounting for both <font color="FF0000">volumetric light scattering</font> and <font color="FFA600">the opacity term of all occluders</font>, which is the total opacity of the ocluders along the ray. 

This term accumulates objects' opacity. If there's a solid object between light source and observer all light energy will be zeroed, however we must account for indirect light as well as seen in eq. 1.

## Wrap up

This covers a shallow walk through the theory of visible light and atmospheric scattering. With the information above we should be able to compute the light _energy_ towards the viewer for any point in space, note that we left out things like light wavelength for simplicity. I hope you have enough to get started.

In the next entry I will demonstrate these concepts implementing volumetric shafts of light with GLSL, completely dismissing all we learnt here and just hacking our way to rendered images.


[Continue to part 2]({% post_url 2017-12-04-light-shafts-pt-2 %})


-------------


[^1]: [Rendering equation](https://en.wikipedia.org/wiki/Rendering_equation)
[^2]: [Colorful equations with MathJax](http://adereth.github.io/blog/2013/11/29/colorful-equations/)
[^3]: [Why number $$e$$?](https://www.youtube.com/watch?v=AuA2EAgAegE)
[^4]: [Light Scattering Demystified - Theory and Practice, Lars Øgendal](http://www.nbi.dk/~ogendal/personal/lho/lightscattering_theory_and_practice.pdf)
[^100]: [Bidirectional reflectance distribution function](https://en.wikipedia.org/wiki/Bidirectional_reflectance_distribution_function)
[^32]: [Rayleigh and Mie scattering](http://hyperphysics.phy-astr.gsu.edu/hbase/atmos/blusky.html)
[^7]: [Nvidia GPU Gems, Chapter 13. Volumetric Light Scattering as a Post-Process](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch13.html)
[^44]: Image based on [Hyperphysics scattering post](http://hyperphysics.phy-astr.gsu.edu/hbase/atmos/blusky.html) and derived from [Sharayanan's work](https://commons.wikimedia.org/wiki/File:Mie_scattering.svg). Under the [Creative Commons Attribution-Share Alike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en) licence.