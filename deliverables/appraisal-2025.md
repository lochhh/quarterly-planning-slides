# Annual Appraisal 2025 — Chang Huan Lo

---

## A1: Progress Against Previous Year's Objectives

### Objective 1: Engage in Continuous Learning

I continued to expand my skillset through both structured and self-directed learning. Together with colleagues, I participated in a weekly study group working through the Machine Learning for Intelligent Systems course (CS4780/CS5780), covering topics from supervised learning to kernel methods and ensemble techniques. I also attended RSECon2025, the annual conference for research software engineering, where I participated in discussions on LLM and AI applications in research software engineering, alongside sessions on emerging practices in sustainable research software development.

In my day-to-day work, I adopted and integrated several new tools and frameworks across projects, including loguru for structured logging in movement, artifact.ci for documentation deployment workflows, and the Pydantic data validation library. 

### Objective 2: Foster Collaborative Work

I maintained active collaboration across multiple teams and organisations throughout 2025. Within the Neuroinformatics Unit and the Aeon team, I participated in regular team meetings and contributed team meeting presentations. I engaged with the broader movement community through Community Calls, Zulip discussions, and GitHub discussions.

Beyond SWC, I made cross-organisational contributions to multiple repositories spanning BrainGlobe, SpikeInterface, SLEAP (sleap-io), Bonsai (docfx-tools), and artifact.ci, ranging from CI/CD security improvements to bug fixes and feature enhancements.

### Objective 3: Implement New Features and Maintain Code Quality

This was the most substantial area of delivery in 2025, with 140 merged pull requests across the Aeon, movement, and PoseInterface projects.

**Aeon:**
- Increased aeon_api test coverage to above 78%. Added comprehensive unit tests for the `video.py`, `schema`, `api`, and `reader` modules.
- Improved the `load` API with optional start/end boundary support and datetime index handling.
- Maintained documentation quality, including restructuring the User Guide, Reference pages, adding social analysis example notebooks, hardware documentation, wiring schematics, a publications page.
- Set up full experiment data sharing via Globus.

**Movement:**
- Completed logging refactor, replacing Python's `logging` module with `loguru` for more structured and user-friendly logging.
- Unified the dataset loading interface, refactored dataset validators, and wrote contributor guide on adding new loaders/validators. This simplifies the process of writing new loaders, enabling movement to support a wider range of tracking software.
- Added support for loading and saving 3D DeepLabCut poses.
- Added I/O support for the ndx-pose NWB extension, enabling movement to read and write pose data in the Neurodata Without Borders format.
- Improved documentation with API docs aggregation for flat modules, a gallery of examples, and automatically updating contributor list.

**PoseInterface:**
- Set up the foundational codebase and documentation infrastructure.

### Objective 4: Improve Documentation Quality

Documentation was a significant focus across all projects. Beyond the 47 aeon_docs PRs mentioned above, key documentation achievements included:
- Added comprehensive hardware documentation for the Aeon acquisition system, including wiring schematics and acquisition module specifications.
- Added a publications page and restructured the User Guide for improved navigation.
- Updated and maintained contributor guidelines, including clarifying docs deployment workflows and contributing code guidelines.
- Wrote and improved docstrings for aeon_api's `api.py` and `reader.py` modules.

### Objective 5: Increase Engagement in Online Discussions

I actively participated in project-relevant discussions across multiple platforms. On GitHub, I opened 69 issues and engaged in discussions across Aeon, movement, and external repositories. I contributed to Zulip discussions and participated in movement Community Calls. 

---

## A2: Demonstrating Achievements

### 1. Professional Practices

My most significant technical contributions in 2025 centred on three areas:

**Software architecture and API design:** I designed and implemented the unified dataset loading interface in movement, consolidating separate loading functions into a cohesive API. This simplifies the user experience and establishes a pattern for future data format support. In aeon_api, I improved the `load` function with optional boundary inclusion and datetime index support, addressing user-reported issues.

**Testing and code quality:** I exceeded the aeon_api test coverage target (>70%), writing comprehensive unit tests for core modules. I also drove code quality improvements including refactoring DeepLabCut CSV validation in movement and fixing ruff and mypy errors across projects.

**Research support:** I contributed to the Aeon platform paper by maintaining and improving the documentation site, sharing full social experiment datasets via Globus, and adding example notebooks (HMM analysis, social analysis, DataJoint fetch and compute) to support data analysis workflows.

### 2. Interpersonal Skills

I collaborated effectively across team and organisational boundaries. Within NIU and Aeon, I contributed to team meetings, shared knowledge through presentations, and engaged in Community Calls and Zulip discussions. I volunteered as a Teaching Assistant for three courses in Experimental Neuroscience 2025 (Introduction to Software Development in Python, Video Behavioural Analysis, and Collaborative Coding and Software Development Good Practices), and co-created course materials and served as TA for the Animals in Motion track at NIU Open Software Week 2025.

### 3. Management, Planning, and Delivery

N/A

### 4. Governance and Compliance

N/A

### 5. Institutional Citizenship

I volunteered as a Teaching Assistant for the following courses taught as part of Experimental Neuroscience 2025 at UCL:
- Introduction to Software Development in Python
- Video Behavioural Analysis
- Collaborative Coding and Software Development Good Practices

I also served as a TA and co-created course materials for the Animals in Motion track at NIU Open Software Week 2025.

Beyond teaching, I contributed to raising UCL's and NIU's profile through open-source contributions to external projects (BrainGlobe, SpikeInterface, SLEAP, Bonsai), demonstrating NIU's commitment to collaborative, open research software development.

### 6. Development

**Formal/structured learning:**
- Participated in a weekly colleague study group on Machine Learning for Intelligent Systems (Cornell CS4780/CS5780), covering supervised and unsupervised learning, kernel methods, and ensemble techniques.
- Attended RSECon2025.

**Informal/on-the-job learning:**
- Adopted and integrated new tools and frameworks: loguru (structured logging), artifact.ci (documentation preview on CI), Pydantic (data validation).
- Gained experience with Globus data management by setting up dataset sharing for Aeon social experiments.

### 7. Feedback

The Aeon platform paper, which I contributed to through extensive documentation, dataset sharing, and example notebooks, was published/submitted in 2025 — representing recognition of the team's collective work on making the Aeon system accessible to the broader research community.

---

## A3: Planning for the Future

### 1. Priorities

Key areas of focus for the coming year include:

- **Aeon:** Continue expanding test coverage, upgrade DataJoint integration (from 0.14.x to 2.x), develop ephys pipeline, documentation.
- **Movement:** Unify save interface (extending the unified loader work), COCO keypoint results format support.
- **PoseInterface:** Convert to COCO annotations.
- **NIU shared tooling:** Maintenance of shared CI/CD infrastructure.
- **Green DiSC certification:** Initiate the process of obtaining Green Digital Sustainability Certification for NIU.

### 2. Career Aspirations

I would like to broaden my responsibilities to include driving the Green DiSC certification for NIU, combining my technical background with environmental sustainability practices in research computing.