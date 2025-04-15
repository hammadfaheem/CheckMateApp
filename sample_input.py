student_raw_text ="""The OSI model in networking is a conceptual framework used to understand and standardize the functions of a communication system. It consists of seven layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.
A router is a device that forwards data packets between computer networks, while a switch operates at a local level to connect devices within a single network.
Firewalls are crucial for network security because they monitor and control incoming and outgoing network traffic based on security rules, helping prevent unauthorized access and attacks."""


teacher_questions = """1. What is the OSI model in networking?
2. What are the differences between a router and a switch?
3. Explain the importance of firewalls in network security."""

teacher_raw_text = """
1. The OSI (Open Systems Interconnection) model is a conceptual framework used to standardize network communication. It consists of seven layers: 
   - **Physical Layer**: Handles the physical connection between devices.  
   - **Data Link Layer**: Manages node-to-node communication and error detection.  
   - **Network Layer**: Handles routing and forwarding of data packets.  
   - **Transport Layer**: Ensures reliable transmission of data between systems.  
   - **Session Layer**: Manages sessions and connections between applications.  
   - **Presentation Layer**: Translates data formats and encryption.  
   - **Application Layer**: Provides network services to end-users.

2. A **router** and a **switch** serve different functions in networking:
   - A **router** operates at the **network layer (Layer 3)** and is responsible for forwarding data between different networks using IP addresses.  
   - A **switch** operates at the **data link layer (Layer 2)** and is used within a local network (LAN) to connect devices efficiently using MAC addresses.  
   - Routers enable communication between networks (e.g., connecting to the internet), while switches improve network efficiency within a single network.

3. Firewalls play a critical role in **network security** by:
   - Monitoring and controlling **incoming and outgoing traffic** based on predefined security rules.  
   - Preventing **unauthorized access** by blocking malicious traffic.  
   - Acting as a barrier between a **trusted internal network** and **untrusted external sources**, reducing the risk of cyber threats.  
   - Implementing security policies such as **packet filtering, intrusion detection, and deep packet inspection** to safeguard sensitive data.
"""


total_marks = 30


# student_raw_text = """Alice has 12 apples, and she gives 4 apples to her friend Bob. Then, she buys 6 more apples from a store. After that, she equally divides all her apples among 3 of her friends.

# A train travels at a speed of 60 km/h. If it travels for 3 hours without stopping, how far does it go?"""

# teacher_questions = """1. How many apples does Alice have after giving some to Bob and buying more?
# 2. How many apples does each friend get after Alice divides them equally?
# 3. How far does the train travel in 3 hours if it moves at 60 km/h?
# 4. How many oranges does Charlie have left after eating some and receiving more from a friend?
# """
# teacher_raw_text = """ 
# 1. Alice starts with 12 apples. She gives 4 to Bob, leaving her with:
#    12 - 4 = 8 apples.
#    Then, she buys 6 more apples:
#    8 + 6 = 14 apples.
#    So, Alice has **14 apples** after the transactions.

# 2. Alice equally divides the 14 apples among 3 friends:
#    14 ÷ 3 ≈ 4.67 apples per friend.
#    Since apples are whole objects, she can distribute **4 apples per friend** and have **2 apples left**.

# 3. The train travels at a speed of **60 km/h** for **3 hours**. The total distance covered is:
#    Distance = Speed × Time
#    Distance = 60 km/h × 3 h = **180 km**.
#    So, the train travels **180 km** in 3 hours.

# 4. Charlie starts with **10 oranges**. He eats **3 oranges**, leaving him with:  
#    10 - 3 = **7 oranges**.  
#    Then, his friend gives him **5 more oranges**:  
#    7 + 5 = **12 oranges**.  
#    So, Charlie has **12 oranges** after the transactions.
# """


ai_text = """The OSI (Open Systems Interconnection) model is a conceptual framework that standardizes the functions of a telecommunication or computing system into seven layers. It helps different networking devices and systems communicate with each other using standardized protocols.
7 Layers of the OSI Model:

    Physical Layer – Deals with raw data transmission over physical media (cables, radio waves, etc.).
    Data Link Layer – Handles error detection and correction, and establishes direct connections between nodes.
    Network Layer – Manages routing and forwarding of data packets between devices.
    Transport Layer – Ensures reliable data delivery, error recovery, and flow control.
    Session Layer – Manages and controls communication sessions between applications.
    Presentation Layer – Translates, encrypts, and compresses data for the application layer.
    Application Layer – Provides network services to end-users (e.g., web browsing, email).

The OSI model is mainly used as a reference model for understanding network protocols and communication processes. However, real-world networking often follows the TCP/IP model, which is more commonly used in the internet."""

human_text = """The Open Systems Interconnection (OSI) model is a reference model from the International Organization for Standardization (ISO) that "provides a common basis for the coordination of standards development for the purpose of systems interconnection."[2] In the OSI reference model, the communications between systems are split into seven different abstraction layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.[3]

The model partitions the flow of data in a communication system into seven abstraction layers to describe networked communication from the physical implementation of transmitting bits across a communications medium to the highest-level representation of data of a distributed application. Each intermediate layer serves a class of functionality to the layer above it and is served by the layer below it. """