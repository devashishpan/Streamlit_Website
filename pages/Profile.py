import pandas as pd
import requests
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Profile",
    page_icon="😊",
)

# sidebar info
st.sidebar.title("User Profile")
st.sidebar.info("This is my Profile.")
#--------------------------------------------------------------------------------------------------------------------
# Other elements
GRAPHQL_URL = "https://api.github.com/graphql"
GRAPHQL_QUERY = """
query {
  viewer {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

def fetch_github_activity(token):
    headers = {
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(GRAPHQL_URL, json={"query": GRAPHQL_QUERY}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"API Request Failed. Status Code: {response.status_code}")
        st.write(response.text)
        return None

#--------------------------------------------------------------------------------------------------------------------




# Headline Section
st.header("AI/ML Engineer & Systems Builder")
st.subheader("Lightweight Model Design | Automated Workflows & Production Pipelines | Big Data Analytics")

# About Me Section
with st.container(border=True,horizontal_alignment="left"):
    col1, col2 = st.columns([3,1],vertical_alignment="center")
    with col1:
        st.markdown("""
        ## Hi! 
        I'm Devashish Kumar Pan. I am a Software Engineer.  
        
        I build scalable backends and production-grade LLM workflows.
        I am a Computer Science & Engineering graduate specializing in Python architecture, high-throughput REST APIs, and automated agentic pipelines deployed securely in the cloud. \
        
        """,anchors=False)
    with col2:
        st.image("assets/profile2.jpg")

# Tech Stack Section
with st.container(border=True, horizontal_alignment="left"):
    st.markdown("""
    ## My Tech Stack
    """,anchors=False)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Model Development",
            "AI/ML Workflows & Agents",
            "Backend & APIs",
            "Serving & Infrastructure",
            "Web Development",
        ]
    )
    with tab1:
        st.markdown("#### Designing, training, and fine-tuning lightweight, task-specific architectures.",anchors=False)
        tab1_data = {
            "Frameworks & Core": [
                "PyTorch",
                "TensorFlow / Keras",
                "Scikit-learn",
                "Numpy & Pandas"
            ],
            "Model Crafting & Training": [
                "Custom NN architectures",
                "Transfer learning",
                "LoRA / QLoRA parameter-efficient fine-tuning (PEFT)",
                "Quantization (GGUF, AWQ)"
            ],
            "Evaluation & Tracking": [
                "MLflow",
                "Weights & Biases (W&B)",
                "Cross-validation, custom loss functions",
                "Confusion metrics & Latency profiling"
            ]
        }
        tab1_df = pd.DataFrame(tab1_data)
        st.markdown(tab1_df.to_markdown(index=False))
    with tab2:
        st.markdown("#### Turning model outputs into autonomous, multi-step execution pipelines.",anchors=False)
        tab2_data = {
            "LLM & Agent Frameworks" : [
                "LangChain",
                "LangGraph",
                "LlamaIndex",
                "LiteLLM"
            ],
            "Workflow Automation & Scheduling" : [
                "Celery",
                "Redis Queues",
                "Airflow",
                "Asynchronous event-driven pipelines"
            ],
            "RAG & Retrieval" : [
                "Vector embeddings",
                "Chunking strategies & Hybrid search" ,
                "ChromaDB & FAISS",
                "Pinecone / Qdrant"
            ]
        }
        tab2_df = pd.DataFrame(tab2_data)
        st.markdown(tab2_df.to_markdown(index=False))
    with tab3:
        st.markdown("#### Embedding intelligence into robust, low-latency production software.",anchors=False)
        tab3_data = {
            "Languages" : [
                "Python",
                "Java & JavaScript",
                "SQL & Rust"
            ],
            "API Frameworks" : [
                "FastAPI & Flask" ,
                "OpenAPI" ,
                "RESTful Architecture & WebSockets / Server-Sent Events (SSE)"
            ],
            "Databases & Caching" : [
                "PostgreSQL",
                "SQLite",
                "Redis (in-memory caching & messaging)"
            ]
        }
        tab3_df = pd.DataFrame(tab3_data)
        st.markdown(tab3_df.to_markdown(index=False))
    with tab4:
        st.markdown("",anchors=False)
        tab4_data = {
            "Containerization & Edge" : [
                "Docker & Docker Compose",
                "ONNX Runtime",
                "Ollama / vLLM"
            ],
            "Cloud & DevOps" : [
                "GitHub Actions (CI/CD) & Git Version Control",
                "Linux environments",
                "Cloud Platforms (GCP / AWS / Render)"
            ],
            "Developer Workflows" : [
                "Pytest",
                "Postman/cURL",
                "Structured JSON schema validation (Pydantic)"
            ]
        }
        tab4_df = pd.DataFrame(tab4_data)
        st.markdown(tab4_df.to_markdown(index=False))
    with tab5:
        st.markdown("""
        
        """,anchors=False)

with st.spinner("Fetching data from GitHub...") and st.container(horizontal_alignment="center"):
    token_ = st.secrets["GIT_TOKEN"]
    result = fetch_github_activity(token_)

    if result and "data" in result and result["data"]["viewer"]:
        calendar = result["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]
        total_contribs = calendar["totalContributions"]

        # Parse JSON results into a flat list of dicts
        flat_days_data = []
        for week in calendar["weeks"]:
            for day in week["contributionDays"]:
                flat_days_data.append({
                    "Date": day["date"],
                    "Contributions": day["contributionCount"]
                })

        # Convert to Pandas DataFrame
        df = pd.DataFrame(flat_days_data)
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        # Display Summary Metric
        with st.container(vertical_alignment="bottom"):
            col1, col2 = st.columns([2,5])
            with col1:
                st.metric(label="Total Contributions (Past Year) for @devashishpan", value=total_contribs)
            with col2:
                st.link_button("Github","https://github.com/devashishpan")
        # Render the Graph
        st.subheader("Daily Contribution Timeline(Last 30 Days)")
        st.line_chart(df.tail(30), y="Contributions", width="stretch")

        # Optional: Show data table toggle
        #with st.expander("View Raw Data Table"):
        #    st.dataframe(df)
    else:
        st.error("Could not retrieve data. Please double-check your username and token permissions.")
