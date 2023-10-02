---
layout: post
title:  "Tapetum Lucidum"
date:   2023-10-02
tags: [unreal,unreal engine,UE5,GYLT,Stadia,VFX]
comments: true
disqus_identifier: TapetumLucidum
image: 
    path: "img/600/racheye.jpg"
excerpt: "Gylt was the first game I worked at. It was a spooky one, the art style inspired by Laika movies (Coraline, Kubo). Every now and then you could find these weird looking tentacles with huge eyes pulsating in the darkness. They were called The Observers."
---

[Gylt](https://store.steampowered.com/app/2206210/GYLT/) was the first game I worked at. It was a spooky one, the art style inspired by Laika movies (Coraline, Kubo). Every now and then you could find these weird looking tentacles with huge eyes pulsating in the darkness. They were called The Observers.

{% include image.html file="gylt-eye.png" description="Personal rendition of The Observers. These are docile beings that can block your path. They will also rudely stare." %}

One day, while playing the game, I walked into Bachman School. The game took place mostly at night time. There is something alrady terrifying about high schools at night. Right after you walk in through the main entrance, there is a hallway. You can barely see anything and once you're deep into the room you can start to see a group of Observers blocking your path.

At this point in the game I already had my flashlight with me. The flashlight was Sally's main weapon agains, well, darkness. And I had a little aha moment. **It would be great if I could already see moving eyes glowing in the darkness when I first walked by that gloomy corridor**. This simple and insignificant idea took me on a developer side-quest.

First I pestered my lead Raul, who brushed it off telling me that there were other priorities and that it wasn't our department. Fair enough. Later I asked Simon, who was the lead VFX for the project. He was on board but told me "I like the idea buddy, but this needs to be approved by the art director". Alright then, a few days later I found our art director Cesar and I gave him a little pitch. I even did some research and found that this eye glow is called [*Tapetum Lucidum*](https://en.wikipedia.org/wiki/Tapetum_lucidum).

{% include image.html file="racheye.jpg" description="Tapetum Lucidum is a layer of tissue in the eye that reflects visible light. They used a cool practical effect in Blade Runner to capture this without any CGI." %}

Cesar finally gave in and gave me a solid *maybe*. It certainly wasn't the first thing on his list. This was **outrageous**. How could we have huge eyes, a flashlight as the main weapon, and not have this!? I sat on it for a few days until it dawned on me that I could just go and do it myself.

It was a nice excuse to toy with materials. The logic behind it was quite simple, if the light source and the Observer's eyes aligned with the camera's forward vector, the eye then can reflect back light towards the camera and have a slight glow. Nothing a dot product and an emissive material cannot fix.

{% include image.html file="material-tapetum-mockup.png" description="You've probably seen reflective tape in those construction worker vests. The idea here is the same. If light source direction aligns with your eye, the tapetum will bounce the light back to you." %}

I showed it to Simon and he was into it. He was visibly amused by a newly hired gameplay programmer showing him a rudimentary visual effect. He even gave me some feedback and we iterated it for a while. I was working on this separate dark level when I found a few minutes to spare. He later kindly took the material and gave it some magic VFX touches and *voilà*, it was in the game.

{% include image.html file="tapetum-draft-1.png" description="Tapetum Lucidum effect just as it appears in the released game. It's very subtle." %}

It's still one of my favorite game dev moments. Something sparks your imagination and once an idea forms it's hard for you to let it go. *An idea is like a virus, resilient, highly contagious*. I really hope someone noticed while playing the game. I had a blast with this tiny feature.

Always hire a prototype to be the salesperson of your idea.