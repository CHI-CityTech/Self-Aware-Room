# Self-Aware Room Research Framework

## Purpose

Research documentation identifies the questions the Self-Aware Room (SAR) is designed to investigate. Technical documentation elsewhere in the repository describes the systems, components, interfaces, and implementations used to investigate those questions.

This research layer organizes questions, hypotheses, theoretical frameworks, avenues of inquiry, evidence needs, and connections to experiments. It does not replace or duplicate detailed technical specifications. The framework is intended to remain useful as hardware, software, models, and funded projects change.

## Central Inquiry

> **What does it mean to collaborate with machine intelligence?**

This is the overarching SAR inquiry. SAR treats collaboration as an open research problem rather than assuming that sensing, automation, or fluent language is sufficient to establish collaboration.

A related proposition is:

> **When can the learning environment itself become a collaborator, and what happens to human agency, ethics, control, and authority when it does?**

**When the Classroom Itself Becomes a Collaborator** is therefore a significant cross-cutting research proposition within SAR, not a replacement for the broader central question.

## SAR as a Research Testbed

SAR is both an engineered system and a research instrument. Its architecture provides capabilities for sensing, correlation, semantic interpretation, policy evaluation, orchestration, response, and observability. Experiments use those capabilities to generate evidence about environmental intelligence, collaboration, learning, governance, and mediation.

The system should be evaluated by what it makes possible for human participants to learn, question, create, and decide, not only by whether it can produce technically successful outputs.

## Avenues of Inquiry

### AOI-01 - Environmental Agency and Collaboration

**Core question:** Under what conditions can an intelligent learning environment meaningfully be considered a collaborator rather than merely a responsive or automated system?

This avenue examines degrees of participation among sensing, perception, inference, semantic interpretation, response, feedback, and adaptation. It distinguishes computational agency from human agency and asks what, if anything, makes environmental participation collaborative. Automation or sensor coverage alone does not establish collaboration.

Relevant evidence includes the quality and timing of environmental responses, participant interpretation of those responses, opportunities for feedback and revision, and whether the system supports or constrains human initiative.

Related technical documentation includes the [computational pipeline](../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md), the [computational glossary](../computational/D00.02_SAR_Computational_Glossary_V1_2026-07-29.md), and the [architecture orientation](../architecture/README.md).

### AOI-02 - Ethics, Agency, Control, and Authority

**Core question:** What forms of agency can be delegated to an intelligent environment, and what forms of control and authority should remain with human participants?

SAR should treat agency, control, and authority as related but distinct. **Agency does not necessarily imply authority.** A computational system may be permitted to sense, infer, recommend, or act while humans retain authority over goals, boundaries, interpretation, and consequential decisions.

The EDOCA dimensions provide an evaluative framework for this avenue:

- **Effort:** What work is reduced, displaced, or newly required?
- **Distortion:** What is lost, transformed, or misrepresented through mediation?
- **Observability:** What can participants inspect, reconstruct, and question?
- **Control:** Who can constrain, revise, pause, or override system behavior?
- **Authority:** Who is entitled to set goals, interpret outcomes, and make consequential decisions?

EDOCA is introduced here as a research framework for evaluating systems; it is not presented as a completed governance specification. Evidence should include provenance, uncertainty, policy decisions, no-action outcomes, human review, override paths, and participant experience.

The [computational pipeline](../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md) separates interpretation from authorization and makes observability, policy, permissions, and human review relevant to this inquiry.

### AOI-03 - Mediation and Balanced Blended Space

**Core question:** How does information, agency, and meaning move among physical, virtual, computational, cognitive, and conceptual participants within SAR?

This avenue investigates the Balanced Blended Space (BBS) framework already present in the architecture documentation. BBS links physical, virtual, and conceptual spaces, and considers relationships between cognitive and computational intelligence. The architecture's mediation syntax provides a way to examine source, vector, destination, temporal relationships, spatial relationships, and transformation across boundaries.

The research question is not whether the spaces are simply connected, but how mediation changes what can be perceived, understood, expressed, and acted upon. This README does not reproduce the BBS specification; the [canonical architecture framework](../architecture/Self-Aware%20Room%20-%20Technical%20Framework%20%26%20System%20Architecture.md) remains the appropriate source for that detail.

### AOI-04 - Multimodal Perception and Environmental Understanding

**Core question:** What does it mean for a computational environment to develop a meaningful representation of itself, its occupants, and ongoing activity?

SAR uses "self-aware" in an operational sense: computational environmental awareness and representation, not a claim about machine consciousness. The research progression should remain explicit:

1. **Sensing** - acquiring observations from instruments and software sources.
2. **Detection** - identifying events, entities, or changes.
3. **Correlation** - associating observations across time, space, and sources.
4. **Multimodal coherence** - evaluating whether observations can form a consistent state model.
5. **Semantic interpretation** - assigning meaning or structure to coherent evidence.
6. **Inference** - deriving possibilities, context, or predictions with uncertainty.
7. **Environmental response** - selecting, authorizing, and observing an action or no-action outcome.

This avenue examines how audio, computer vision, depth and spatial sensing, gesture, presence, environmental telemetry, and semantic processing combine. It asks when additional modalities improve understanding and when they introduce contradiction, distortion, privacy cost, or unjustified confidence.

The [sensor inventory and computational mapping](../sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md) and [computational pipeline](../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md) describe the implementation surfaces without settling the research questions.

### AOI-05 - Distributed, Localized, and Personalized Intelligence

**Core question:** How does an intelligent environment change when computational intelligence is distributed among smaller, specialized, local, or personalized models rather than concentrated entirely in large centralized models?

