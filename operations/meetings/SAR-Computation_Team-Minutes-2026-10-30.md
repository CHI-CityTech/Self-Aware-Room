# Meeting Minutes – Self-Aware Room (SAR) Project

## Meeting Metadata

**Date:** 2026-10-30

**Time:** 18:32 – 19:09 (EST)

**Facilitator:** Professor David Smith

**Attendees:**

- Professor David Smith
- Kazi Tamim Nomany
- Kazi Rahimu Islam
- Kazi Tasin
- Dangol Sunima

## Meeting Overview

The team convened to review progress on the Self-Aware Room (SAR) project and establish next steps for implementation. The discussion centered on Kazi Tamim's proposals for sensor ID systems and class diagrams (issues #22, #23, #24), AI implementation strategy, and assignment of development tasks across the team. Key decisions included adopting a hybrid AI approach (local open-source models + commercial LLMs), developing abstract class libraries in Python for the L1-L5 computational pipeline, and establishing clear responsibilities for database exploration, class library development, and audio pipeline validation.

## Discussion Topics

### 1. Adjunct Position for Kazi Tasin

Professor Smith discussed the possibility of Kazi Tasin receiving an adjunct position at the department. The most likely courses would be CST1101, CST1102, or CST1000. Kazi Tasin reported discussions with Professor Milonas and Professor Marcos Pinto, with tentative positive feedback.

### 2. Project Repository Structure

Professor Smith confirmed that Kazi Tamim's three research proposals have been uploaded to the GitHub repository under `documents/research/nomani`. These proposals are now accessible to all team members and serve as the foundation for upcoming development work.

### 3. Sensor ID System Proposal (Issue #22)

Kazi Tamim presented a proposal for implementing permanent IDs for physical sensors using UUID v4. Key recommendations include:

- Each physical sensor receives a permanent ID
- Moving a sensor to another room retains the same ID
- Replacing a sensor generates a new ID
- Sensor IDs are separated from stream IDs
- One device can send multiple data streams, each with its own ID

Professor Smith emphasized the need for further formalization of the ID system and sensor classification requirements, including defining tagging methods and required data classes.

### 4. Class Diagram and Data Flow (Issue #23)

Kazi Tamim presented a UML class diagram outlining shared and specialized fields across different record types. The team discussed the need for a protocol to handle information flow through streams and packets, emphasizing the importance of simplifying the number of unique IDs required. The next step is to define generic object classes for different system layers (L1, L2, L3, L4, L5) to accommodate various sensors and processing pathways.

### 5. AI Implementation Strategy

Kazi Rahimu explained the team's hybrid approach to AI implementation:

- **Short-term:** Use both local open-source LLMs (e.g., DeepSeek 7B for reasoning, Gemma 4 for coding) and commercial LLMs (GPT, Claude) for complex tasks
- **Long-term goal:** Transition all operations to local models
- **Architecture:** Distributed AI system with 5-20 specialized expert models, each optimized for specific tasks

Professor Smith mentioned ongoing efforts through the AI Task Force to provide GPU access for students and plans to deploy local servers to host AI models.

### 6. Database Development

The team confirmed that a previous student's database work had ended. Kazi Tamim will present findings recommending MongoDB as the database solution. The immediate priority is not writing to the database but rather establishing data flow through the system, with interim solutions such as writing to flat files or serialized objects acceptable for testing purposes.

### 7. Development Language and Environment

The team confirmed Python as the primary development language for class libraries and computational pipeline implementation. All team members (Kazi Tamim, Kazi Rahimu, Dangol Sunima) expressed comfort with Python.

### 8. Grant Opportunities and Project Visibility

Kazi Tasin reported collaboration with Professor Wicksell on exploring the CUNY AI Innovation Grant with Professor Raj Korban at Hunter College. The team is seeking an angle to involve the Chi (Center of Holistic Integration) project. Additionally, Kazi Tasin and Kazi Tamim presented the SAR project at a conference in Albany, increasing project visibility. Professor Smith noted that searches for "Center of Holistic Integration" now return the project at the top of results.

## Action Items / GitHub Issues

### Issue: Convert Meeting Summary and Transcript into GitHub Issues

**Assignee:** David Smith

**Description:**

Convert the meeting summary and transcript from the 2026-10-30 SAR project meeting into formal GitHub issues. This includes creating issue tickets for all action items, research tasks, and development assignments discussed during the meeting.

**Acceptance Criteria:**

- All action items from meeting are represented as GitHub issues
- Each issue includes title, assignee, description, acceptance criteria, and labels
- Issues reference dependencies (e.g., #22, #23, #24) where applicable
- Meeting transcript and summary are archived in the repository

**Labels:** `documentation`, `admin`, `task`

**Dependencies:** None

---

### Issue: Mentor Students and Identify Database Contributors

**Assignee:** Kazi Rahimu Islam

**Description:**

Continue mentoring students involved in the SAR project through weekly or bi-weekly touchpoints. Actively identify and recruit students interested in contributing to database development work, particularly those with experience or interest in MongoDB or similar technologies.

**Acceptance Criteria:**

- Establish regular meeting schedule (weekly or bi-weekly) with mentored students
- Document student progress and interests in project tracking system
- Identify at least 1-2 candidates interested in database development
- Onboard database-interested students with relevant project documentation

**Labels:** `mentoring`, `recruitment`, `database`

**Dependencies:** None

---

### Issue: Explore CUNY AI Innovation Grant Opportunity

**Assignee:** Kazi Rahimu Islam

**Description:**

Collaborate with Professor Raj Korban at Hunter College (via Professor Wicksell) to explore opportunities for integrating the Chi/SAR project into the CUNY AI Innovation Grant. Identify specific angles, research questions, or technical components that align with grant objectives and could benefit from grant funding.

**Acceptance Criteria:**

- Schedule and complete initial meeting with Professor Wicksell and/or Professor Korban
- Document grant objectives and alignment opportunities with SAR project
- Prepare proposal outline or angle for Chi/SAR involvement
- Report findings and recommendations to Professor Smith

**Labels:** `grant`, `research`, `external-collaboration`

**Dependencies:** None

---

### Issue: Develop Basic Class Objects for Computational Pathway

**Assignee:** Kazi Tamim Nomany

**Description:**

Develop the foundational abstract class library for the SAR computational pathway in Python, based on proposals in issues #22, #23, and #24. These classes should define the structure for data flow through system layers L1-L5, accommodating various sensor types and processing requirements. Focus on creating generic, reusable class definitions that can be instantiated and extended as needed.

**Acceptance Criteria:**

- Create Python class definitions for abstract base classes representing system layers (L1, L2, L3, L4, L5)
- Define sensor ID and stream ID structures per issue #22 recommendations
- Implement class structure per UML diagram in issue #23
- Include shared fields (common to all objects) and specialized fields (record-type specific)
- Document class methods, attributes, and usage examples
- Commit class library to GitHub repository under appropriate module structure

**Labels:** `enhancement`, `development`, `architecture`, `python`

**Dependencies:** #22, #23, #24

---

### Issue: Evaluate Sensor ID and Class Diagram Proposals Using Audio Pipeline

**Assignee:** Dangol Sunima

**Description:**

Review and evaluate Kazi Tamim's proposals in issues #22, #23, and #24 by testing them against the existing audio pipeline implementation. Identify ambiguities, potential conflicts, areas requiring refinement, or missing definitions. Provide feedback on how well the proposed ID system and class structure integrate with real-world microphone acquisition workflows.

**Acceptance Criteria:**

- Review proposals in issues #22, #23, #24 thoroughly
- Test proposed sensor ID system against audio pipeline use cases
- Test proposed class structure against audio data flow (L1-L5 layers)
- Document findings: ambiguities, conflicts, missing definitions, or areas for improvement
- Provide written feedback in issue comments or summary document
- Recommend refinements or modifications to proposals as needed

**Labels:** `research`, `testing`, `audio`, `validation`

**Dependencies:** #22, #23, #24

---

### Issue: Implement Data Flow Testing Through L1-L5 Layers

**Assignee:** Dangol Sunima

**Description:**

Once abstract class libraries are developed (see Kazi Tamim's task), implement test cases to validate data flow through the L1-L5 computational layers using the audio pipeline as a reference implementation. Focus on ensuring that data can be instantiated, passed through each layer, logged appropriately, and forwarded to the next layer—even if the internal processing logic is not yet implemented.

**Acceptance Criteria:**

- Import and instantiate class library objects for L1-L5 layers
- Create test cases that pass audio data through L1 → L2 → L3 → L4 → L5
- Verify that each layer receives input, logs activity, and forwards output correctly
- Document test results, including any failures or issues encountered
- Commit test code and results to repository

**Labels:** `testing`, `development`, `audio`, `validation`

**Dependencies:** Kazi Tamim's class library development task

## Notes

- The team confirmed Python as the primary development language for the project.
- MongoDB has been recommended as the database solution, pending formal presentation of findings by Kazi Tamim.
- Professor Smith emphasized that initial focus should be on establishing data flow and testing class structures, not on writing to the database.
- Smartphone sensors are being considered as voluntary participation elements in the SAR system, requiring explicit user opt-in.
- The team discussed the need to identify additional sensors beyond microphone and heat/temperature to enable meaningful correlation analysis at the L2 layer.
- Kazi Tasin and Kazi Tamim presented the SAR project at a conference in Albany, increasing project visibility.
- All proposals and research documents are stored in the GitHub repository under `documents/research/nomani`.
