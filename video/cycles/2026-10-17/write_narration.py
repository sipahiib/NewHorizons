from pathlib import Path
import json
C=Path(__file__).resolve().parent
sections=[
('opening_hook',5,'AI is stepping into the lab.'),
('opening_support',7,'Google is testing agents that plan experiments and learn from real measurements.'),
('opening_question',4,'But who checks their work?'),
('body',None,'''These laboratory scenes illustrate the tools and procedures involved. They are not recordings of Google's experiments.

On October sixteenth, Google Research presented three projects exploring how artificial intelligence could become a more useful partner at the laboratory bench. The connection between them is experimental feedback: propose an idea, test it, examine what actually happened, and revise the next attempt.

That sounds straightforward. But a laboratory is much less forgiving than a text window. A computer program can be perfectly valid and still tell a robot to do something impossible. A pipette might not fit into a container. A well might be empty. Or a liquid might not mix as expected, quietly distorting the result.

Google's first project, called VERID, is designed to bridge that gap. It keeps a live digital record of the equipment, the liquids and the available pipette tips. Before commands reach the robot, they pass through a simulated run. The system checks physical constraints and tracks what has already happened.

The team's demonstrations used dyes and water to test these foundations. In one case, a planned action would not fit the equipment, so the agent had to replan. In another, saved state helped it recover after a measurement device failed, without repeating the liquid transfers. These are useful examples of error handling. They do not show that every possible mistake can be prevented.

The second project asks a different question: can experimental results help an agent design better molecules?

The researchers worked with aptamers, short strands of DNA that can fold into shapes capable of binding to proteins. Across three rounds of design and testing, agents received laboratory measurements and revised their candidates.

One attempt exposed a revealing problem. The molecules appeared to bind strongly, but many were simply sticky. They attached to unwanted targets and even to the beads used in the test. Chasing the strongest-looking signal had led the search in the wrong direction. With those measurements, the agents changed their design strategy and improved the next round's selectivity. The agent setup also changed between rounds, so this was not a controlled test of feedback alone.

A third project explored protein design, combining human guidance with agent-driven search and laboratory checks. It produced binders for a protein associated with solid tumours. Binding a target, however, is only an early research step. It does not demonstrate a safe or effective cancer treatment.

There are other limits. These are results reported by the team that built the systems. The projects are separate building blocks, and bringing them together remains future work. People still approve molecular designs, check protocols and supervise robot runs.

For viewers, the important change is the direction of travel. AI research is moving beyond generating plausible answers towards testing ideas against the physical world. That could help scientists explore more possibilities. But the useful measure of progress is not how confidently an agent speaks. It is whether a carefully checked experiment supports what it claims.'''),
('closing',10,'That was our latest news. Stay with science, and stay tuned.')]
(C/'narration.json').write_text(json.dumps(dict(cycle=C.name,voice='en-GB-RyanNeural',rate='-2%',sections=[dict(id=i,target=t,text=s) for i,t,s in sections]),indent=2)+'\n')
print([(i,len(s.split())) for i,t,s in sections])
