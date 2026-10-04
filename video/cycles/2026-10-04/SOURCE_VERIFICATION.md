# Source Verification — 2026-10-04

This supplements the accepted research packet; it preserves the approved topics, hooks and cautious framing.

## ECG paper

The publisher's full accepted PDF is retained at `build/video/2026-10-04/research/ecg.pdf`, with extracted text at `ecg.txt`. DOI: 10.1038/s44325-026-00153-2. Published 2 October, accepted 19 September 2026. Authors: Viktor van der Valk, Douwe Atsma, Roderick Scherptong and Marius Staring.

Methods describe historical acute-coronary-syndrome patients from 2018–2023, including actual home ECG recordings with Withings smartwatches. The raw one-lead population was 708 patients / 63,950 recordings. After matched labelling and quality filtering, 460 patients / 5,480 recordings remained; 77.6% were male. The 12-lead set had 1,856 patients / 7,197 recordings; shared test evaluation involved 144 patients. Patient-level splitting avoids mixing a patient's recordings between training and test sets.

AUC 0.883 belongs to the pretrained one-lead model; the one-lead model without pretraining scored 0.863, and the 12-lead model 0.897. AUC is discrimination across thresholds, not percent diagnostic accuracy. The work is retrospective and single-centre, without independent external prospective outcome validation. Recording quality is a substantial limitation. No claim that a watch replaces imaging or improves outcomes is made. The four selected paper figures are CC BY 4.0 and have no conflicting per-figure third-party credit.

## AI discharge-summary paper

The full accepted PDF/text are retained at `build/video/2026-10-04/research/ai.pdf` and `ai.txt`. DOI: 10.1038/s41746-026-03320-y. Published 2 October, accepted 16 September 2026. First author Tyler Osborne; Stony Brook-led.

Sixty internal-medicine encounters lasting 7–21 days were sampled from January 2023–December 2024. Twelve reviewers (six hospitalists, six primary-care physicians) assessed the paired summaries; each encounter received two reviews. GPT-5.2 (2025-12-11 snapshot) summaries were produced in March 2026 through a private HIPAA-compliant Azure deployment. Reviewers were unblinded. They preferred AI summaries in 57/60 encounters (95%). Fewer omissions drove the annotation improvement; estimated harm measures did not differ significantly. It is a single-hospital retrospective clinician evaluation, not a patient-outcomes trial. The CC BY-NC-ND artwork is not used.

## Event dates and media

ESA's 2 October report concerns September 2026 testing. The authenticated position demonstration occurred 16 September and was already reported 17 September. Selected recorded ESA footage explicitly documents September 2025. NASA's 2 October report concerns summer 2026 INSPYRE measurements, including the 26 August Wildhorse encounter in Idaho; warning/model improvements are goals. Selected NASA media credits and exclusions are in `CREDITS.md` and `MEDIA_AUDIT.md`.

Clinical background references: [NHS ECG](https://www.nhs.uk/tests-and-treatments/electrocardiogram/), [American Heart Association ejection fraction](https://www.heart.org/en/health-topics/heart-failure/diagnosing-heart-failure/ejection-fraction-heart-failure-measurement). These support the electrical-recording versus pumping-function explanation, not the new study's performance claim.
