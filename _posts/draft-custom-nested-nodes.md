---
layout: post
title:  "Nested Anim Blueprint Nodes"
date:   2023-10-03
tags: [unreal,unreal engine,UE5,animation,animation programming]
comments: true
disqus_identifier: nestedABPNodes
image: 
    path: "images/post_banners/nested-anims.png"
---

Here I'll show you how to implement Anim Blueprint logic in code. Is that worth doing? Not usually. But it's a handy tool in case you want to hide some complexity under the hood and expose only a pretty node in the editor.

good guidelines to kick off
https://www.unrealengine.com/en-US/blog/creating-custom-animation-nodes 

Unreal's [Animation Node Technical Guide](https://docs.unrealengine.com/5.3/en-US/animation-node-technical-guide-in-unreal-engine/) is a good starting point. And that's where we'll start from. I assume you already have a working Anim Node. There is also a [simplified guide](https://www.unrealengine.com/en-US/blog/creating-custom-animation-nodes) for you to setup your anim nodes.

// Code for anim node

// Code for anim graph

Basically any ABP (Anim Blueprint) node that you can use in the editor can also be used from code. It's only a matter for you to connect the pins internally and initialize them. Once connected, the evaluation happens in sequence. Same as your custom node is just a link in a bigger chain in your ABP. Your node can hold multiple internal nodes that all get evaluated in sequence.

