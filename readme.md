<h1 align="center">Danielino Google Takeout Downloader</h1>

<p align="center">
  <strong>Automate and streamline your Google Takeout download process.</strong>
</p>

<hr/>

<h2>Overview</h2>
<p>
  [Guarda il video su YouTube](https://youtube.com/watch?v=34gGnnnN138)
  The <strong>Danielino Google Takeout Downloader</strong> is a Python-based tool designed to automate and simplify the downloading of Google Takeout archives. It efficiently manages common issues like download interruptions, failures, and file tracking. The tool logs in automatically, handles two-factor authentication, and resumes downloads if interrupted.
</p>
<p><em>Note:</em> This software was developed quickly to meet a personal need and may contain bugs. It is provided as-is, with the hope that it may be useful or serve as a basis for further development.</p>

<h2>Features</h2>
<ul>
  <li><strong>Automated Download Resumption:</strong> Automatically resumes downloads from where they left off if interrupted.</li>
  <li><strong>Two-Factor Authentication Support:</strong> Handles Google's two-factor authentication, making it easier to download large sets of data.</li>
  <li><strong>Download Management:</strong> Keeps track of downloaded and pending files using a local database.</li>
  <li><strong>Masked Browser Automation:</strong> Uses a masked Chromium browser to bypass Google's download interruptions.</li>
</ul>

<h2>Requirements</h2>
<ul>
  <li><strong>Operating System:</strong> Tested on Windows. Functionality on Linux is unknown.</li>
  <li><strong>Python Version:</strong> Tested with Python 3.11.</li>
</ul>

<h2>Installation</h2>
<ol>
  <li><strong>Clone the Repository:</strong>
    <pre><code>git clone https://github.com/DanielsaanCodes/DanielinoGTakeout_Downloader_v2.git
cd Danielino_GoogleTakeout_Downloader</code></pre>
  </li>

  <li><strong>Create and Activate a Virtual Environment (Recommended):</strong>
    <pre><code>python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`</code></pre>
  </li>

  <li><strong>Install Dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>

  <li><strong>Configure the <code>.env</code> File:</strong>
    <p>Create a <code>.env</code> file in the root directory and add your Google account password and two-factor authentication key:</p>
    <pre><code>GOOGLE_PASSWORD=your_google_password
G2FA_KEY=your_2fa_key</code></pre>
  </li>
</ol>

<h2>Usage Instructions</h2>

<ol>
  <li><strong>Prepare Your Google Takeout Email:</strong>
    <ul>
      <li>Open the Google Takeout email in your browser -> [Watch video on YouTube](https://youtube.com/watch?v=34gGnnnN138).</li> 
      <li>Save the email as an HTML file.</li>
      <li>Place the saved file in the <code>htmlstarter</code> folder and rename it to <code>mailButtons.html</code>.</li>
    </ul>
  </li>

  <li><strong>Starting the Downloader:</strong>
    <p>When you first run the script, you'll be prompted to choose an option:</p>
    <ul>
      <li>Press <strong>1</strong> to reset the database and start a new download session. This will delete previous progress and allow you to start fresh.</li>
      <li>Press <strong>2</strong> to resume downloads from where they left off using the existing database.</li>
    </ul>
    <pre><code>python main.py</code></pre>
    <p>Downloads will be saved in the <code>downloads</code> folder. If the download is interrupted, the script will automatically resume from the last successful download.</p>
  </li>
</ol>

<h2>Two-Factor Authentication Setup</h2>
<p>To use the downloader, you need to set up two-factor authentication with Google:</p>
<ol>
  <li><strong>Go to Google Security Settings:</strong>
    <p>Navigate to your Google account's security settings.</p>
  </li>

  <li><strong>Add a New App for Two-Factor Authentication:</strong>
    <p>Generate a new app-specific password.</p>
  </li>

  <li><strong>Insert the 2FA Key in the <code>.env</code> File:</strong>
    <p>Use the key generated in the previous step.</p>
  </li>

  <li><strong>Verify the 2FA Key:</strong>
    <p>To get the verification code, use the function <code>getCode(g2fa_key)</code> provided in the code or input the key into an authenticator app (like Google Authenticator or Twilio Authy).</p>
    <p><em>Important:</em> Ensure the key is added both to the <code>.env</code> file and your authenticator app before saving your Google account settings.</p>
  </li>

  <li><strong>Automatic 2FA Handling:</strong>
    <p>The downloader will automatically handle the 2FA challenge during the download process.</p>
  </li>
</ol>

<h2>Support and Feedback</h2>
<p>If you encounter bugs or have suggestions for improvement, please let me know by opening an issue in the GitHub repository.</p>

<h2>Support My Work</h2>
<p>If you find this tool helpful, consider supporting me by subscribing to my YouTube channel: <a href="https://www.youtube.com/@Daanielsan" target="_blank">Daanielsan</a>.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License. Feel free to use and modify it as needed.</p>

<p><strong>Remember to leave a star on GitHub if you find this tool useful!</strong></p>
