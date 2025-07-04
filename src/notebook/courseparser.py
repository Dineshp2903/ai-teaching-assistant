import re
from typing import List, Dict


def extract_line(text: str, label: str) -> str:
    match = re.search(fr"\*\*{label}:\*\*\s*(.*)", text)
    return match.group(1).strip() if match else None


def extract_list(text: str, label: str) -> List[str]:
    match = re.search(fr"\*\*{label}:\*\*\s*(.*?)\n\s*\n", text, re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    items = re.findall(r"-\s+(.*)", block)
    return [item.strip() for item in items]


def extract_duration(text: str) -> float:
    match = re.search(r"\*\*Estimated Duration:\*\*\s*([\d.]+)", text)
    return float(match.group(1)) if match else None


def parse_course_text(agent_output: str) -> List[Dict]:
    weeks = []
    week_sections = re.split(r"\*\*Week\s+(\d+):\s*(.*?)\*\*", agent_output, flags=re.DOTALL)[1:]
    # week_sections = [week_number1, title1, content1, week_number2, title2, content2, ...]
    for i in range(0, len(week_sections), 3):
        week_number = int(week_sections[i])
        module_title = week_sections[i + 1].strip()
        content_block = week_sections[i + 2]

        week_data = {
            "week_number": week_number,
            "module_title": module_title,
            "subtopics": extract_list(content_block, "Key Subtopics"),
            "learning_objectives": extract_list(content_block, "Learning Objectives"),
            "estimated_duration": extract_duration(content_block),
            "tools": extract_list(content_block, "Tools/Platforms"),
            "assignments": extract_list(content_block, "Assignments/Hands-on Practice"),
            "prerequisites": extract_line(content_block, "Prerequisites")
        }
        weeks.append(week_data)

    return weeks


# agent_output would be parsed using the function above.
# For testing, you can assign the agent_output string from user input to test the parser.

agent_output = """
## IoT in Agriculture: A Beginner's Guide (6-Week Course Syllabus)

**Target Audience:**  B.E. graduates in Electrical and Electronics Engineering (EEE) with basic programming knowledge.

**Course Overview:** This comprehensive 6-week course introduces the fundamentals of Internet of Things (IoT) technology and its applications in agriculture.  Participants will gain a practical understanding of how sensors, actuators, data communication, and cloud computing are revolutionizing farming practices. Through hands-on exercises and real-world case studies, they will learn to design, implement, and analyze IoT solutions for smart agriculture.

**Week 1: Introduction to IoT and Agriculture**

- **Key Subtopics:** 
    -  What is IoT?
    -  Applications of IoT in Agriculture
    -  Types of sensors used in agriculture
    -  Basic networking concepts
- **Learning Objectives:** 
    -  Define IoT and its core components.
    -  Understand the potential of IoT in transforming agriculture.
    -  Identify different types of sensors used in various agricultural applications.
    -  Grasp fundamental networking concepts relevant to IoT.
- **Estimated Duration:** 8 hours
- **Tools/Platforms:** 
    -  Online presentation software (e.g., Google Slides, PowerPoint)
    -  Introductory IoT resource websites (e.g., IoTivity, ThingSpeak)
- **Assignments/Hands-on Practice:** 
    - Research and present a use case of IoT in agriculture.
    - Hands-on exploration of a simple IoT sensor and its data outputs.

**Week 2: Sensors and Actuators in Agriculture**

- **Key Subtopics:** 
    -  Soil sensors (moisture, pH, nutrient levels)
    -  Weather sensors (temperature, humidity, rainfall)
    -  Plant sensors (growth, stress, disease)
    -  Actuators: Irrigation systems, lighting control
- **Learning Objectives:** 
    -  Explore the functionalities of different types of agricultural sensors.
    -  Understand the principles of operation for actuators in smart agriculture.
    -  Learn how sensors collect and transmit data for agricultural applications.
- **Estimated Duration:** 10 hours 
- **Tools/Platforms:**
    -  Sensor data visualization tools (e.g., ThingSpeak, Blynk)
- **Assignments/Hands-on Practice:**  
    -  Develop a simple data logging system using a soil moisture sensor and a cloud platform.

**Week 3: Data Communication and Networking**

- **Key Subtopics:** 
    -  Cellular networks (2G, 3G, 4G, 5G)
    -  Wi-Fi networks for IoT sensors
    -  Low-Power Wide-Area Networks (LPWAN)
    -  Data transmission protocols (MQTT, CoAP)
- **Learning Objectives:**
    -  Compare and contrast different communication protocols suitable for IoT in agriculture.
    -  Understand the concepts of network security in IoT.
    -  Familiarize with basic data transmission protocols used in IoT.
- **Estimated Duration:** 8 hours
- **Tools/Platforms:**  
    -  Network simulation software (e.g., NS-3)
    -  IoT platform with cloud connectivity (e.g., Azure IoT Hub, AWS IoT Core)
- **Assignments/Hands-on Practice:**   
    -  Set up a basic network communication using a sensor and a cloud platform.

**Week 4: Cloud Computing and Data Analytics**

- **Key Subtopics:** 
    -  Cloud storage for IoT data
    -  Data processing and analytics platforms
    -  Machine learning algorithms for agricultural applications
- **Learning Objectives:** 
    -  Explore the benefits of cloud computing for storing and analyzing IoT data.
    -  Understand how to use data analytics tools for agricultural decision-making.
    -  Introduce basic machine learning concepts relevant to agriculture. 
- **Estimated Duration:** 10 hours
- **Tools/Platforms:**
    -  Cloud data storage services (e.g., AWS S3, Azure Blob Storage)
    -  Data visualization libraries (e.g., matplotlib, seaborn)
- **Assignments/Hands-on Practice:** 
    -  Process and visualize historical agricultural sensor data using a cloud platform and data analytics tools.

**Week 5: Designing and Implementing IoT Solutions for Agriculture**

- **Key Subtopics:** 
    -  System Design Principles for IoT in Agriculture
    -  Prototype Development 
    -  Case Studies: Smart irrigation, precision farming, livestock monitoring
- **Learning Objectives:** 
    -  Apply design principles to develop IoT solutions for specific agricultural challenges.
    -  Build a basic prototype of an IoT-based agriculture solution.
    -  Analyze real-world case studies of successful IoT implementations in agriculture.
- **Estimated Duration:** 12 hours 
- **Tools/Platforms:** 
    -  Microcontroller boards (e.g., Arduino, Raspberry Pi)
    -  IOT sensing kits
    -  Cloud platform for data visualization and analysis
- **Assignments/Hands-on Practice:**  
    -  Build a simple prototype of an IoT-based agriculture solution (e.g., a smart plant watering system).

**Week 6: Future Trends and Challenges in IoT Agriculture**
- **Key Subtopics:**
    -  Emerging Technologies ( AI, Blockchain, Drones)
    -  Ag-Tech Industry Landscape
    -  Ethical Considerations and Sustainability
- **Learning Objectives:**
    -  Explore the latest advancements driving innovation in IoT agriculture.
    -  Analyze the impact of these technologies on the agricultural sector.
    -  Discuss the ethical implications and sustainability concerns associated with IoT in agriculture.
- **Estimated Duration:** 6 hours
- **Tools/Platforms:**
    -  Online articles and research papers on emerging IoT trends in agriculture
    -  Industry reports and white papers
- **Assignments/Hands-on Practice:** 
    -  Research paper on a specific trend in IoT agriculture (e.g., blockchain in supply chain management) or 
    -  Develop a proposal for a new IoT solution addressing a challenge in agriculture.
"""

result = parse_course_text(agent_output)
print(result)