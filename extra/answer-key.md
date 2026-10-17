# Answer key and explanations: full exam simulation

Claude Certified Architect – Foundations (CCAR-F) · Extra section: full exam simulation

Every question is original, written for this course against the official blueprint. None is copied from the real exam or the guide's sample questions, and none repeats a question from the quick checks, the module quizzes, the readiness check or the three practice exams. Use this key after the videos, to re-read a reason or check a question you paused on.


## Part 1: Scenario 1, Customer Support Resolution Agent · questions 1–15

> Customer support resolution agent. You are building a support agent with the Claude Agent SDK for an online retailer. It resolves returns, billing disputes and account problems through custom MCP tools (get_customer, lookup_order, process_refund, escalate_to_human). The goal is to resolve at least 80% of contacts on first contact while handing the right cases to people.

### Question 1 · Multiple choice

A team writes its own agentic loop on the Messages API for the support agent. Which signal should decide whether the loop runs the requested tools and calls Claude again?

- **A.** Whether the reply's text says the case is closed, with words such as "Done" or "Resolved".
- **B.** Its stop_reason: run the tools and call again on tool_use, and return on end_turn.
- **C.** Whether the response holds any text block, since a tool request never comes with text.
- **D.** A limit of eight calls per conversation, chosen from the average ticket length.

**Answer: B** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.1 · Lesson 1.4

- **A** (wrong): Text is written for the customer; reading it for a finish signal is fragile, and it ignores pending tool calls.
- **B** (right): stop_reason is the API's own statement of why the turn ended, so it says exactly when tools are waiting.
- **C** (wrong): A response can carry text and tool_use blocks together, so the test misses real tool requests.
- **D** (wrong): A cap is a safety limit; as the loop's control it stops some cases early and wastes calls on others.

### Question 2 · Multiple choice

Customers often put several problems in one message, such as a damaged item, a double charge and a new delivery address. In 18% of those messages the agent fixes the first problem well and never mentions the others. Which change addresses the cause?

- **A.** Send every multi-issue message straight to a human agent, since the bot handles single issues well.
- **B.** Shorten the system prompt, so the agent has more room in its context for long messages.
- **C.** Ask customers to write one problem per message, and close the chat after each resolution.
- **D.** Have the agent list each separate concern first, investigate each one, and reply once with a resolution for all of them.

**Answer: D** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.4 · Lesson 3.6

- **A** (wrong): It gives up cases the agent can resolve and lowers first-contact resolution.
- **B** (wrong): The messages are short; the agent stops after one concern because nothing makes it track the rest.
- **C** (wrong): It pushes the work onto the customer and lengthens every multi-issue contact.
- **D** (right): Naming the concerns up front gives each one its own investigation, and the single reply is checked against that list.

### Question 3 · Multiple choice

After a merger, half of all orders sit in the acquired company's system, which answers with epoch-second timestamps and numeric status codes; the main system already answers with ISO dates and words. Customers of the acquired brand are told their parcel left on 1 January 1970. What is the most reliable fix?

- **A.** A PreToolUse hook that blocks lookup_order calls for orders in the older system.
- **B.** Add a convert_date tool that Claude can call whenever a date looks wrong.
- **C.** A PostToolUse hook that converts both systems' results to one format, ISO dates and status words, before Claude sees them.
- **D.** Describe both formats in the system prompt, and ask Claude to convert dates and codes before answering.

**Answer: C** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.5 · Lesson 3.4

- **A** (wrong): Those are real orders; blocking them leaves customers without an answer.
- **B** (wrong): Claude has to notice the problem first, the same judgment that is failing now.
- **C** (right): The conversion runs in code on every result, so Claude only ever reads one format.
- **D** (wrong): The model still has to convert every time, which is exactly the step that slips.

### Question 4 · Multiple choice

To compare two compensation policies, the team replays a recorded conversation up to the moment the customer asks for compensation. It wants the agent to continue twice, once offering a refund and once a replacement, each from exactly that state. Which approach fits?

- **A.** Start two fresh sessions, each with a written summary of the conversation pasted in.
- **B.** Resume the same session twice in a row without forking, once per policy.
- **C.** Run both policies in one session, asking the agent to answer once for each.
- **D.** Resume the recorded session with fork_session, once per policy, so each branch starts from the same history.

**Answer: D** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.7 · Lesson 3.8

- **A** (wrong): A summary isn't the same state; details the agent had seen are lost, and the two may differ.
- **B** (wrong): The second run continues after the first branch, so it doesn't start from the shared point.
- **C** (wrong): Each answer sees the other one, so the branches aren't independent.
- **D** (right): A fork copies the history up to that point into a new session, so both branches share the start and stay independent.

### Question 5 · Multiple response

The support agent hands warranty questions to a warranty subagent. The subagent's answers keep asking the customer for the order number and the product, although the customer gave both earlier in the chat. Which two should the coordinator put in the subagent's prompt? (Choose two.)

- **A.** Nothing more; the subagent should ask the customer for anything it is missing.
- **B.** The order number, the product and the facts already established in the chat.
- **C.** The customer's exact warranty question, and what the agent has already checked or told them.
- **D.** The coordinator's own system prompt, so the subagent follows the same rules.
- **E.** The full raw transcript, every tool call and result included, so nothing can be missed.

**Answer: B and C** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.3 · Lesson 4.2

- **A** (wrong): That is the behavior being fixed: it makes the customer repeat themselves.
- **B** (right): A subagent sees only the prompt it is given, so the facts it needs must be in it.
- **C** (right): The subagent can then answer the real question without repeating work or contradicting the agent.
- **D** (wrong): The subagent has its own role and prompt; copying the coordinator's doesn't pass the case facts.
- **E** (wrong): It floods the subagent with noise and cost; the relevant facts are what it needs.

### Question 6 · Multiple choice

A support coordinator has three subagents: orders, billing and returns. Logs show it sends every customer message to all three and merges their answers. Costs have tripled, and some replies contradict themselves. What should change?

- **A.** Let the three subagents message each other until they agree, before anything is sent.
- **B.** Keep sending each message to all three, and have the coordinator keep the longest answer.
- **C.** Remove the coordinator, and let each subagent reply to the customer directly.
- **D.** Have the coordinator delegate each message only to the subagents it concerns, and combine the results.

**Answer: D** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.2 · Lesson 4.1

- **A** (wrong): It adds more calls on top of the waste, and every message still goes to all three.
- **B** (wrong): Cost stays tripled, and the longest answer isn't the right one.
- **C** (wrong): Nobody reconciles the answers any more, so the customer gets several replies.
- **D** (right): Routing by concern removes the wasted calls, and one coordinator still reconciles what comes back.

