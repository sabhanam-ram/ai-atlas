# Transcript: Building more effective AI agents

- Source: https://www.youtube.com/watch?v=uhJJgc-0iTQ
- Channel: Anthropic
- Video ID: uhJJgc-0iTQ
- Fetched: 2026-06-11
- Method: youtube-transcript-api

---

[00:00] - I think there's also a lot of interesting things
[00:01] to explore of multi-agent as a form of test time compute.
[00:05] - Basically letting Claude,
[00:08] many Claudes work on a problem can be, you know,
[00:11] get you a better final answer than just one.
[00:18] - Hey, I'm Alex, I lead Claude Relations here at Anthropic.
[00:21] Today we're gonna be talking about
[00:22] building more effective agents
[00:24] and I'm joined by my colleague.
[00:25] - I'm Erik, I work on multi-agent research
[00:27] here at Anthropic.
[00:28] - Erik, to kick us off here,
[00:30] can you just explain why Claude is so good at agent tasks?
[00:33] - Yeah, sure.
[00:34] So during our training,
[00:35] we let Claude practice being an agent.
[00:38] We give it open-ended problems for it to work on
[00:41] where it can take many steps
[00:43] and use tools, explore where it is and what it's working on
[00:47] before giving a final answer.
[00:49] And by getting lots of practice at being an agent,
[00:51] Claude becomes really good at this.
[00:53] - Okay, so it's these long running tasks
[00:54] and a variety of domains basically.
[00:57] And through the process of RL
[01:00] and other training mechanisms,
[01:01] Claude is learning an objective of how to do these things
[01:04] with basically limited guidance or feedback.
[01:07] - Exactly, we do lots of RL on coding tasks,
[01:10] on search tasks, lots of things for Claude
[01:12] to practice being an agent in different environments.
[01:15] - There's kind of this conception, I think of Claude models
[01:17] that they're really, really strong in code,
[01:20] but that doesn't always maybe transfer into other domains
[01:22] or that coding is its own separate thing.
[01:24] What are your kind of views on that generally?
[01:26] - So coding has been the first task
[01:28] that we've really focused on,
[01:30] but once you have an amazing coding agent,
[01:32] a coding agent can do any other kind of work.
[01:34] - If you need to do search, you can do web search,
[01:38] you know, via APIs, you can plan a weekend by,
[01:42] you know, creating a schedule.
[01:44] So we really see coding as a very fundamental skill
[01:48] for an agent that's gonna have a lot of spillover effect,
[01:50] to be able to make Claude great at all sorts of things
[01:53] and sort of like train on the hardest thing first
[01:56] and then everything else will become easy.
[01:57] - One interesting thing I've seen here recently
[02:00] with a feature that we released in Claude AI on the web
[02:04] was the ability for Claude to create actual files
[02:08] through writing code.
[02:09] So it was like writing a Python script
[02:11] and then the Python script got ran
[02:13] and all of a sudden you have like a Excel sheet
[02:15] that popped out of that.
[02:17] Is that kind of the future direction that we're headed
[02:18] is like Claude's writing scripts
[02:20] and taking actions on computers to create files
[02:23] or do things that are traditionally not code related?
[02:26] - I think that's one of the really effective ways
[02:28] Claude will be able to do these things.
[02:30] Actually, just a few days ago Claude was helping me
[02:32] make some diagrams for a presentation
[02:34] and it was able to create files
[02:36] just by writing out the SVGs,
[02:38] but then I wanted it to make a much more detailed diagram
[02:41] that would need a lot of repetition
[02:43] and so Claude was actually able to do this
[02:45] by writing some code to generate the SVG,
[02:48] which ran much, much faster than Claude itself
[02:50] needing to write you know,
[02:51] it was a very, very repetitive image file
[02:54] with lots and lots of sort of detailed patterns in it.
[02:56] - Yeah. - So, yeah,
[02:57] I think that for a lot of cases writing code
[03:00] to produce some artifact will be much better
[03:03] than just trying to create that artifact directly.
[03:05] So it's one way to do it for harder cases.
[03:07] - Okay, right, yeah.
[03:08] Code allows for kind of this speed up
[03:11] that's not even possible with like a human like clicking
[03:13] and dragging and using their mouse on a computer.
[03:16] Like repeated actions.
[03:17] - Exactly, Claude gets a for loop.
[03:18] - Yeah, if you're a developer
[03:21] and you're building an agent with Claude,
[03:23] one thing that we've started to see become really popular
[03:25] is this Claude Code SDK.
[03:26] Can you walk me through what that is
[03:28] and how you're seeing developers starting to use that?
[03:30] - Yeah, so we're really excited about developers
[03:32] using the Claude Code SDK.
[03:34] This is something where previously if you wanted
[03:37] to build a coding agent or sort of any agent,
[03:40] you had to really go from
[03:42] nothing but hitting an API endpoint,
[03:45] build the loops yourself, build all the tools,
[03:48] build executing these tools,
[03:50] interacting with files, interacting with MCP.
[03:53] We basically have already built all of that into Claude Code
[03:56] and even though its name is Claude Code,
[03:58] really Claude Code is just a general purpose agent
[04:01] that is most often used for code.
[04:03] Yeah, we are encouraging a lot of developers to use this SDK
[04:06] as the core of their agent loop
[04:08] and that way they don't have to spend a lot of time
[04:11] reinventing the wheel that we've already put a lot of time
[04:14] into polishing and perfecting that core agent loop
[04:17] and instead they can use that
[04:19] and then just add their tools
[04:21] for their own custom business logic
[04:23] or affordances into that via MCP.
[04:25] - Right, so it offers that sort of customizability
[04:28] to where you can remove the coding-specific bits.
[04:30] - Exactly. - And put in
[04:31] whatever sort of prompt or tools that you need,
[04:34] just like slots nicely into the scaffold.
[04:36] - Yeah, I think also the people
[04:37] have been using Claude Code for all sorts of things.
[04:39] I think the, my strangest use of Claude Code
[04:42] is I once had it plan a date for me
[04:44] where I did a bunch of web searches,
[04:46] found interesting activities and restaurants in the area
[04:48] and so not code related at all, but it has all the tools.
[04:51] - How was the date?
[04:52] - It was pretty good.
[04:53] It was great, yeah. - Claude did a good job?
[04:55] - Yeah, Filoli Gardens
[04:56] and then a Chinese restaurant nearby.
[04:57] - Wow, okay. - Claude did a good job.
[04:59] - I'm impressed. - Yeah.
[05:00] One other thing on Claude Code
[05:01] that has been another popular feature
[05:05] I've seen a lot of software engineers use lately
[05:07] is Claude MD files.
[05:08] So these are files that you, you know,
[05:11] define within a project
[05:12] and gives Claude relevant information about
[05:14] what your programming style is
[05:16] or like what the layout of the directories are,
[05:18] things like that.
[05:19] We've now launched a similar concept
[05:21] that maybe takes a step further called Skills.
[05:23] Can you explain what Skills are
[05:25] and how we're starting to see developers use them
[05:27] and what they mean for Agents?
[05:29] - Yeah, so Claude Skills are a very exciting extension
[05:32] of Claude MD files where instead of just giving it
[05:36] notes files, you can give it any sort of file.
[05:39] That can be PowerPoint template files, it can be code
[05:43] and like helper scripts that you want it to use.
[05:46] It can be images or assets.
[05:49] And I think this extension of not just instructions
[05:51] but resources for the agent to use
[05:54] is a really, really powerful tool where you might say,
[05:57] not just these in are my instructions
[05:59] for making PowerPoint presentations, but here's, you know,
[06:02] the head shots of all of our company leadership
[06:04] that you might need to reuse in many presentations
[06:06] and just giving it all to Claude in a reusable way.
[06:08] So it has everything it needs right there.
[06:10] - One analogy I've heard used internally
[06:13] that I really, really like is,
[06:14] it's kind of like in "The Matrix"
[06:16] when Neo is learning kung fu for the first time
[06:19] and they like inject him with the Kung Fu information
[06:22] and all of a sudden he is like a Kung Fu master.
[06:24] That feels like very similar to when I give Claude a skill
[06:27] of some type of like, here's how you create spreadsheets.
[06:29] And it's like, oh, all of a sudden
[06:30] Claude's like a banker now
[06:32] and it can create a financial model for me.
[06:34] - That and where they load in all of the racks of equipment
[06:37] and tools and stuff for them to grab.
[06:38] - Yes. - It's like, you know,
[06:39] you can start with these things, not just instructions.
[06:41] - Yeah, I love that.
[06:42] Switching gears a little bit,
[06:43] so last time we chatted on camera here a few months back
[06:48] and we were talking about Agents
[06:49] and at the time we were in this transition
[06:51] from maybe workflows which are like very defined ways
[06:55] of how you chain together prompts
[06:57] to what was just like a single agent system
[07:00] where you're running a model in a loop.
[07:02] Since then, what's been the evolution in the space?
[07:05] - Yeah, so we've really seen Agents take over from workflows
[07:08] where Claude has gotten so good at responding to feedback
[07:12] and correcting its own work
[07:14] that now Agent loops really dramatically outperform
[07:18] workflows for most things where you care most about
[07:22] absolute quality.
[07:23] Workflows are still great,
[07:24] where you need very low latency
[07:25] and you want Claude to just give a best answer, single shot.
[07:28] Agents are really, really high performance now.
[07:32] I think one of the things that I've seen develop since then
[07:35] is what I call workflows of Agents.
[07:38] Whereas previously an application might have had
[07:40] a workflow that had Claude in single shot
[07:43] write a SQL command in order to load data
[07:45] and then that would go to another step in the workflow
[07:48] where it would then write a chart to display that data.
[07:52] And if the SQL command failed, you know this,
[07:56] it doesn't know that it's not returning any data
[07:58] and then the second step of the workflow--
[07:59] - Right. - Is kind of screwed.
[08:01] - Completely falls apart.
[08:02] - But now I've seen people where each one of those steps
[08:04] in the workflow is actually a closed loop
[08:06] where instead of just writing a single attempt
[08:09] at a SQL query, it then runs, Claude sees the output
[08:13] and then it can keep iterating and repeat
[08:14] until it knows that it got the right value
[08:16] and then it transitions to the next step in the workflow.
[08:19] - Okay, interesting.
[08:20] So yes, this evolution I guess
[08:24] of like chaining together prompts
[08:26] to now chaining together agents in these loops themself,
[08:29] we'll see where that goes from there.
[08:31] One other big topic of discussion,
[08:33] I feel like that has taken a lot more chatter as of late
[08:37] is this question around observability and verification.
[08:42] Can you explain what that challenge is
[08:44] and how people are starting to think about it?
[08:46] - Yeah, so observability is very hard for Agents,
[08:49] especially as the systems get more complex
[08:51] and I think that's one of the reasons
[08:53] where I still really believe
[08:54] that even though the models are much more capable today
[08:58] than they were a year ago and they can work better
[09:01] in an agent or even more complex setups,
[09:03] I think that simplicity is still a really important thing
[09:06] and that even though you can build a big workflow of agents,
[09:10] you should still start sort of by
[09:12] from the simplest possible thing
[09:13] and then work up to a more complex solution.
[09:17] And you know, that's first trying single shotting things
[09:19] or trying, you know, single shot prompt to Claude Code SDK,
[09:23] which is now just sort of such a simple, easy thing to use.
[09:27] And then I think only as needed adding layers
[09:30] and layers of complexity
[09:31] because that's gonna make the absorbability harder.
[09:33] - Another term here maybe in parallel to workflows
[09:36] of agents is multi-agent, is that the same thing
[09:39] or is that something different?
[09:40] - Yeah, so multi-agent is my main area of research now.
[09:44] I'd say it's pretty different from a workflow of agent.
[09:46] - Okay. - Workflows of agents,
[09:48] where sort of an one agent goes,
[09:50] finishes and then it transitions
[09:52] or its output gets sent to the next agent to work on.
[09:56] Multi-agent is where fundamentally you have multiple agents
[09:59] or multiple Claudes working at the same time
[10:02] where maybe one parent agent delegates tasks
[10:07] to five sub-agents that can each then work in parallel.
[10:10] And this is how our deep research
[10:12] search product works is the main orchestrator agent
[10:16] will decide and create several sub-agents.
[10:18] They can do lots of searches in parallel
[10:20] and that's way better for the user
[10:22] because you know, all this happens in parallel
[10:24] and you get the answer back much sooner.
[10:27] We also see things like in Claude Code
[10:30] the model will use a subagent.
[10:31] So if something, if some sub-task is gonna take
[10:34] tens of thousands of tokens,
[10:36] like maybe finding a certain implementation of a class,
[10:39] but the answer really boils down to something very small,
[10:42] it can do that work in a sub-agent
[10:44] to protect the main context from all of that,
[10:48] those tokens that aren't necessary for the main work.
[10:50] So yeah, basically can offload this piece of work
[10:53] and just get back the final answer that it needs.
[10:56] - So are we exposing then this subagent in this case
[10:59] is like a tool that Claude can call upon?
[11:02] - Exactly. - Pass in,
[11:03] it'll pass in the prompt
[11:04] as like a parameter or something?
[11:05] - Exactly, yeah.
[11:06] So to the, to Claude sub-agents look like a tool
[11:09] where it can pass prompts to the sub-agents
[11:12] that will then go and do work.
[11:13] And part of my research is training Claude
[11:15] to be a better manager and know how to--
[11:17] - Oh interesting. - Give clear instructions
[11:19] to its sub-agents and make sure
[11:20] that they gets the right things
[11:21] and needs out of them.
[11:22] - How is this different than,
[11:23] or is this maybe like a specialized part
[11:25] of tool calling overall or is it different in some ways?
[11:28] - I would say that this uses the framework of tool calling
[11:31] for that communication protocol
[11:35] and it just happens to be a tool that itself
[11:37] is backed by Claude, by another Claude.
[11:39] - Does Claude have like an intuitive understanding
[11:40] of what a subagent is or do we have to like teach it?
[11:43] Like you're actually talking to another version
[11:45] of yourself, Claude,
[11:47] like don't get freaked out sort of thing?
[11:49] - I would say that Claude makes a lot of the same mistakes
[11:53] that first time managers make
[11:55] of where it will give incomplete
[11:57] or sort of unclear instructions.
[11:58] - Right, right. - To a sub-agent.
[12:00] - Right. - And you know,
[12:01] kind of expect the subagent
[12:03] to have the right context when actually it doesn't.
[12:05] And I think something we've seen
[12:07] during training on sub-agents is that Claude
[12:10] starts to get much more verbose and much more detailed
[12:12] and give its subagent the overall context
[12:15] of what's going on. - Interesting.
[12:16] - So that they can do better work
[12:17] that adds them to the whole, so.
[12:19] I'd say that, you know, it definitely Claude,
[12:23] Claude has a lot to learn
[12:24] and is learning to get better at this.
[12:25] - Okay, cool. - Yeah.
[12:27] - What are, what are some of the use cases here?
[12:29] So their search is one in like preserving context,
[12:32] is there other things
[12:33] that people are using multi-agent for right now?
[12:35] - Yeah, I think coding is,
[12:37] there's a lot of subagent use in coding.
[12:40] Anything that can be parallelized or MapReduced.
[12:43] If you have something where you need to produce
[12:45] a lot of output or there's maybe 10 parts
[12:48] of some output you're creating,
[12:50] if you can split that up among 10 sub-agents,
[12:53] that can be really, really effective for saving context
[12:56] and getting faster results.
[12:58] I think there's also a lot of interesting things to explore
[13:00] of multi-agent as a form of test time compute.
[13:04] - Basically letting Claude,
[13:06] many Claudes work on a problem can be, you know,
[13:09] get you a better final answer than just one.
[13:11] Just like with people, you know,
[13:12] a bunch of people putting their heads together
[13:14] can get better results.
[13:15] - In that case, are we specializing these agents in any way?
[13:19] Do we gear them towards like one type of persona or another,
[13:22] or is it just kind of let them take whatever form?
[13:25] - I think you can do either.
[13:27] You know, sometimes it's helpful to give a bunch of people
[13:29] the same exact task and see
[13:31] what the different answers they come up with are.
[13:33] Sometimes it's good to have many people
[13:34] or many agents work from different approaches
[13:36] to the same problem or split it up.
[13:39] One thing I've seen a lot is customers
[13:42] that have a lot of tools, maybe 100 or 200 tools
[13:45] that they want an agent to use,
[13:47] they found that it's really good to split up
[13:49] those tools among sub-agents.
[13:51] So the main agent, all it has to know is hey,
[13:53] I want to use this bucket of tools
[13:56] and then there's a subagent that goes
[13:57] and does the actual work there.
[13:59] So that each subagent just has maybe 20 tools
[14:02] that it needs to understand and know how to use.
[14:04] - Have we tried like scaling agents like all the way up?
[14:07] Like what happens if you have like a thousand versions
[14:09] of Claude all working on one problem?
[14:11] Does it just turn into chaos?
[14:13] - I've not tried that yet. - Okay.
[14:14] - But I'll get back to you.
[14:15] - Good research idea right there.
[14:17] What are some of other like failure modes
[14:19] that we're seeing right now with agents or multi-agents?
[14:22] - Yeah, I think just like any sort of complex system,
[14:26] I think it's easy to overbuild something
[14:28] and lose a lot of efficiency
[14:29] and just create sort of a lot of like dead weight.
[14:32] And so I've seen overbuilt multi-agent systems
[14:35] spend too much time just talking back and forth
[14:38] with each other and not actually making progress
[14:40] on the main task, and you know,
[14:42] human agents or human organizations suffer from the stew.
[14:45] As companies get bigger,
[14:47] you have more communication overhead and you know,
[14:49] less and less work is actually, you know,
[14:51] the people on the ground making progress on things.
[14:54] - And so I think that's another interesting thing to study
[14:56] is like how can we make organizations of Claudes
[15:00] very effective while keeping the overhead small?
[15:03] - If I'm a developer and I want to get started with agents,
[15:06] whether I'm building on the Claude Code SDK
[15:08] or just trying to on my own, do you have any tips
[15:10] or best practices that you'd give them?
[15:12] - Yeah, I think the best practices really remain
[15:15] start simple and make sure, you know,
[15:17] you only add complexities you need.
[15:19] I think another really important thing
[15:21] is think from the point of view of your agents.
[15:24] If you are giving Claude tools or prompts
[15:27] or sort of any affordances, put yourself in Claude's shoes
[15:31] and read what it actually gets, what it sees as the model
[15:35] and make sure there's actually enough information there
[15:37] for you to solve the problem.
[15:39] It's very easy to sort of forget, you know,
[15:42] that we're seeing everything
[15:43] and the model only sees what we showed.
[15:46] - Right. - And it's.
[15:47] - Yeah. - Yeah, I feel like
[15:48] it's always important to go back
[15:49] into like the raw transcript of like your tool calls
[15:53] and your logs and everything and just view that.
[15:56] - Exactly, and I think another thing
[15:57] is that as people are building more things like MCPS
[16:00] and trying to connect Claude to more things,
[16:03] I think a very natural first instinct that people have
[16:07] that's very wrong is that an MCP
[16:10] or tools should be one-to-one with your API
[16:13] and I think actually tools for the model or MCPs
[16:17] should be one-to-one with your UI, not your API.
[16:21] Because ultimately the model is a user of these things.
[16:24] It's not, it doesn't work like a traditional program.
[16:27] So if your API might have three separate endpoints
[16:30] for say loading a Slack conversation
[16:34] and turning a user ID into a username
[16:37] and turning a channel ID into a channel name.
[16:40] If those are the tools you give the model
[16:41] to understand Slack, for it to understand anything,
[16:45] it's gonna have to make three tool calls.
[16:47] Versus as a user, you know,
[16:48] we just see everything all nicely rendered.
[16:50] - Oh, that's interesting. - So you wanna create a tool
[16:53] or an MCP for the model
[16:54] that it presents everything all at once
[16:57] with as little interaction as possible.
[16:59] Just like for a user it'll be terrible
[17:01] if every time you had Slack
[17:02] you had to like click on a user ID
[17:04] to see what the name was, et cetera.
[17:06] - Right, right, I like that.
[17:07] So kind of working back from like the end state almost
[17:10] instead of like just trying to map
[17:11] the technical specs one to one.
[17:12] - Exactly, and sort of surround
[17:14] whatever context you need with it.
[17:15] - What do you think the future of Agents
[17:18] has in store for us?
[17:19] Any predictions on these next six to 12 months?
[17:22] - I think Agents are gonna become a lot more pervasive
[17:25] sort of starting in areas that are verifiable
[17:27] like software engineering.
[17:29] You know, coding agents have already changed how I work
[17:32] and how tons of people at Anthropic work
[17:35] and I think there's still a huge amount
[17:36] to be be gained there.
[17:38] I think one of the really exciting things is if agents
[17:40] can start getting better at verifying their own work
[17:44] with things like computer use of, they can write a web app,
[17:47] but can they go actually open it up and test it
[17:49] and then find their own bug
[17:51] instead of you needing to do that.
[17:52] I think that's one of the most exciting things.
[17:53] - Yeah. - Is like closing
[17:54] that loop of testing
[17:56] so that I don't have to be Claude's QA engineer.
[17:58] - Right, so kind of combining all these things
[18:00] from the software engineering abilities
[18:02] to the computer use abilities
[18:04] once we put all these pieces together.
[18:06] - Yep, and I think the computer use
[18:08] is also gonna really open up a lot of other avenues
[18:12] and domains where agents
[18:13] have been sort of locked out of so far.
[18:15] - What would be an example of that?
[18:17] - I think that if you want to have Claude
[18:18] sort of do work for you in a Google Doc.
[18:21] - Yeah. - Right now it's,
[18:22] you know, Claude can write for you
[18:23] but you're copy and pasting back and forth.
[18:25] - Right. - But if you have computer use
[18:26] and you say, Hey Claude, can you clean up this Google doc?
[18:29] It can just do it right there for you.
[18:30] Scrolling around, clicking, editing the text
[18:32] and that's just such a nicer experience
[18:34] than needing to copy and paste back and forth.
[18:37] - Yeah. - It's like wherever you are,
[18:38] Claude can be there with you if it has with computer use.
[18:41] - Well I'm very excited to have Claude write my Google Docs
[18:43] and respond to all of my comments for me.
[18:45] - Exactly. - That'd be
[18:46] a very nice future.
[18:48] Erik, this has been great.
[18:49] Thank you so much for the conversation.
[18:50] - Absolutely, thank you.
