Backend Data Engineering Journey

A hands-on learning repository documenting my progression toward becoming a Backend Data & Ingestion Engineer, with a focus on building reliable Python systems that extract, validate, transform, and prepare data for downstream use.

The repository contains practical exercises, experiments, notes, testing work, and progressively more structured implementations as I build my understanding of backend automation and data ingestion.

---

🎯 Current Direction

Backend Automation • Data Ingestion • Python • REST APIs • Data Validation • ETL

My current focus is developing the engineering fundamentals required to build dependable data ingestion systems rather than simply learning isolated technologies.

---

🧠 What I Have Practiced

Python & Execution Fundamentals

- Functions, classes, objects, and instances
- Modules and imports
- Call stack and execution flow
- References and object identity
- Mutable vs immutable objects
- Shallow vs deep copying
- "self" and instance state
- Context managers and resource lifecycle

HTTP & REST API Engineering

- "requests"
- "requests.Session"
- Authentication and API keys
- HTTP headers
- Timeouts
- HTTP status handling
- JSON responses
- Response validation
- HTTP connection reuse and session state

Reliable HTTP Clients

- "HTTPAdapter"
- "urllib3 Retry"
- Bounded retries
- Retryable HTTP status codes
- Exponential backoff
- "Retry-After"
- Idempotent HTTP methods
- Separation of transport and pipeline logic

Data Validation

- Pydantic
- "BaseModel"
- "model_validate()"
- Nested schemas
- Field aliases
- "EmailStr"
- "HttpUrl" / URL validation
- Validation errors
- Handling invalid API payloads

Data Processing & Ingestion

- Nested JSON processing
- Data transformation
- Data flattening
- Pagination
- Page-by-page extraction
- Dataset accumulation
- ETL pipeline structure
- Separation of extraction, validation, transformation, and orchestration

Testing Fundamentals

- Test cases
- Assertions
- Positive tests
- Negative tests
- Edge cases
- Exception testing
- "pytest"
- Reading test failures and actual-vs-expected results

---

🏗️ Engineering Patterns I'm Practicing

A major part of this journey is learning why systems are structured the way they are, not just making code work.

Current architectural concepts include:

main()
   ↓
Pipeline Orchestration
   ↓
Pagination / Extraction
   ↓
HTTP Client
   ↓
API Response
   ↓
Pydantic Validation
   ↓
Transformation
   ↓
Output Dataset

I'm also practicing:

- Separation of concerns
- Single-responsibility design
- Dependency relationships
- Resource ownership and lifecycle
- Reusable HTTP client design
- Fault-tolerant request handling
- Explicit error handling
- Testable code structure

---

📍 Roadmap

✅ Practiced / Covered

- [x] Python fundamentals
- [x] Python execution flow
- [x] Call stack and object references
- [x] Object identity and mutability
- [x] OOP fundamentals
- [x] "self" and instance variables
- [x] Context managers
- [x] "requests"
- [x] "requests.Session"
- [x] REST API requests
- [x] Authentication fundamentals
- [x] HTTP headers and timeouts
- [x] HTTP response handling
- [x] Retry strategies
- [x] "HTTPAdapter" + "Retry"
- [x] Exponential backoff
- [x] Pydantic validation
- [x] Nested JSON schemas
- [x] Data transformation and flattening
- [x] Pagination fundamentals
- [x] ETL architecture fundamentals
- [x] Logging fundamentals
- [x] Testing fundamentals
- [x] "pytest" basics
- [x] Assertions and exception testing

🔄 Currently Developing

- [ ] Deeper automated testing
- [ ] Testing HTTP clients and API behavior
- [ ] Database integration
- [ ] PostgreSQL
- [ ] Data persistence patterns
- [ ] Scheduling and automation
- [ ] More robust ingestion pipelines
- [ ] End-to-end pipeline projects

🔜 Planned

- [ ] Advanced web scraping and extraction
- [ ] Production-oriented data ingestion projects
- [ ] Advanced API integration patterns
- [ ] Monitoring and operational reliability
- [ ] End-to-end data engineering projects

---

🧪 Learning Approach

I follow a mastery-first approach:

«Understand → Practice → Test → Refine → Build»

Rather than rushing through technologies, I focus on understanding how each component works, how it connects to the rest of the system, and why a particular engineering decision is appropriate.

The goal is to move from:

Learning concepts
      ↓
Writing small exercises
      ↓
Understanding execution and data flow
      ↓
Testing behavior
      ↓
Building reusable components
      ↓
Building complete ingestion systems

---

📂 Repository Structure

The repository is organized progressively so that each stage builds on the previous one.

backend-data-engineering-journey/
│
├── 01_python_basic/
│
├── 02_pydantic_validation/
│
├── 03_api_requests/
│   └── authentication/
│
├── ...
│
└── README.md

The structure will evolve as the learning path expands.

---

🌐 Connect

- LinkedIn: https://www.linkedin.com/in/ibrahim-waziri-b69909293

- Peerlist: peerlist.io/worldofwazeer

---

👤 Author

Ibrahim Waziri

Backend Data & Ingestion Engineering Learner

Building practical Python skills, documenting the engineering process, and progressing from fundamentals toward reliable data ingestion systems.

«Learning in public. Building for the future.»