### Question 7 · Multiple response

In a hand-written loop on the Messages API, which two steps are required for Claude to use tool results correctly? (Choose two.)

- **A.** Put the tool results into the system prompt, so they stay available for the whole chat.
- **B.** Append Claude's whole response, its tool_use blocks included, to the messages before sending results.
- **C.** Run the requested tools only after Claude has stopped with end_turn.
- **D.** Return each result in a tool_result block with the matching tool_use_id, in the next user message.
- **E.** Give each result a fresh id generated by the application, so ids never repeat.

**Answer: B and D** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.1 · Lesson 1.3

- **A** (wrong): Results belong in the conversation as tool_result blocks, answering the calls that requested them.
- **B** (right): The tool_result blocks refer to those tool_use blocks, so they must stay in the history.
- **C** (wrong): Tools run when the stop reason is tool_use; end_turn means Claude has finished.
- **D** (right): The id ties each result to the call that asked for it.
- **E** (wrong): The result must carry the id from Claude's tool_use block, or it can't be matched.

### Question 8 · Multiple choice

The agent has refund_payment and issue_store_credit. Their descriptions read "Gives the customer money back" and "Gives the customer value back". Customers who ask for store credit often get a card refund instead. What should the team change first?

- **A.** Add a system prompt line: always prefer store credit unless the customer insists on a refund.
- **B.** Merge both into one compensate_customer tool, with a free-text field for the method.
- **C.** Rewrite each description to say what the tool does, when to use it instead of the other, what it needs and what it returns.
- **D.** List issue_store_credit first in the tools array, so it is considered first.

**Answer: C** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.1 · Lesson 2.1

- **A** (wrong): It biases every case instead of letting Claude tell the two tools apart.
- **B** (wrong): The choice moves into free text, which is harder to validate and to audit.
- **C** (right): Claude chooses tools from their descriptions, so the descriptions must draw the line between the two.
- **D** (wrong): Tool order isn't a routing signal; the near-identical descriptions remain.

### Question 9 · Multiple choice

process_refund is called for an order delivered 41 days ago, and the refund policy allows 30 days. What should the tool return to the agent?

- **A.** An error result marked retryable, so the agent can try again in a few minutes.
- **B.** A normal result with the text "refund declined", so the conversation isn't interrupted.
- **C.** A business-rule error marked not retryable, with a short reason the agent can explain to the customer.
- **D.** An exception that ends the conversation, since a policy violation should stop the agent.

**Answer: C** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.2 · Lesson 2.4

- **A** (wrong): The policy window won't change in a few minutes; every retry fails the same way.
- **B** (wrong): Marking a failure as success invites the agent to treat the refund as done or to try again.
- **C** (right): The agent learns that retrying won't help, and it has the words to tell the customer why.
- **D** (wrong): The customer is left with no answer, when the agent could explain and offer alternatives.

### Question 10 · Multiple choice

The team wants the agent's very first action in every conversation to be a call to get_customer, and after that it should choose tools freely. How should tool_choice be set?

- **A.** Name get_customer in tool_choice for the whole conversation.
- **B.** Set tool_choice to none on the first request, so the agent reads the policy before acting.
- **C.** Set tool_choice to any for the whole conversation.
- **D.** Name get_customer in tool_choice on the first request, then use auto on every request after it.

**Answer: D** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.3 · Lesson 2.3

- **A** (wrong): Then every turn must call get_customer, and the agent can never use another tool.
- **B** (wrong): none forbids tools on that request, the opposite of what is wanted.
- **C** (wrong): any forces some tool on every turn, not necessarily get_customer, and never allows a plain reply.
- **D** (right): Forcing the named tool once guarantees the first call; auto afterwards gives the agent its normal freedom.

### Question 11 · Multiple choice

In the Agent SDK, the support tools come from an MCP server registered under the name support. Which allowed_tools entry allows only its process_refund tool?

- **A.** mcp__support__process_refund
- **B.** process_refund@support
- **C.** mcp__support__*
- **D.** support.process_refund

**Answer: A** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.4 · Lesson 2.6

- **A** (right): MCP tools are named mcp, the server name and the tool name, joined by double underscores.
- **B** (wrong): That isn't how MCP tool names are written, so it matches nothing.
- **C** (wrong): The wildcard covers the whole server, so it allows every one of its tools.
- **D** (wrong): That isn't how MCP tool names are written, so it matches nothing.

### Question 12 · Multiple choice

Midway through long chats about several orders, the agent swaps one order's delivery date for another's. Every lookup_order call adds roughly sixty JSON fields, mostly carrier scans and warehouse codes, and the conversation uses a handful. What helps most?

- **A.** Tell Claude in the system prompt to ignore fields it doesn't need.
- **B.** Trim each lookup result to the fields the task uses, such as status, dates and amounts, before it's added.
- **C.** Switch the agent to a model whose context window is larger.
- **D.** Summarize the whole conversation every ten turns, amounts and order numbers included.

**Answer: B** · Domain 5 (Context Management & Reliability) · Task Statement 5.1 · Lesson 3.7

- **A** (wrong): The fields still sit in the context on every turn.
- **B** (right): Less irrelevant text accumulates, so the facts that matter stay easy to find.
- **C** (wrong): The chat still fills with irrelevant fields; a bigger window holds more noise.
- **D** (wrong): Summaries blur exact values, and the noise returns with the next lookups.

### Question 13 · Multiple response

Which two customer messages should make the agent hand the case to a human right away? (Choose two.)

- **A.** "I'm really annoyed this came late! Where is the refund for order 2210?"
- **B.** "Can I talk to a real person about this, please?"
- **C.** "I'm not sure the refund went through. Can you confirm?"
- **D.** "The seller cancelled my pre-order, and your policy says nothing about that. Am I compensated?"
- **E.** "Can you check where my order 4471 is right now, please?"

**Answer: B and D** · Domain 5 (Context Management & Reliability) · Task Statement 5.2 · Lesson 3.5

- **A** (wrong): Frustration alone isn't a trigger; the agent can look up the refund.
- **B** (right): An explicit request for a human is honored at once.
- **C** (wrong): The agent can check and confirm it with its tools.
- **D** (right): The policy is silent on this case, so a person should decide.
- **E** (wrong): A routine status question the agent resolves with its tools.

### Question 14 · Multiple choice

When the payment gateway returns a timeout, the agent hands every case to a human, and the support queue overflows on busy evenings. Most timeouts succeed on a second attempt. What should change?

