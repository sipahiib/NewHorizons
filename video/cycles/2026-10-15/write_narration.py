"""Approved English narration; proposal IDs are distinct from output order."""
from pathlib import Path
import json
C=Path(__file__).resolve().parent
sections=[
('opening_hook',5,"NASA tested tiny batteries at minus eighty degrees Celsius."),
('opening_support',7,"NASA recreates space conditions in thermal-vacuum chambers like this one."),
('opening_teaser',4,"Then, mutations make RNA droplets move."),
('nasa_body',None,"""The project is called SPEARS. NASA researchers are developing solid-state batteries for equipment that may one day work on the Moon. The key change is inside the cell. Instead of a liquid electrolyte, which carries charge between the electrodes, these prototypes use a solid ceramic or polymer material.

Why does that matter? Space equipment faces more than a cold winter morning. It must cope with a vacuum and large changes in temperature. A battery has to survive those conditions and supply useful power when needed. Those are two different tests.

NASA reports that small prototype cells worked during thermal-vacuum testing from minus sixty to eighty degrees Celsius, with reduced performance at minus eighty. In a separate test, the cells survived exposure down to minus one hundred and seventy degrees without damage. They did not operate at that temperature. Heaters would still be needed to warm them before use.

The moving footage here shows other NASA thermal-vacuum facilities and testing work. It illustrates the process, rather than showing the SPEARS battery experiment. The photographs show the actual project and its researchers.

A battery that tolerates deep cold before warming could reduce the need to keep equipment heated continuously. But that is a potential engineering benefit. These are small prototypes, and NASA is still developing hardware for future space tests. The announcement does not establish a flight-ready power system, a consumer product, or a proven improvement in electric-car range.

For now, the useful lesson is straightforward. In extreme environments, surviving the cold and working in the cold are separate achievements. SPEARS is investigating both."""),
('rna',None,"""A few genetic changes made these RNA droplets move.

Researchers in Heidelberg, working with colleagues at the German Cancer Research Center and the University of Augsburg, studied tiny structures assembled from synthetic RNA. These droplets are laboratory models for some features of cells. They are not newly created living organisms.

RNA is made from a DNA template. In this experiment, the droplets could hold that template inside them, linking genetic information to the structure it produces. The researchers then introduced mutations into the template and watched what changed.

Instead of simply falling apart, some droplets developed internal cavities called vacuoles. Those compartments remained stable for days. In the experimental time-lapse microscopy shown here, the cavities change the way material is arranged inside the droplets. That internal activity is associated with tiny movements over distances measured in micrometres.

The mutated droplets moved farther than their unmutated counterparts. More encounters could lead them to merge and grow. The cavities could also collect small molecules, giving the droplets internal storage spaces.

That connects a change in genetic instructions to a new physical structure, and then to a new function. It gives scientists a simple system for asking how useful properties might emerge from molecular changes.

The university announced the findings on October thirteenth. The peer-reviewed paper appeared on October seventh, so the announcement is newer than the underlying publication.

There are important limits. The study does not show a complete living cell, autonomous reproduction, or a medical treatment. Movement is not evidence that the droplets choose where to go. Future immune-related applications are a research ambition.

What the experiment offers today is a way to investigate how genetic variation can change the behaviour of simple molecular compartments."""),
('closing',10,"That was our latest news. Stay with science, and stay tuned."),
('r1',45,"""AI is making detailed storm simulations cheaper to run. Ai2's new HiRO-ACE version two turns coarse climate output into three-kilometre rain, wind and pressure fields. These images are simulated weather, not recorded storms. In the researchers' benchmark, generating the detailed data used roughly three hundred times less inference computation than the reference model. That could help scientists explore more extreme-weather scenarios. But this is a preprint evaluated against a simulation. It does not prove better daily forecasts, and the current system cannot yet generate these detailed outputs for warmer future climates."""),
('r2',45,"""El Niño was not the only force strengthening Hurricane Polo. A new World Weather Attribution analysis finds human-caused warming influenced its intensity at least as strongly. The storm happened in September; the new development is the attribution study. Here, satellite images and satellite-derived rainfall visualizations show Polo's structure. They do not prove how much warming changed its rainfall. The researchers could not quantify that contribution because the climate models did not reproduce observed rainfall trends. The practical lesson is to prepare for more than coastal wind: flooding can threaten communities well inland, even after a hurricane weakens.""")]
data=dict(cycle=C.name,voice='en-GB-RyanNeural',rate='-2%',sections=[dict(id=id,target=target,text=text) for id,target,text in sections])
(C/'narration.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print([(s['id'],len(s['text'].split())) for s in data['sections']])
