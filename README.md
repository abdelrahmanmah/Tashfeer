<br />
<div align="center">
  
  <a href="https://github.com/abdelrahmanmah/Tashfeer">  <!-- TODO: Update this link! -->
    <!-- You can create a simple logo or use an emoji -->
    <!-- Option 1: Emoji -->
    <h1 style="font-size: 4em;">🕶️</h1>
    <!-- Option 2: Simple Text Logo (if you prefer) -->
    <!-- <img src="images/logo.png" alt="Logo" width="80" height="80"> -->
  </a>

  <h3 align="center">Tashfeer - The Cipher Suite</h3>

  <p align="center">
    An interactive web application for encrypting and decrypting messages using classic ciphers.
    <br />
    Your personal digital enigma machine!
    <br />
    <a href="https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME]/issues">Report Bug</a> <!-- TODO: Update this link! -->
    ·
    <a href="https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME]/issues">Request Feature</a> <!-- TODO: Update this link! -->
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#cipher-protocols">Cipher Protocols</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project 🚀

[![Tashfeer Screenshot][product-screenshot]](https://example.com) <!-- TODO: Add a screenshot URL or path -->
<!-- If you have deployed it, replace https://example.com with the live URL -->
<!-- Otherwise, you can remove the link from the screenshot -->

Welcome, Agent! **Tashfeer** (تشفير - Arabic for "encryption") is your go-to digital toolkit for exploring the fascinating world of classical cryptography. This Streamlit-powered application allows you to:

*   🔒 **Encrypt** sensitive intel before transmission.
*   🔓 **Decrypt** intercepted messages.
*   🔀 Apply **Transposition Ciphers** that rearrange the order of characters.
*   🔄 Employ **Substitution Ciphers** that replace characters with others.
*   ✨ Combine both techniques for **layered security**.

Tashfeer is designed to be intuitive for beginners while offering a glimpse into the core concepts that underpin modern secure communication. Whether you're a budding cryptographer, a puzzle enthusiast, or just looking to send secret messages, Tashfeer has you covered!

### Key Features:
*   **Interactive UI**: Easy-to-use interface powered by Streamlit.
*   **Multiple Cipher Choices**:
    *   🚧 Rail Fence Cipher
    *   📊 Row Transposition Cipher
    *   🅰️ Caesar Cipher
    *   🔑 Vigenère Cipher
*   **Combined Operations**: Encrypt with substitution then transposition, or decrypt in reverse order.
*   **Dynamic Key Inputs**: Tailor keys for each specific cipher.
*   **Real-time Feedback**: Status updates and error handling during operations.
*   **Cipher Briefings**: In-app explanations for each protocol.

### Built With

This section lists the major frameworks/libraries used to bring Tashfeer to life.

*   [![Streamlit][Streamlit-shield]][Streamlit-url]
*   [![Python][Python-shield]][Python-url]
*   [![NumPy][NumPy-shield]][NumPy-url]

<!-- GETTING STARTED -->
## Getting Started 🕵️‍♂️

To get your local copy of Tashfeer up and running, follow these simple steps.

### Prerequisites

Ensure you have Python (3.7+ recommended) and pip installed on your system.
*   Python & pip
    ```sh
    # Check Python version (usually comes with pip)
    python --version
    pip --version
    ```

### Installation

1.  **Clone the Mission Files (Repository)**:
    ```sh
    git clone https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME].git # TODO: Update this link!
    cd [YOUR_REPOSITORY_NAME] # TODO: Update this path!
    ```
2.  **Install Required Packages (Intel)**:
    It's recommended to use a virtual environment.
    ```sh
    # Create a virtual environment (optional but good practice)
    python -m venv venv
    # Activate it:
    # Windows
    # venv\Scripts\activate
    # macOS/Linux
    # source venv/bin/activate

    pip install -r requirements.txt
    ```
3.  **Launch the Cipher Engine**:
    ```sh
    streamlit run project3.py
    ```
    Your default web browser should automatically open Tashfeer!

<!-- USAGE EXAMPLES -->
## Usage 🛠️

Once Tashfeer is running:

1.  **Select Your Objective**: Choose `🔒 Encrypt` or `🔓 Decrypt` from the sidebar.
2.  **Choose Your Strategy**:
    *   `🔀 Transposition Only`: For ciphers that rearrange letters.
    *   `🔄 Substitution Only`: For ciphers that swap letters.
    *   `✨ Combined`: For a two-layer operation (Substitution then Transposition for encryption; Transposition then Substitution for decryption).
3.  **Select Protocol(s)**: Based on your strategy, choose the specific cipher algorithm(s) (e.g., Rail Fence, Caesar).
4.  **Enter Key(s) 🗝️**: Provide the necessary key for the selected cipher(s) (e.g., number of rails, keyword, shift value). Helper text will guide you.
5.  **Input Your Message 📝**: Type or paste your plaintext (for encryption) or ciphertext (for decryption) into the "Input" text area.
6.  **Engage Cipher Engine! 🚀**: Click the button to process your message.
7.  **Retrieve Output 📦**: The processed message will appear in the "Output" text area. Success messages and balloons will confirm mission accomplishment!

Access the `📖 Cipher Protocol Briefings` expander at the bottom for a detailed explanation of how each cipher works and the operational flow.

<!-- You'll want to take a screenshot of your app and save it in an `images` folder or link to it if hosted. -->
<!-- For local images, create an `images` folder in your repo. -->
<!-- ![Tashfeer Interface Screenshot](images/screenshot.png) -->
<!-- If you can create a GIF, that's even better! -->

<!-- CIPHER PROTOCOLS -->
## Cipher Protocols 📜

Tashfeer implements the following classical ciphers:

*   **Transposition Ciphers (Rearrangement)**
    *   `🚧 Rail Fence Cipher`: Writes plaintext diagonally downwards on successive "rails" of an imaginary fence, then reads off row by row.
        *   *Key*: Number of rails (integer ≥ 2).
    *   `📊 Row Transposition Cipher`: Writes plaintext into a grid and reorders the columns based on a keyword.
        *   *Key*: A keyword (string of letters).

*   **Substitution Ciphers (Letter Swapping)**
    *   `🅰️ Caesar Cipher`: Each letter in the plaintext is shifted a certain number of places down or up the alphabet.
        *   *Key*: Shift value (integer 0-25).
    *   `🔑 Vigenère Cipher`: A polyalphabetic substitution using a keyword to determine various Caesar shifts in sequence.
        *   *Key*: A keyword (string of letters).

*   **`✨ Combined Operations`**:
    *   **Encryption**: Substitution cipher is applied first, followed by a transposition cipher on the result.
    *   **Decryption**: Transposition cipher is decrypted first, followed by substitution cipher decryption on the result.

<!-- ROADMAP -->
## Roadmap 🗺️

*   [ ] Add more classical ciphers (e.g., Playfair, ADFGVX).
*   [ ] Implement basic cryptanalysis tools (e.g., frequency analysis).
*   [ ] Option to ignore non-alphabetic characters or include them in ciphers.
*   [ ] Enhanced UI/UX elements.
*   [ ] Ability to save/load encrypted messages and keys.
*   [ ] One-Time Pad (OTP) demonstration (with clear warnings about true randomness).
*   [ ] User accounts / history (if deployed as a larger service).

See the [open issues](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME]/issues) for a full list of proposed features (and known issues). <!-- TODO: Update this link! -->

<!-- CONTRIBUTING -->
## Contributing 🤝

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

<!-- CONTACT -->
## Contact 📞

[Your Name/GitHub Username] - @[YourTwitterHandle_Optional] - [your.email@example.com_Optional] <!-- TODO: Update contact info -->

Project Link: [https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME]](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPOSITORY_NAME]) <!-- TODO: Update this link! -->

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments 🙏

*   Inspired by the world of cryptography and secret codes.
*   [Othneil Drew's Best-README-Template](https://github.com/othneildrew/Best-README-Template) for the structural inspiration.
*   The Streamlit community for an amazing framework.
*   All the pioneers of classical ciphers.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png  <!-- TODO: Create an images/screenshot.png file or link to an uploaded image -->
[Streamlit-shield]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/
[Python-shield]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[NumPy-shield]: https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