- **A.** Retry transient gateway failures a few times with a short wait; hand over only if they keep failing.
- **B.** Have the agent tell the customer the refund went through, since most timeouts succeed later.
- **C.** Stop handing over on any gateway error, and tell the customer to try again later.
- **D.** Raise the gateway's timeout to two minutes for every call.

**Answer: A** · Domain 5 (Context Management & Reliability) · Task Statement 5.3 · Lesson 4.6

- **A** (right): Local recovery handles the common case, and a person only sees the failures that persist, with their context.
- **B** (wrong): It reports an unknown outcome as a success, which is the most expensive error.
- **C** (wrong): Persistent failures then go nowhere, and the customer does the agent's job.
- **D** (wrong): Customers wait longer on every call, and real outages still reach the queue.

### Question 15 · Multiple choice

Product managers want a weekly analysis of 3,000 closed support tickets to find recurring product defects. Nobody knows in advance which defects will show up. How should the work be decomposed?

- **A.** A fixed pipeline with one prompt per defect category in last quarter's list.
- **B.** One request that reads all 3,000 tickets together and lists every defect.
- **C.** Map themes on a sample first, then dig into each theme, adjusting the plan as findings arrive.
- **D.** One subagent per support agent, each reviewing only its own closed tickets.

**Answer: C** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.6 · Lesson 4.4

- **A** (wrong): New defects fall outside last quarter's categories, so they're never found.
- **B** (wrong): Far too much input for one pass, and details in the middle get lost.
- **C** (right): An open-ended question needs a plan that adapts to what each step finds.
- **D** (wrong): Splitting by who handled a ticket scatters each defect across many reports.


## Part 2: Scenario 4, Developer Productivity with Claude · questions 16–30

> Developer productivity with Claude. You are building an internal developer tool with the Claude Agent SDK. It helps engineers explore unfamiliar code, understand a legacy system, generate boilerplate and automate repetitive tasks, using the built-in tools (Read, Write, Edit, Bash, Grep, Glob) and MCP servers.

### Question 16 · Multiple choice

In a code-migration tool built with the Agent SDK, an analysis subagent reports back in free prose: "several handlers still use the old client." The coordinator then has to search the repository again to find which ones. What should the subagent's prompt ask it to return?

- **A.** Only a count of the handlers that still use the old client.
- **B.** A list of findings, each with its file, line and the call found, apart from any commentary.
- **C.** A longer prose report that describes each of the handlers in more detail.
- **D.** Its full transcript, so the coordinator can see every search it ran.

**Answer: B** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.3 · Lesson 4.2

- **A** (wrong): A count can't tell the coordinator where to make the changes.
- **B** (right): The coordinator gets the locations as data it can act on, without searching again.
- **C** (wrong): More prose still leaves the coordinator to dig the locations out.
- **D** (wrong): It floods the coordinator's context; what it needs is the findings.

### Question 17 · Multiple choice

An engineer asks the agent to map how three independent services handle authentication. The trace shows the coordinator starting the first subagent, waiting for its answer, then the second, then the third: nine minutes in all. How can the same work finish sooner?

- **A.** Raise max_turns for each subagent, so none of them stops early.
- **B.** Merge the three subagents into one, with a longer prompt that covers all three services.
- **C.** Have the coordinator issue all three subagent calls in one response, so the three run in parallel.
- **D.** Ask each subagent to start the next one when it finishes.

**Answer: C** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.2 · Lesson 4.3

- **A** (wrong): They weren't stopping early; they were running one at a time.
- **B** (wrong): One agent then works through the services one after another, in a context three times as full.
- **C** (right): Independent work started in the same turn runs concurrently, so the wait is about one subagent's time.
- **D** (wrong): That keeps them in sequence and moves control away from the coordinator.

### Question 18 · Multiple choice

The agent must move 140 test files from one assertion library to another. The files follow four patterns. A single long session handled the first 60 files well, then began skipping files and repeating finished ones. Which approach should the team take?

- **A.** A fixed pipeline: the same instructions file by file, then a final pass that runs the whole suite.
- **B.** Let one agent choose which file to open next, in a single session, until every file is done.
- **C.** Give each of the four patterns its own subagent, which edits all files of its pattern in one session.
- **D.** Send all 140 files in one prompt and ask for every rewrite in a single answer.

**Answer: A** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.6 · Lesson 4.4

- **A** (right): Each step starts with a small, focused context, and the last pass catches what only shows across files.
- **B** (wrong): That is the long session that degraded.
- **C** (wrong): The sessions are still long, and a file can mix patterns, so the work splits along the wrong lines.
- **D** (wrong): The output is far too large for one answer, and quality drops across that much input.

### Question 19 · Multiple choice

An engineer spent two hours with the agent analyzing a legacy billing module, then stopped for the night. The next morning nothing in the repository has changed. What is the most efficient way to continue?

- **A.** Start a new session and paste the last answer from yesterday as its first message.
- **B.** Start a new session and run the whole analysis again from the beginning.
- **C.** Resume yesterday's session, then run /clear so the work starts on a clean slate.
- **D.** Resume yesterday's session by its ID, since everything it learned still matches the code.

**Answer: D** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.7 · Lesson 3.8

- **A** (wrong): One answer is a fraction of what the session knew, so much of the analysis is lost.
- **B** (wrong): It repeats two hours of work that is still correct.
- **C** (wrong): /clear throws away the context that resuming brought back.
- **D** (right): The earlier analysis is still valid, so continuing it saves re-reading the whole module.

### Question 20 · Multiple choice

While tidying branches, the agent has run git push --force twice this month. The team wants that to be impossible, whatever the prompt or the task says. What should they add?

- **A.** A PreToolUse hook on Bash that denies any git push with --force or -f, and tells the agent why.
- **B.** A rule in the system prompt: never force-push under any circumstances.
- **C.** A PostToolUse hook that restores the remote branch after a forced push.
- **D.** Remove Bash from the agent's tools entirely.

**Answer: A** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.5 · Lesson 3.4

- **A** (right): The hook runs before every Bash call, so the command can never execute.
- **B** (wrong): An instruction lowers the odds but can't make the push impossible.
- **C** (wrong): It runs after the damage, and a restore can itself fail or race other pushes.
- **D** (wrong): The agent also needs Bash to run tests and builds.

### Question 21 · Multiple choice

On large refactors, some runs end with the result subtype error_max_turns, and engineers start the task over. What does that subtype mean, and what should they do instead?

- **A.** The loop hit its turn limit before Claude finished; resume the session to continue.
- **B.** The context window overflowed; switch to a model with a larger window.
- **C.** The model refused the task; rephrase the request and run it again.
- **D.** A tool failed; read that tool's error message and fix the tool.

