import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('Companies_tab')


def lambda_handler(event, context):
    logger.info("Event: %s", str(event))

    intent_name = event['sessionState']['intent']['name']
    logger.info("Intent detected: %s", intent_name)

    # ---------------- COMPANY INFO INTENT ----------------
    if intent_name == "CompanyInfoIntent":

        try:
            company_name = event['sessionState']['intent']['slots']['CompanyName']['value']['interpretedValue'].strip()
        except Exception:
            return build_response("Please provide a valid company name like Amazon or Google.","CompanyInfoIntent")

        response = table.scan()
        items = response.get('Items', [])

        item = next(
            (i for i in items if i['CompanyName'].lower() == company_name.lower()),
            None
        )

        if item:
            message = (
                f"🏢 Company: {item['CompanyName']}\n"
                f" | "
                f"📊 Hiring Scale: {item['HiringScale']}\n"
                f" | "
                f"💼 Roles: {item['TypicalRoles']}"
            )
        else:
            message = f"❌ Company '{company_name}' not found."

        return build_response(message,intent_name)

    # ---------------- ELIGIBILITY INTENT ----------------
    elif intent_name == "EligibilityIntent":

        try:
            company_name = event['sessionState']['intent']['slots']['CompanyName']['value']['interpretedValue'].strip()
        except Exception:
            return build_response("Please tell a company name like Amazon, Google, Microsoft.","EligibilityIntent")

        response = table.scan()
        items = response.get('Items', [])

        item = next(
            (i for i in items if i['CompanyName'].lower() == company_name.lower()),
            None
        )

        if item:
            message = (
                f"🎓 Minimum CGPA: {float(item['MinCGPA'])}\n\n"
                f"|"
                f" 💼 Eligible Roles: {item['TypicalRoles']}"
            )
        else:
            message = f"❌ Eligibility info not found for '{company_name}'."

        return build_response(message,intent_name)

    # ---------------- COMPARISON INTENT ----------------

    elif intent_name == "ComparisonIntent":

        try:
            company_a = event['sessionState']['intent']['slots']['CompanyA']['value']['interpretedValue'].strip()
            company_b = event['sessionState']['intent']['slots']['CompanyB']['value']['interpretedValue'].strip()
        except:
            return build_response(
                "Please provide two companies like Amazon and Google.",
                intent_name
            )

        logger.info("Company A from Lex: %s", company_a)
        logger.info("Company B from Lex: %s", company_b)

        response = table.scan()
        items = response.get('Items', [])

        def normalize(text):
            return text.lower().replace(" ", "").strip()

        a = next(
            (
                i for i in items
                if normalize(i['CompanyName']) == normalize(company_a)
            ),
            None
        )

        b = next(
            (
                i for i in items
                if normalize(i['CompanyName']) == normalize(company_b)
            ),
            None
        )

        if a and b:
            message = (
                f"⚖️ Company Comparison\n\n"
                f"🏢 {a['CompanyName']}\n"
                f"🎓 CGPA: {a['MinCGPA']}\n"
                f"📊 Hiring Scale: {a['HiringScale']}\n\n"
                f"    VS\n\n   "
                f"🏢 {b['CompanyName']}\n"
                f"🎓 CGPA: {b['MinCGPA']}\n"
                f"📊 Hiring Scale: {b['HiringScale']}"
            )
        else:
            message = (
                f"❌ {company_a} or {company_b} not found in database."
            )

        return build_response(message, intent_name)

    # ----------------  ROLE EXPLAINER INTENT ----------------
    elif intent_name == "RoleExplainerIntent":

        role_explanations = {

            "sde": (
                "SDE (Software Development Engineer):\n"
                "- Designs and builds software applications\n"
                "- Works on backend, frontend, and system design\n"
                "- Strong focus on DSA and problem solving\n"
                "- Uses Java, Python, C++\n"
                "- Common in Amazon, Google, Microsoft"
                "- Participates in code reviews and debugging\n"
                "- Works with databases, APIs, and cloud services\n"
            ),

            "software engineer": (
                "Software Engineer:\n"
                "- Develops and maintains software systems\n"
                "- Builds applications, APIs, and backend services\n"
                "- Requires strong coding and debugging skills"
            ),

            "data scientist": (
                "Data Scientist:\n"
                "- Analyzes large datasets to extract insights\n"
                "- Analyzes large datasets\n"
                "- Builds machine learning models\n"
                "- Uses Python, Statistics, Pandas, NumPy"
                "- Performs data cleaning and feature engineering\n"
                "- Uses Python, Statistics, Pandas, NumPy, Scikit-Learn\n"
                "- Creates visualizations and business reports\n"
                "- Works closely with business and product teams\n"
                "- Career Growth: Senior Data Scientist → Lead Data Scientist"
            ),

            "data analyst": (
                "Data Analyst:\n"
                "- Analyzes business data\n"
                "- Creates dashboards and reports\n"
                "- Uses SQL, Excel, Power BI, Tableau"
            ),

            "ml engineer": (
                "ML Engineer:\n"
                "- Builds and deploys ML models\n"
                "- Uses TensorFlow, PyTorch, Python\n"
                "- Works on production AI systems"
            ),

            "ai engineer": (
                "AI Engineer:\n"
                "- Builds AI applications and chatbots\n"
                "- Works with ML, Deep Learning, Generative AI\n"
                "- Uses OpenAI APIs, LangChain, Python"
                "- Works with LLMs, NLP, and AI models"
            ),

            "product manager": (
                "Product Manager:\n"
                "- Defines product roadmap\n"
                "- Works with engineering and business teams\n"
                "- Focuses on customer requirements"
            ),

            "devops engineer": (
                "DevOps Engineer:\n"
                "- Manages CI/CD pipelines\n"
                "- Automates deployments\n"
                "- Uses Docker, Kubernetes, AWS"
                "- Improves deployment speed and reliability\n"
                "- Monitors infrastructure and application health\n"
                "- Works closely with development teams\n"
                "- Career Growth: Senior DevOps Engineer → Platform Engineer"
            ),

            "cloud engineer": (
                "Cloud Engineer:\n"
                "- Designs cloud infrastructure\n"
                "- Works with AWS, Azure, GCP\n"
                "- Manages scalable cloud systems"
                "- Deploys scalable and highly available systems\n"
                "- Manages networking, security, and storage services\n"
                "- Uses Infrastructure as Code tools like Terraform\n"
                "- Monitors performance and optimizes cloud costs\n"
                "- Career Growth: Senior Cloud Engineer → Cloud Architect"
            ),

            "frontend developer": (
                "Frontend Developer:\n"
                "- Builds website user interfaces\n"
                "- Uses HTML, CSS, JavaScript, React\n"
                "- Focuses on user experience"
            ),

            "backend developer": (
                "Backend Developer:\n"
                "- Builds APIs and server-side applications\n"
                "- Uses Python, Java, Node.js\n"
                "- Works with databases and cloud services"
            ),

            "full stack developer": (
                "Full Stack Developer:\n"
                "- Works on frontend and backend\n"
                "- Builds complete web applications\n"
                "- Uses React, Node.js, SQL, APIs"
                "- Works with SQL and NoSQL databases\n"
                "- Integrates APIs and cloud services\n"
                "- Handles deployment and maintenance\n"
                "- Career Growth: Senior Developer → Tech Lead"
            ), 

            "genai engineer": (
                "GenAI Engineer:\n"
                "- Builds Generative AI applications using LLMs\n"
                "- Develops chatbots, AI assistants, and RAG systems\n"
                "- Works with OpenAI, Claude, Gemini, and Llama models\n"
                "- Uses LangChain, LangGraph, Vector Databases\n"
                "- Designs prompt workflows and AI pipelines\n"
                "- Deploys AI applications on cloud platforms\n"
                "- Career Growth: Senior GenAI Engineer → AI Architect"
            ),

            "data engineer": (
                "Data Engineer:\n"
                "- Builds and manages data pipelines\n"
                "- Collects, transforms, and stores large datasets\n"
                "- Works with SQL, Python, Spark, Hadoop\n"
                "- Designs data warehouses and ETL processes\n"
                "- Ensures data quality and scalability\n"
                "- Supports Data Scientists and ML Engineers\n"
                "- Career Growth: Senior Data Engineer → Data Architect"
            ),

            "computer vision engineer": (
                "Computer Vision Engineer:\n"
                "- Develops systems that understand images and videos\n"
                "- Builds object detection and image classification models\n"
                "- Works with OpenCV, TensorFlow, PyTorch\n"
                "- Used in autonomous vehicles, healthcare, and security\n"
                "- Trains deep learning models on visual data\n"
                "- Optimizes models for real-time performance\n"
                "- Career Growth: Senior CV Engineer → AI Researcher"
            ),

            "prompt engineer": (
                "Prompt Engineer:\n"
                "- Designs prompts for Large Language Models (LLMs)\n"
                "- Improves AI response quality and accuracy\n"
                "- Works with GPT, Claude, Gemini, and other LLMs\n"
                "- Creates prompt templates and AI workflows\n"
                "- Evaluates and optimizes AI outputs\n"
                "- Collaborates with AI Engineers and Product Teams\n"
                "- Career Growth: Senior Prompt Engineer → GenAI Specialist"
            ),

            "cybersecurity engineer": (
                "Cybersecurity Engineer:\n"
                "- Protects systems, networks, and applications from attacks\n"
                "- Performs vulnerability assessments and penetration testing\n"
                "- Works with firewalls, encryption, and security tools\n"
                "- Monitors and responds to security incidents\n"
                "- Ensures compliance with security standards\n"
                "- Uses tools like Wireshark, Burp Suite, SIEM platforms\n"
                "- Career Growth: Security Engineer → Security Architect"
            )
        }

        role_aliases = {

            "sde": ["sde", "software development engineer"],

            "software engineer": [
                "software engineer",
                "software developer",
                "developer",
                "software engineering"
            ],

            "data scientist": [
                "data scientist",
                "data science"
            ],

            "data analyst": [
                "data analyst",
                "business analyst",
                "data analyst engineer"
            ],

            "ml engineer": [
                "ml engineer",
                "machine learning engineer"
            ],

            "ai engineer": [
                "ai engineer",
                "artificial intelligence engineer",
                "genai engineer",
                "generative ai engineer",
                "ai developer"
            ],

            "product manager": [
                "product manager",
                "pm",
                "product owner"
            ],

            "devops engineer": [
                "devops engineer",
                "devops",
                "sre",
                "site reliability engineer"
            ],

            "cloud engineer": [
                "cloud engineer",
                "aws engineer",
                "azure engineer",
                "gcp engineer",
                "cloud architect",
                "cloud developer"
            ],

            "frontend developer": [
                "frontend developer",
                "front end developer",
                "react developer"
                
            ],

            "backend developer": [
                "backend developer",
                "back end developer",
                "api developer"

            ],

            "full stack developer": [
                "full stack developer",
                "fullstack developer",
                "full stack engineer"
            ],

            "genai engineer": [
                "genai engineer",
                "generative ai engineer",
                "llm engineer",
                "large language model engineer"
            ],
            "data engineer": [
                "data engineer",
                "data engineering"
            ],
            "computer vision engineer": [
                "computer vision engineer",
                "cv engineer",
                "vision engineer"
            ],
            "prompt engineer": [
                "prompt engineer",
                "prompt engineering",
                "prompt engineering specialist"

            ],
            "cybersecurity engineer": [
                "cybersecurity engineer",
                "security engineer",
                "cybersecurity",
                "infosec engineer",
                "security specialist"

            ]

        }

        user_input = event.get("inputTranscript", "").lower()

        logger.info("USER INPUT: %s", user_input)

        matched_role = None

        all_aliases = []

        for role_name, aliases in role_aliases.items():
            for alias in aliases:
                all_aliases.append((alias, role_name))

        all_aliases.sort(key=lambda x: len(x[0]), reverse=True)

        for alias, role_name in all_aliases:
            if alias in user_input:
                matched_role = role_name
                break

        if matched_role:
            message = role_explanations[matched_role]
        else:
            message = (
                "I can explain roles like:\n"
                "- SDE\n"
                "- Software Engineer\n"
                "- Data Scientist\n"
                "- Data Analyst\n"
                "- ML Engineer\n"
                "- AI Engineer\n"
                "- Product Manager\n"
                "- DevOps Engineer\n"
                "- Cloud Engineer\n"
                "- Frontend Developer\n"
                "- Backend Developer\n"
                "- Full Stack Developer"
            )

        return build_response(message, intent_name)
    # ---------------- FALLBACK ----------------

    elif intent_name == "WelcomeIntent":

        message = (
            "👋 Welcome to Student Placement Assistant!\n\n | "
            "I can help you with:\n\n | "
            "🏢 Company Information\n | "
            "🎓 Eligibility Criteria\n | "
            "⚖ Company Comparison\n | "
            "💼 Role Explanations\n\n | "
            "Try asking:\n"
            "- Tell me about Amazon\n | "
            "- Eligibility for Google\n | "
            "- Compare Amazon vs Tesla\n | "
            "- Explain AI Engineer"
        )
        return build_response(message, intent_name)

    else:

        message = (
            "❓ Sorry, I didn't understand that.\n\n"
            "You can ask things like:\n\n"
            "🏢 Tell me about Amazon\n"
            "🎓 Eligibility for Google\n"
            "⚖ Compare Amazon vs Tesla\n"
            "💼 Explain ML Engineer\n"
            "💼 What does a Data Scientist do?\n\n"
            "Try one of the examples above."
        )

        return build_response(message, intent_name)


# ---------------- RESPONSE FUNCTION ----------------
def build_response(message, intent_name):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }