# Sources and References

This document lists the sources referred to during the development of the College ID Validator project for Turtil Company internship, completed by [Your Name] on June 21, 2025.

## General Resources
1. **Grok 3 (xAI)**  
   - **Description**: AI assistant provided initial code snippets, guidance on dataset integration, model training (`images_classifier.py`), README creation, and Docker deployment. Assisted in debugging errors and optimizing accuracy (90.91% validation, 100% test on 45 cases).  
   - **Usage**: Code structure for `sample.py`, `main.py`, and testing was generated with Grok’s help, then extensively customized with project-specific logic (e.g., 354 colleges, Docker setup).

2. **ChatGPT (OpenAI)**  
   - **Description**: AI tool used to generate initial code ideas for image processing, API setup, and testing scripts.  
   - **Usage**: Provided starting points for `main.py` and `test_validation.py`, significantly modified to meet project requirements.

3. **Canva**  
   - **URL**: [https://www.canva.com](https://www.canva.com)  
   - **Description**: Online design tool providing customizable ID card templates. Used to manually create base designs for 161 simulated ID card designs for the dataset.  
   - **Usage**: Templates were downloaded, modified (e.g., altered layouts, added noise), and integrated into `generated_ids/` to ensure simulation.

4. **ThisPersonDoesNotExist.com**  
   - **URL**: [https://thispersondoesnotexist.com](https://thispersondoesnotexist.com)  
   - **Description**: Website generating AI-based unique face images. Used to source base face photos for 161 IDs and 45 test cases.  
   - **Usage**: Images were manually incorporated, then masked or blurred (via `sample.py`) to avoid resembling real individuals.

5. **Python Documentation**  
   - **URL**: [https://docs.python.org/3/](https://docs.python.org/3/)  
   - **Description**: Official Python documentation for libraries like `PIL`, `torch`, and `fastapi`.  
   - **Usage**: Guided implementation of image processing and API endpoints.

6. **Docker Documentation**  
   - **URL**: [https://docs.docker.com/](https://docs.docker.com/)  
   - **Description**: Official guide for Docker installation and containerization.  
   - **Usage**: Informed Dockerfile creation and deployment commands.

## Specific Code References
- **Sample Data Generation**: AI-generated code (Grok, ChatGPT) and online tutorials (e.g., Stack Overflow) adapted for `sample.py`, with Canva templates and `thispersondoesnotexist.com` images manually integrated and modified.
- **Model Training**: PyTorch tutorials and AI assistance shaped `images_classifier.py`.
- **FastAPI Setup**: Initial code from ChatGPT, refined with FastAPI quickstart for `main.py`.

## Notes
- Code was initially generated with assistance from Grok 3 and ChatGPT, with significant customization including error fixes (e.g., `font=info` typo), dataset enhancement (161 IDs, 45 test cases), and Docker integration.
- 161 ID cards and 45 test cases were manually created using Canva templates (modified with noise and layout changes) and `thispersondoesnotexist.com` images (masked or blurred), ensuring all logos, names (except college names), roll numbers, and images are simulated as per requirements. Only college names from `approved_colleges.json` are real.
- Evaluators can contact [yourname@example.com](mailto:yourname@example.com) for clarification or to review the process.