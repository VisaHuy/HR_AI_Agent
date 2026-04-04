### **Table of Contents**
1. [Claude 3.5 Sonnet (Anthropic)](#claude-35-sonnet-anthropic)
2. [Gemini 1.5 Pro (Google)](#gemini-15-pro-google)
3. [ChatGPT 3.5 (OpenAI)](#chatgpt-35-openai)

---

### **Claude 3.5 Sonnet (Anthropic)**
*   **Model Name/Company:** Claude 3.5 Sonnet, developed by **Anthropic**.
*   **Model Type:** This model is built on the philosophy of **Constitutional AI**, which focuses on creating AI systems aligned with human values and ethical considerations. It is specifically recognized for its strong performance in tasks requiring **logical reasoning** and strict adherence to instructions.
*   **Compare with another model:** In the research study, Claude 3.5 Sonnet achieved an **exceptional 95% success rate** (passing 19 out of 20 tasks), significantly outperforming both Gemini 1.5 Pro (60%) and ChatGPT 3.5 (20%). Unlike the other models, Claude demonstrated a robust understanding of **spatial relationships** and maintained object state integrity accurately even in complex, multi-step operations.

### **Gemini 1.5 Pro (Google)**
*   **Model Name/Company:** Gemini 1.5 Pro, developed by **Google**.
*   **Model Type:** Gemini is a **multimodal model** designed to process and generate text, images, audio, and video. Architecturally, it represents a departure from traditional transformer-only designs, incorporating **novel attention mechanisms** and more efficient training techniques.
*   **Compare with another model:** Gemini 1.5 Pro showed a **marked improvement over ChatGPT 3.5**, successfully completing 60% of the tasks compared to ChatGPT's 20%. However, it remained **less reliable than Claude 3.5 Sonnet**; while Gemini performed well on simple tasks, its accuracy decreased as complexity increased, occasionally failing to prevent **object collisions** in three-dimensional space.

### **ChatGPT 3.5 (OpenAI)**
*   **Model Name/Company:** ChatGPT 3.5, developed by **OpenAI**.
*   **Model Type:** Based on the **Generative Pre-trained Transformer (GPT) architecture**, this model utilizes **Reinforcement Learning from Human Feedback (RLHF)**. This technique involves fine-tuning the model on human-written responses and optimizing it through reward modeling to align outputs with human preferences.
*   **Compare with another model:** ChatGPT 3.5 was the **lowest performing model** in the study, with only a 20% success rate. Its primary struggle compared to Claude and Gemini was a **failure to follow multi-step instructions**; for instance, it failed to return the robot to its origin point in 75% of its failed attempts. It also demonstrated significant difficulties with **spatial reasoning** and correctly calculating movements along different axes, leading to more frequent errors than the other two models.

## **Reference**
*   **[1]A. Sobo, A. Mubarak, Almas Baimagambetov, and Nikolaos Polatidis, “Evaluating LLMs for Code Generation in HRI: A Comparative Study of ChatGPT, Gemini, and Claude,” Applied Artificial Intelligence, vol. 39, no. 1, Dec. 2024, doi: https://doi.org/10.1080/08839514.2024.2439610.
**