This avenue investigates the tradeoffs among privacy, latency, specialization, personalization, data locality, observability, system control, institutional authority, and individual authority. Existing local-model documentation describes dedicated local GPU infrastructure, localized LLM research, and personalized agent roles. These are research and architectural directions, not evidence that local deployment alone guarantees privacy, governance, or FERPA compliance.

The repository's Arc of Engineering can be treated as a hypothesis:

```text
emergence
    |
centralized
    |
hybrid
    |
distributed
    |
ubiquitous
```

> If AI follows technological patterns observed in other engineering domains, intelligent environments may increasingly combine centralized general-purpose models with distributed specialized and local computational systems.

SAR can investigate this hypothesis; it should not be read as an inevitable trajectory. Relevant evidence includes comparative latency and capability, data movement, failure modes, personalization effects, auditability, and who retains operational and institutional control.

### AOI-06 - Pedagogy and Human Learning

**Core question:** Under what conditions does environmental intelligence meaningfully improve learning, access, creativity, collaboration, or reflection?

This avenue keeps human purposes at the center of the research program. It asks whether adaptation improves learning, when automation removes unnecessary friction, when it removes meaningful intellectual effort, how different modes of participation are supported, and what new forms of collaboration become possible. It also asks which educational problems are actually being solved and how students can understand and critique the AI systems around them.

The executive materials connect SAR to the CUNY OAA AI Innovation project, AI literacy, OER, localized LLM research, and ethics education. Those connections support investigation of faculty development, experiential learning, bias, fairness, transparency, and accountability, while leaving the educational outcomes open to evidence.

## Relationship Among Research Areas

The avenues are coupled rather than sequential. Environmental agency intersects with multimodal understanding and mediation. Mediation raises questions about effort, distortion, observability, control, and authority. Distributed intelligence changes what can be observed and controlled. Pedagogy provides a human context for evaluating whether these capabilities matter, rather than a stage that follows them.

```text
                                                         CENTRAL INQUIRY
                      What does it mean to collaborate with machine intelligence?
                                                                              |
               +--------------------------+--------------------------+
               |             |             |             |             |
         AOI-01        AOI-02        AOI-03        AOI-04        AOI-05        AOI-06
       Environmental  Ethics /      Mediation &   Multimodal    Distributed  Pedagogy &
       Agency &       EDOCA         Balanced      Environmental / Localized  Human
       Collaboration               Blended Space Understanding Intelligence Learning
```

This is a conceptual map, not a causal or dependency model. The avenues are related lenses on the central inquiry. Ethics and EDOCA evaluate questions across the system; pedagogy provides a human context that can evaluate the significance of every avenue; and experiments may investigate one avenue or several at once.

## Research -> System -> Experiment -> Evidence

SAR research should use the following iterative relationship:

```text
Research Question
       |
Required Capability
       |
SAR Architecture / System
       |
Experiment
       |
Observation / Evidence
       |
Research Interpretation
       |
Refined Question or Hypothesis
```

An experiment may contribute evidence to more than one avenue. Existing experiments are currently concentrated on communications and video integration, and should not be assumed to answer semantic or pedagogical questions merely because they exercise system components. Future experiment reports may include a section such as:

```markdown
## Research Alignment

Related Avenue(s) of Inquiry:

- AOI-01 Environmental Agency and Collaboration
- AOI-04 Multimodal Perception and Environmental Understanding
```

The [experiments index](../../experiments/README.md) remains the canonical guide to experiment status, evidence, and promotion.

## Related Documentation

- [SAR documentation index](../README.md)
- [Executive Brief](../executive/01_Self-Aware%20Room%20-%20Executive%20Brief.md)
- [Architecture orientation](../architecture/README.md)
- [Technical Framework and System Architecture](../architecture/Self-Aware%20Room%20-%20Technical%20Framework%20%26%20System%20Architecture.md)
- [Computational documentation](../computational/README.md)
- [General Computational Pipeline Specification](../computational/D01.01_SAR_General_Computational_Pipeline_Spec_V1.1_2026-07-27.md)
- [Coherence, Correlation, and Integration Specification](../computational/D01.03_SAR_Coherence_Correlation_and_Integration_Detailed_Spec_V0_2026-07-28.md)
- [Sensor documentation](../sensors/README.md)
- [Sensor Inventory and Computational Mapping](../sensors/SAR_Sensor_Inventory_and_Computational_Mapping_V1_2026-08-03.md)
- [Summer 2026 roadmap](../roadmap_summer_2026.md)
- [Experiments index](../../experiments/README.md)

## Emerging Questions / Future Reconciliation

The research layer records questions that should be reconciled in later revisions rather than silently resolving them in historical or canonical documents:

- Some architecture and executive language may imply that human and computational agents are necessarily equal or symmetrical partners. BBS symmetry is a useful analytical relation, but it does not by itself establish equal agency, authority, or responsibility.
- Existing local-model language connects local deployment with privacy, governance, and FERPA compliance. Local processing may support those goals, but it does not by itself guarantee legal compliance, ethical adequacy, or institutional governance.
- Computational agency, autonomy, awareness, intelligence, and collaboration are used at different levels of abstraction across the repository. Future work should define their relationships and identify observable criteria.
- The coherence and integration specification remains incomplete. Temporal windows, association, contradiction handling, confidence aggregation, observability requirements, and validation scenarios remain research and implementation questions.
- The sensor inventory and runtime mapping are not yet fully populated. Claims about multimodal environmental understanding should therefore distinguish architectural capability from demonstrated evidence.
- Future experiments should make their research alignment, evidence limits, and implications for the avenues of inquiry explicit without turning every operational integration test into a claim about collaboration or learning.