**Answer: A** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.1 · Lesson 3.1

- **A** (right): The work so far is in the session, so continuing it is faster than starting again.
- **B** (wrong): The subtype says the turn budget ran out, not the context.
- **C** (wrong): A refusal isn't reported as a turn limit.
- **D** (wrong): Tool failures come back as tool results inside the loop, not as this subtype.

### Question 22 · Multiple response

Developers keep finding commits from the agent that broke the build: it committed before running the tests, or after they failed. Which two pieces together make sure a commit happens only after a passing test run in the same session? (Choose two.)

- **A.** A PostToolUse hook on the test command that records in session state whether the run passed.
- **B.** A line in the system prompt: always run the tests before you commit.
- **C.** A request that the agent state the test result in its final message.
- **D.** The test command added to CLAUDE.md, so the agent knows which command to run.
- **E.** A PreToolUse hook that denies git commit unless that state shows a passing run.

**Answer: A and E** · Domain 1 (Agentic Architecture & Orchestration) · Task Statement 1.4 · Lesson 3.3

- **A** (right): Code, not the model, knows the last real test result.
- **B** (wrong): An instruction can be skipped; nothing checks it.
- **C** (wrong): That reports after the fact and can be wrong.
- **D** (wrong): Knowing the command doesn't make the agent run it before committing.
- **E** (right): The commit is blocked in code until a passing run exists.

### Question 23 · Multiple response

Which two pairings of a task with a built-in tool are right? (Choose two.)

