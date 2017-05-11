---
layout: post
title: Visual Studio Code and openFrameworks
date: 2017-01-29
icon: indent
---

All the cool kids are using these flashy [electron](https://electron.atom.io/) based editors. And here I was using Visual Studio on Windows and XCode on Mac. Constantly changing environments is a huge pain. So I decided to go full cross-platform.

Don't get me wrong, those are great and I'll still use them for big projects, work mostly. But when I want to [openFrameworks](http://openframeworks.cc/) and chill, I want something that feels light and snappy (though, electron framework will hog your RAM like the chromey it is) . Something cross-platform and reliable.

I looked at the popular options, because they're more likely to be maintained and supported. Contenders were: Sublime, Atom and VSC. Sublime's not free, and between Atom and VSC seems like VSC is performing a bit better. Plus, I'm used to Visual Studio so the familiarity helped here.

> V: Hey!  
> S: Now what?   
> V: Aren't you forgetting something?  
> S: (Sigh) ...Ok, Vim, you're the best.  
> V: Damn straight!    

Actually you all should learn Vim. The thing is, Vim does not have to be used from the terminal (yes, you'll still be a hacker, don't worry). You can use Vim's workflow in most editors nowadays. 

# How to do this

## VSC c++ properties

Create `c_cpp_properties.json` file which has the include paths. 

You can do this by Command Palette > C/CPP: Edit Configurations

Python script will:
* Add of include paths to the c_cpp_properties file
* create/modify the appropriate task.json file
** See http://code.visualstudio.com/docs/editor/tasks



## xcode commands

list targets

    xcodebuild -list -project $project

build scheme

    xcodebuild -scheme $project build





# Actually..

I'm creating all these scripts for python and that's cool and all...But the oF community already has this great tool that generates projects with addons and the like, the projectGenerator. Why not extend it by adding vscode app capabilities?

We just need to inherit from the `baseProject` class, and implement everythin in there for the vscode JSON structures. It's kind of tricky because we still want xcode and visual studio projects to exist, so that the launch commands just pipe to the projects below. VSC is just a façade that will enable programmers to use a single cross-platform editor. Underneath there's all the horse-power XCode and Visual Studio can gather.


## Tasks

* First of all implement a basic VSC project class that uses JSON, maybe we can use the ofxJSON addon.. or directly the libraries. XML is part of the core OF, JSON should also be accessible.
* Test the command line projectGenerator and see what it can do, for vscode we've seen it's actually not that complex. We only need to add the include directories and probably PG already sends all the necessary oF files.
* Voila!