- **A.** Find every file named *.proto under services/: Glob.
- **B.** Find one error code in a 4,000-line log: Read the whole file.
- **C.** Find the files whose text mentions "deprecated": Glob.
- **D.** Find every call to retryPolicy( across the repository: Grep.
- **E.** Change one line that appears in three files: Write each file again from memory.

**Answer: A and D** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.5 · Lesson 2.7

- **A** (right): Glob matches file paths by pattern.
- **B** (wrong): Grep finds the line directly without loading the file into context.
- **C** (wrong): That's a content search, which is Grep's job; Glob only matches names.
- **D** (right): Grep searches file contents.
- **E** (wrong): Edit changes the exact text; rewriting from memory risks losing other content.

### Question 24 · Multiple choice

Asked how a request travels from the HTTP layer to the database in an unfamiliar 2,000-file service, the agent starts reading files in alphabetical order and runs out of context halfway. What should it do instead?

- **A.** Read every file in the src folder first, so nothing relevant is missed.
- **B.** Ask the developer to paste the files they think are relevant into the chat.
- **C.** Grep for the route's handler, then Read along the calls it makes, one file at a time.
- **D.** Glob for *.py and summarize each matching file before tracing anything.

**Answer: C** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.5 · Lesson 2.7

- **A** (wrong): Same problem: it loads far more than the question needs.
- **B** (wrong): The agent can find the path itself with its tools; this hands the work back.
- **C** (right): It loads only the files on the path, found as it follows the calls.
- **D** (wrong): Glob only lists names; summarizing everything is still reading everything.

### Question 25 · Multiple response

An engineer wants a personal notes MCP server in every project they open, and nobody else should get it. The team's Sentry server must reach everyone who clones the repository, without its token in git. Which two choices are right? (Choose two.)

- **A.** Add the notes server with user scope, in the engineer's own configuration.
- **B.** Put the Sentry server in the repository's .mcp.json, with the token written as ${SENTRY_AUTH_TOKEN}.
- **C.** Put the Sentry server in .mcp.json with the team's token typed into its env block.
- **D.** Have each developer add the Sentry server by hand with local scope.
- **E.** Put the notes server in the repository's .mcp.json.

**Answer: A and B** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.4 · Lesson 2.6

- **A** (right): User scope applies to all their projects and is never shared.
- **B** (right): The config is shared through git, and each developer's token comes from their own environment.
- **C** (wrong): The token ends up in git for everyone to read.
- **D** (wrong): Nothing is shared through the repository, so setups drift.
- **E** (wrong): Then every teammate gets the engineer's personal server.

### Question 26 · Multiple choice

The agent is connected to two MCP servers, docs and code, and each has a tool called search described as "Search." The agent often searches the code server for runbooks and the docs server for function definitions. What should the team do?

- **A.** Add a system prompt line telling the agent to think carefully about which search to use.
- **B.** Merge both servers' searches into one tool that queries docs and code together.
- **C.** Disconnect the docs server while the agent works on code.
- **D.** Rename them search_docs and search_code, and describe what each searches and when to use it.

**Answer: D** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.1 · Lesson 2.2

- **A** (wrong): Nothing in the tools tells Claude which is which, so care alone can't help.
- **B** (wrong): Results mix code and docs, and every search pays for both.
- **C** (wrong): Engineers ask about both, so the agent loses a source it needs.
- **D** (right): Distinct names and boundaries let Claude tell the two tools apart.

### Question 27 · Multiple choice

In plan mode, an engineer asks Claude to study how 30 services call the auth library before proposing a change. The investigation fills the main conversation with file contents, and the plan that follows misses details found early on. What should the engineer do next time?

- **A.** Leave plan mode, so Claude can edit files while it investigates.
- **B.** Have an Explore subagent investigate and return a summary, then plan from that summary.
- **C.** Paste all 30 services' files into one message, so Claude sees everything at once.
- **D.** Run /compact in the middle of the investigation.

**Answer: B** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.4 · Lesson 5.5

- **A** (wrong): Editing doesn't make the reading any shorter, and changes land before a plan exists.
- **B** (right): The verbose reading stays in the subagent's context, and the plan starts from a short, complete summary.
- **C** (wrong): The context fills even faster.
- **D** (wrong): Compaction keeps a summary but can drop the early details the plan needed.

### Question 28 · Multiple choice

A repository's CLAUDE.md has grown to 900 lines: API conventions, testing, deployment and more. The team wants it modular, with the same content loaded as before. What fits?

- **A.** Put each topic's section in a CLAUDE.md inside the top-level folder with the closest name.
- **B.** Move the sections into README.md, which Claude reads automatically.
- **C.** Move each topic into its own file and import those files from CLAUDE.md with the @path syntax.
- **D.** Keep one file and move the most important sections to the top.

**Answer: C** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.1 · Lesson 5.2

- **A** (wrong): Folder CLAUDE.md files load by location, not by topic, so content would load at the wrong times.
- **B** (wrong): README.md isn't loaded as memory.
- **C** (right): Imports keep one entry point while each topic lives in its own file.
- **D** (wrong): The file stays one large block that is hard to maintain.

### Question 29 · Multiple choice

An engineer asks Claude to build a caching layer for an internal API. They haven't decided the expiry time, how entries are invalidated, or whether stale reads are acceptable. What is the best first step?

- **A.** Write the caching code by hand, and ask Claude only for the tests.
- **B.** Ask for an implementation now, and correct it in code review.
- **C.** Have Claude interview them about requirements and edge cases, then implement.
- **D.** Ask for three different implementations and pick the best one.

**Answer: C** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.5 · Lesson 5.6

- **A** (wrong): The tests would encode the same unmade decisions.
- **B** (wrong): Claude guesses each open decision, and review finds them one by one.
- **C** (right): The open decisions surface before any code depends on a guess.
- **D** (wrong): Three guesses still answer questions nobody has decided.

### Question 30 · Multiple choice

A documentation subagent only needs to read code and update Markdown files under docs/. It was defined with every built-in tool, and last week it ran a cleanup script through Bash that deleted generated files. What should change?

- **A.** Keep every tool, and review the subagent's commands after each run.
- **B.** Tell the subagent in its prompt to use Bash only for safe commands.
- **C.** Give the coordinator the documentation work instead, with every tool.
- **D.** Give the subagent only the tools its role needs, such as Read, Grep, Glob and Edit.

**Answer: D** · Domain 2 (Tool Design & MCP Integration) · Task Statement 2.3 · Lesson 4.5

- **A** (wrong): The review comes after the damage.
- **B** (wrong): It is still an instruction; the tool stays available.
- **C** (wrong): The same broad tool set moves to an agent with an even wider role.
- **D** (right): A subagent can only use the tools in its definition, so the risky ones aren't there to misuse.


## Part 3: Scenario 5, Claude Code for Continuous Integration · questions 31–45

> Claude Code for continuous integration. You are adding Claude Code to a CI/CD pipeline. It reviews pull requests, generates test cases and leaves feedback developers act on. The prompts must give actionable feedback and keep false positives low.

### Question 31 · Multiple choice

Release notes for a CI change say the review step now runs claude --bare -p for a quicker start. Since that release, review comments contradict the naming rules in the repository's CLAUDE.md, which nobody touched. What explains this, and what fixes it?

- **A.** --bare skips auto-discovered configuration such as CLAUDE.md; drop --bare, or pass the conventions in explicitly.
- **B.** CI runners can't read files outside the job's working directory; copy CLAUDE.md into the job's folder.
- **C.** CLAUDE.md applies only to interactive sessions; repeat the conventions in the prompt of every run.
- **D.** The model ignores long CLAUDE.md files under -p; shorten the file to fit.

**Answer: A** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.6 · Lesson 6.1

- **A** (right): The run stopped loading the file, so the conventions never reach the reviewer.
- **B** (wrong): The file is in the checkout; it was skipped, not out of reach.
- **C** (wrong): A plain -p run does load CLAUDE.md; only --bare skips it.
- **D** (wrong): Length isn't the cause; the file isn't being loaded at all.

### Question 32 · Multiple choice

A CI review step should read the code and run npm run lint, but must never edit files or push. Under -p with no permission settings, the run can't use the linter. What should the invocation include?

- **A.** --verbose, so the job log shows which approval is missing.
- **B.** --allowedTools with Read, Grep, Glob and Bash(npm run lint *), so only those run unprompted.
- **C.** --dangerously-skip-permissions, so the run never stops for an approval.
- **D.** A sentence in the prompt saying the linter is allowed and edits are not.

**Answer: B** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.6 · Lesson 6.1

- **A** (wrong): Logging the problem doesn't grant the permission.
- **B** (right): Pre-approved tools run headless, and everything else stays unavailable.
- **C** (wrong): It also allows edits and pushes, which the step must never do.
- **D** (wrong): The prompt doesn't grant permissions; the linter still can't run.

### Question 33 · Multiple choice

Each night a job has Claude patch failing checks, then asks the same conversation to look over its own patch before a pull request opens. That step approves nearly everything, but a third of the patches later turn out to be buggy. What should change?

- **A.** Review in a separate claude -p run that sees only the diff, not the writing session.
- **B.** Ask the same session to review its own fix twice before it posts.
- **C.** Turn on extended thinking in the same session for the review step.
- **D.** Tell the session to be very critical when it reviews its own work.

**Answer: A** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.6 · Lesson 6.5

- **A** (right): An independent instance doesn't share the reasoning that produced the fix, so it can question it.
- **B** (wrong): It reviews with the same context and assumptions, so it misses the same things.
- **C** (wrong): More reasoning in the same context still carries the same blind spots.
- **D** (wrong): An instruction doesn't remove the context that produced the fix.

### Question 34 · Multiple choice

Developers want to start the team's standard code review inside their Claude Code sessions with one short command. Everyone should get the same instructions, kept up to date through the repository. What should the team set up?

- **A.** A personal skill in each developer's ~/.claude/skills/, copied from the wiki.
- **B.** A project skill in .claude/skills/, committed with the repo and started as /review.
- **C.** The review instructions in each developer's ~/.claude/CLAUDE.md.
- **D.** A copy of the review prompt on the wiki, pasted by developers into their sessions.

**Answer: B** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.2 · Lesson 5.4

- **A** (wrong): Personal copies drift, and nothing updates them through the repository.
- **B** (right): It is shared through version control, so every developer gets the same command and every update.
- **C** (wrong): Personal memory isn't shared through the repository, and it isn't a command.
- **D** (wrong): Copies drift, and pasting isn't a command.

### Question 35 · Multiple choice

A rule file, .claude/rules/migrations.md, should load only when Claude works on files under db/migrations/. What does the file need?

- **A.** YAML frontmatter with a paths field holding a glob such as db/migrations/**/*.sql.
- **B.** To be moved into db/migrations/.claude/rules/.
- **C.** An @import line in the root CLAUDE.md with the folder name after it.
- **D.** A first heading that reads "Applies to db/migrations".

**Answer: A** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.3 · Lesson 5.3

- **A** (right): Path-scoped rules load only when Claude touches a matching file.
- **B** (wrong): Rules are discovered in the project's .claude/rules/, scoped by their paths field.
- **C** (wrong): Imports always load; they have no condition.
- **D** (wrong): Headings are content; they don't scope loading.

### Question 36 · Multiple choice

A migration script generated in CI has three problems: a wrong column name, a missing index, and a default value that only makes sense once the column is renamed. How should the developer give Claude the feedback?

- **A.** In one message that covers all three, since the default depends on the rename.
- **B.** Ask for a fresh script from scratch, without mentioning the problems.
- **C.** Fix the column name by hand, and leave the other two for review.
- **D.** One problem per message, waiting for each fix before naming the next.

**Answer: A** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.5 · Lesson 5.6

- **A** (right): Interacting problems are solved together, so each fix accounts for the others.
- **B** (wrong): A new attempt can repeat or move the same mistakes.
- **C** (wrong): The known problems stay in the script.
- **D** (wrong): The default would be fixed against the old name, then broken again by the rename.

### Question 37 · Multiple response

A CI script posts each finding as an inline comment, so it needs the file and line, and it must reject malformed output. Which two belong in the setup? (Choose two.)

- **A.** A regular expression that extracts findings from a Markdown table in the text output.
- **B.** --output-format stream-json, posting each event as a comment.
- **C.** A sentence in the prompt asking Claude to respond in JSON.
- **D.** A --json-schema for findings with required file, line, severity and message fields.
- **E.** --output-format json, with the script reading the findings from the result's structured_output field.

**Answer: D and E** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.6 · Lesson 6.1

- **A** (wrong): Fragile: any change in the table's wording breaks the parse.
- **B** (wrong): Events aren't findings; the stream carries every step of the run.
- **C** (wrong): A request is not a guarantee, and nothing checks the shape.
- **D** (right): The output must match the schema, so every finding has what the script needs.
- **E** (right): The script reads data, not prose.

### Question 38 · Multiple choice

Developers have stopped reading the CI reviewer's comments: about half the files get remarks about naming, although its instructions ask for important issues only. What should the team change?

- **A.** Lower the temperature, so the reviewer's choices are more consistent.
- **B.** Let it post every comment, and have developers resolve what they don't need.
- **C.** Repeat "only important issues" in capital letters at the top of the prompt.
- **D.** State exactly what to report, such as bugs and security flaws, and what to skip, such as naming.

**Answer: D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.1 · Lesson 6.3

- **A** (wrong): It would make the same vague judgment, only more consistently.
- **B** (wrong): The noise stays, and developers keep ignoring the real findings.
- **C** (wrong): Louder wording is still the same vague instruction.
- **D** (right): An explicit list of what counts gives the reviewer a test it can apply to each finding.

### Question 39 · Multiple choice

Findings in five categories are mostly right, but the performance category is wrong about 70% of the time, and developers have started ignoring every comment. What should the team do first?

- **A.** Raise the minimum confidence for every category.
- **B.** Keep every category, and add a note to each comment saying some may be wrong.
- **C.** Turn the whole reviewer off until all categories are perfect.
- **D.** Switch off the performance category while its criteria are fixed; keep the accurate ones running.

**Answer: D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.1 · Lesson 6.3

- **A** (wrong): The accurate categories lose findings, and performance's problem is its criteria.
- **B** (wrong): The noise stays, and the note gives developers another reason to skip comments.
- **C** (wrong): It throws away four categories that already work.
- **D** (right): Trust returns quickly because the noisy category stops, and the useful ones stay.

### Question 40 · Multiple choice

For the CI reviewer's few-shot examples, what does the guidance favor?

- **A.** A few examples of ambiguous cases, each showing why its answer beats the alternative.
- **B.** One long example of a perfect review covering a whole pull request.
- **C.** As many examples as will fit, all of them clear-cut cases.
- **D.** Examples only of the output format, with no reasoning shown.

**Answer: A** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.2 · Lesson 6.4

- **A** (right): Targeted examples teach the judgment that the instructions alone leave open.
- **B** (wrong): A single example invites copying, not generalizing.
- **C** (wrong): Clear cases add tokens without teaching the hard calls.
- **D** (wrong): Format alone doesn't help with ambiguous judgments.

### Question 41 · Multiple choice

The reviewer's JSON schema types severity as a free string. Values come back as High, high, critical and P1, and the dashboard can't count them. What is the best fix?

- **A.** Normalize the values in the dashboard with a growing lookup table.
- **B.** Make severity an enum in the schema, with each allowed value defined in the prompt.
- **C.** Drop severity from the schema and sort by line count.
- **D.** Ask in the prompt for severity always in lowercase.

**Answer: B** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.3 · Lesson 7.2

- **A** (wrong): Each new spelling breaks the count until someone adds it.
- **B** (right): The schema then admits only the defined values, and the definitions say which to pick.
- **C** (wrong): Line count isn't risk.
- **D** (wrong): Case is the smallest part of the problem; critical and P1 remain.

### Question 42 · Multiple response

Which two jobs suit the Message Batches API? (Choose two.)

- **A.** An interactive debugging session with an engineer.
- **B.** A weekly audit of 2,000 files whose report is read on Monday.
- **C.** An agent loop that calls repository tools in the middle of each request.
- **D.** Generating missing docstrings for the whole repository overnight.
- **E.** The pre-merge check a developer waits on before merging.

**Answer: B and D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.5 · Lesson 7.5

- **A** (wrong): Each turn needs an answer now.
- **B** (right): Nobody waits on it, so the lower price is free.
- **C** (wrong): Batch requests are single-shot; tools can't be executed mid-request.
- **D** (right): Latency-tolerant work, finished before anyone needs it.
- **E** (wrong): A batch can take up to 24 hours; the developer is blocked.

### Question 43 · Multiple choice

About one review in fifty comes back with a finding that fails the team's own checks: a line number outside the file. What should the CI step do with such a finding?

- **A.** Retry the same request a few more times, with no extra context added.
- **B.** Rerun the whole review from the start until every one of its findings passes.
- **C.** Post the finding anyway, at the closest valid line in the diff.
- **D.** Retry once with the diff, the failed finding and its specific error; drop it if that fails.

**Answer: D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.4 · Lesson 7.3

- **A** (wrong): Without the error, the same mistake is likely again.
- **B** (wrong): Expensive, and nothing tells the model what was wrong.
- **C** (wrong): The comment lands on a line the finding wasn't about.
- **D** (right): The model gets what it needs to correct the reading, and a cap keeps it from looping.

### Question 44 · Multiple response

A CI job checks out the repository and runs claude -p from its root. Which two sources of memory does that run use? (Choose two.)

- **A.** The CLAUDE.md committed at the repository root.
- **B.** A CLAUDE.md in a subdirectory, once Claude reads files in that directory.
- **C.** CLAUDE.local.md files kept by developers in their own clones.
- **D.** The ~/.claude/CLAUDE.md on a developer's own machine.
- **E.** The README.md at the root of the repository.

**Answer: A and B** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.1 · Lesson 5.2

- **A** (right): It is in the checkout and loads at launch.
- **B** (right): Subdirectory memory loads on demand as Claude works there.
- **C** (wrong): Those are personal and aren't committed, so the checkout doesn't have them.
- **D** (wrong): It lives on that developer's machine, not on the runner.
- **E** (wrong): README.md isn't loaded as memory.

### Question 45 · Multiple choice

In CI, Claude fixes a failing test, but its fixes often pass that one test while breaking others in the suite. What should the job give Claude?

- **A.** A higher max_turns, so Claude can make more attempts at the one test.
- **B.** The full suite's command, with each run's failures fed back until the whole suite passes.
- **C.** A note asking Claude not to change unrelated code.
- **D.** Only the failing test, so Claude stays focused on it.

**Answer: B** · Domain 3 (Claude Code Configuration & Workflows) · Task Statement 3.5 · Lesson 5.6

- **A** (wrong): More attempts at one test still never check the rest.
- **B** (right): Every iteration sees all the tests, so a fix can't trade one failure for another.
- **C** (wrong): It can't see what it breaks without running the other tests.
- **D** (wrong): That is the setup that hides the other breakages.


## Part 4: Scenario 6, Structured Data Extraction · questions 46–60

> Structured data extraction. You are building a system that extracts information from unstructured documents with Claude, validates the output against JSON schemas and feeds downstream systems. It must stay accurate and handle edge cases gracefully.

### Question 46 · Multiple choice

A pipeline receives receipts, invoices and contracts of unknown type, with one extraction tool per type. Every response must be structured data from one of those tools, and Claude should pick which. How should tool_choice be set?

- **A.** The invoice extraction tool, by name.
- **B.** any, so Claude must call one of the tools and chooses which.
- **C.** auto, the default, which lets Claude answer in text.
- **D.** none, with the schemas described in the prompt.

**Answer: B** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.3 · Lesson 7.1

- **A** (wrong): Every document would be extracted as an invoice.
- **B** (right): It guarantees a tool call while leaving the choice of tool to Claude.
- **C** (wrong): Claude may answer in plain text instead of calling a tool.
- **D** (wrong): No tool is called, so no structured data comes back.

### Question 47 · Multiple response

Strict tool use is enabled on the extraction tool. Which two errors can still reach the records? (Choose two.)

- **A.** A string where the schema requires a number.
- **B.** A stated total that doesn't equal the sum of the line items.
- **C.** A property that the schema doesn't define.
- **D.** A delivery date placed in the invoice date field.
- **E.** A required field missing from the record.

**Answer: B and D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.3 · Lesson 7.1

- **A** (wrong): Types are enforced by the schema.
- **B** (right): The schema governs shape, not arithmetic between fields.
- **C** (wrong): Extra properties are rejected when the schema forbids them.
- **D** (right): Both are valid dates, so the shape is correct while the meaning is wrong.
- **E** (wrong): Strict tool use guarantees required fields are present.

### Question 48 · Multiple choice

Some suppliers print a total that disagrees with their own line items. The finance team needs both to be caught and to keep what the document actually says. What should the extraction do?

- **A.** Retry the extraction until the two totals finally match.
- **B.** Tell Claude to correct the stated total so that it matches the line items.
- **C.** Extract both the stated and a calculated total, flag a mismatch, and send it to review.
- **D.** Make the schema reject any record in which the two totals differ.

**Answer: C** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.4 · Lesson 7.3

- **A** (wrong): The document won't change, so the retries fail or invite a made-up value.
- **B** (wrong): The record then shows a total the document never stated.
- **C** (right): The record keeps the document's value, and the mismatch is visible instead of hidden.
- **D** (wrong): Those invoices can never be recorded, and their real values are lost.

### Question 49 · Multiple response

On a European invoice the date 03/04/2026 comes back as March 4, and the team's validator flags it because the invoice's own footer says it was issued in April. Which two should the retry request include? (Choose two.)

- **A.** A higher temperature, so the next attempt differs.
- **B.** Only the error message, to keep the request short.
- **C.** The original document that was extracted.
- **D.** The failed extraction with the validator's specific error.
- **E.** An instruction to be more careful with dates.

**Answer: C and D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.4 · Lesson 7.3

- **A** (wrong): Randomness isn't a correction.
- **B** (wrong): Without the document there's nothing to re-read.
- **C** (right): The model needs the source to read the date again.
- **D** (right): It says exactly what was wrong and why.
- **E** (wrong): Vague; it doesn't say what was wrong.

### Question 50 · Multiple choice

The prompt says to extract only "relevant" line items. Reviewers find shipping, discounts and deposits included on some invoices and left out on others. What should change?

- **A.** Set temperature to 0 for all the extraction calls in the job.
- **B.** Ask Claude for a confidence score on every line it extracts.
- **C.** Tell Claude to be more careful about which lines are relevant.
- **D.** Define which lines count as items, and where shipping, discounts and deposits go.

**Answer: D** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.1 · Lesson 6.3

- **A** (wrong): The same unclear rule is then applied consistently wrong.
- **B** (wrong): Confidence doesn't say whether shipping is an item.
- **C** (wrong): Care doesn't define what relevant means.
- **D** (right): Explicit criteria remove the guesswork that "relevant" leaves.

### Question 51 · Multiple choice

A purchasing team posts supplier records to its ledger, and an audit rule says each must be there no later than eight hours after the document comes in. Documents come in around the clock. To cut cost, someone proposes moving extraction to the Message Batches API. What should they do?

- **A.** Use regular synchronous calls for this pipeline, because a batch can take up to 24 hours.
- **B.** Keep batches small, since small batches always finish within an hour.
- **C.** Batch everything and post late records to the ledger the next day.
- **D.** Submit a batch every hour, so no document waits long to be sent.

**Answer: A** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.5 · Lesson 7.5

- **A** (right): Batches have no latency guarantee shorter than 24 hours, so an eight-hour deadline can't depend on them.
- **B** (wrong): Most finish fast, but none is guaranteed to.
- **C** (wrong): It breaks the eight-hour requirement.
- **D** (wrong): Each batch can still take up to 24 hours to finish.

### Question 52 · Multiple choice

The schema's payment_method is an enum of card, bank_transfer and cash. Some documents say cheque, and some say nothing at all; in both cases records come back with bank_transfer. What should the team change?

- **A.** Remove the enum, and accept any free text in the field.
- **B.** Add cheque to the enum, and keep the field required as before.
- **C.** Add other with a payment_method_detail field, and make the field nullable.
- **D.** Tell Claude to choose whichever enum value is the closest match.

**Answer: C** · Domain 4 (Prompt Engineering & Structured Output) · Task Statement 4.3 · Lesson 7.2

- **A** (wrong): Values become inconsistent for every downstream system.
- **B** (wrong): Silent documents still have to pick something.
- **C** (right): The schema can then express both cases without forcing a wrong value.
- **D** (wrong): The closest value is still wrong.

### Question 53 · Multiple choice

Only the fields that Claude scores below 0.8 reach a reviewer. When the team audited a random sample of fields scored 0.9, one in five turned out to be wrong. What should the team do?

- **A.** Stop using confidence at all, and send every record to review.
- **B.** Measure accuracy against confidence on labeled data, per field, and set thresholds from it.
- **C.** Ask the model to be stricter whenever it assigns a confidence score.
- **D.** Raise the routing threshold to 0.95 for every field at once.

**Answer: B** · Domain 5 (Context Management & Reliability) · Task Statement 5.5 · Lesson 7.6

- **A** (wrong): It discards a signal that calibration can make useful.
- **B** (right): The thresholds then reflect how often each confidence level is actually right.
- **C** (wrong): Self-scoring stays uncalibrated.
- **D** (wrong): A guess at a new number, still not tied to measured accuracy.

### Question 54 · Multiple choice

Auditors must be able to check every extracted value against its source document quickly. What should the record hold?

- **A.** One overall confidence score for the record.
- **B.** For each field, the page and a short quote from where the value came.
- **C.** A summary of the document in two sentences.
- **D.** The full text of the document, attached to the record.

**Answer: B** · Domain 5 (Context Management & Reliability) · Task Statement 5.6 · Lesson 4.7

- **A** (wrong): It doesn't say where any value came from.
- **B** (right): Each value can be traced back to its evidence in seconds.
- **C** (wrong): A summary loses the link between each value and its source.
- **D** (wrong): Auditors still have to search it for every value.

### Question 55 · Multiple choice

The nightly run over 5,000 documents aborts completely when a single file can't be parsed, and nothing reaches the ledger that night. What should change?

- **A.** Stop the run on any failure, and alert on-call to fix it by morning.
- **B.** Retry each failed file over and over until it finally parses.
- **C.** Log each failure with its cause, process the rest, and report what wasn't covered.
- **D.** Skip failed documents silently, so the run always completes.

**Answer: C** · Domain 5 (Context Management & Reliability) · Task Statement 5.3 · Lesson 4.6

- **A** (wrong): That is what's happening now: everything waits on one file.
- **B** (wrong): A corrupt file never parses, so the run stalls.
- **C** (right): One bad file costs one record, and the gap is still visible.
- **D** (wrong): The missing records go unnoticed downstream.

### Question 56 · Multiple response

Before reducing human review of high-confidence extractions, which two should the team have in place? (Choose two.)

- **A.** The model's self-reported confidence on its own.
- **B.** Accuracy measured per document type and per field, on labeled data.
- **C.** The overall accuracy across all documents.
- **D.** Ongoing random checks of high-confidence records, sampled within each document type.
- **E.** Review of the records customers complain about.

**Answer: B and D** · Domain 5 (Context Management & Reliability) · Task Statement 5.5 · Lesson 7.6

- **A** (wrong): Uncalibrated, and blind to confident errors.
- **B** (right): An average can hide a weak type or field.
- **C** (wrong): A high average can hide one type that fails often.
- **D** (right): It catches errors that confidence misses, and drift over time.
- **E** (wrong): Most wrong records never cause a complaint.

### Question 57 · Multiple choice

Some invoices show two dates with no labels, and the schema needs an invoice_date. What should the extraction do when it can't tell which date is meant?

- **A.** Use the later of the two dates, as the more recent one.
- **B.** Return invoice_date as unclear, note both dates, and send the record to review.
- **C.** Use the earlier of the two dates, as the likelier issue date.
- **D.** Leave invoice_date empty, with no note about why it's missing.

**Answer: B** · Domain 5 (Context Management & Reliability) · Task Statement 5.2 · Lesson 3.5

- **A** (wrong): Wrong whenever the later date is the due date.
- **B** (right): A person resolves the ambiguity instead of the record carrying a guess.
- **C** (wrong): A rule of thumb that is wrong whenever the earlier date is the order date.
- **D** (wrong): Nothing tells a reviewer why it's empty or what was found.

### Question 58 · Multiple choice

When fields are extracted from a 180-page contract in one request, values on the middle pages are missed far more often than those near the start or the end. What should the team do?

- **A.** Raise max_tokens so the response has room for every field.
- **B.** Ask Claude to read the middle pages more carefully.
- **C.** Extract section by section, then merge the results, keeping each value's page.
- **D.** Move the contract's middle pages to the start of the request.

**Answer: C** · Domain 5 (Context Management & Reliability) · Task Statement 5.1 · Lesson 3.7

- **A** (wrong): That allows a longer answer, not a better reading of the input.
- **B** (wrong): Attention to the middle of long inputs is the limitation itself.
- **C** (right): Each pass gives its section full attention, and the merge keeps provenance.
- **D** (wrong): The pages now at the middle are missed instead.

### Question 59 · Multiple choice

fetch_document fails for two reasons: some supplier portals deny access until a person grants it, and others time out now and then. Today the agent retries both until the run's limit. What should the tool return?

- **A.** An empty document for both, so the run continues.
- **B.** The same generic error for both, with a longer timeout.
- **C.** A retryable error for both cases, with a longer wait between attempts.
- **D.** A permission error, not retryable, for denials; a transient, retryable error for timeouts.

**Answer: D** · Domain 5 (Context Management & Reliability) · Task Statement 5.3 · Lesson 4.6

- **A** (wrong): Failures look like documents with no content.
- **B** (wrong): The agent still can't tell which failure will clear on its own.
- **C** (wrong): Access-denied portals never open on their own, so the retries are wasted.
- **D** (right): The agent then retries only what can succeed, and reports what needs a person.

### Question 60 · Multiple choice

A lease lists the renewal date as 1 March 2027 in its main text, and as 1 April 2027 in an amendment on page 9. The schema has one renewal_date field. What should the extraction do?

- **A.** Keep both dates with their pages and context, flag the conflict, and send it to review.
- **B.** Keep the amendment's date, since amendments always override the main text.
- **C.** Keep the date from the main text, since it appears first in the lease.
- **D.** Average the two dates, and keep the midpoint as the renewal date.

**Answer: A** · Domain 5 (Context Management & Reliability) · Task Statement 5.6 · Lesson 4.7

- **A** (right): The conflict stays visible with its evidence, and a person decides which one governs.
- **B** (wrong): That's a legal judgment the extraction can't make reliably.
- **C** (wrong): The amendment may override it, and the record hides that.
- **D** (wrong): The result is a date neither text states.
