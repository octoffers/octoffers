# Octoffers

Octoffers is a community-driven project that simplifies job searching.
We manually integrate top career platforms, making it easy to auto-apply to jobs
with just a few clicks. Our open-source tool is free, efficient, and designed to help job seekers like you.


<img src="./.assets/octoffers_mascot.png" align="right" width="50%">

### Supported Platforms
| Platform      | Type    | Status            |
|---------------|---------|-------------------|
| Djinni        | Public  | Complete          |
| Indeed        | Private | Beta              |
| ZipRecruiter  | Private | Under Development |
| WorkBC        | Public  | ToDo              |
| Monster       | Public  | ToDo              |

### Requirements
- **python 3.9+**
- **chrome webdriver**
- **sqlite3**

<br>
<hr>

### Why would you use Octoffers

- **Save countless hours:** Focus on preparing for interviews instead of tedious job hunting tasks.
- Increase your application success rate: Stand out from the crowd with AI-powered cover letters and personalized messages.
- Apply to more jobs efficiently: Octoffers can handle the heavy lifting, allowing you to focus on jobs that truly interest you.
- Open-source and customizable: Contribute to the project's development and customize it to your specific needs.

### Quick start
1) **Install required dependency**
`pip install -r requirements.txt`
2) **Pull Private Drivers** (if you have access)
`git submodule update --init --recursive`
3) **Use OctOffers**
`python octoffers`

### Example use cases
- **Fetch about 50 jobs from djinni**
```bash
python octoffers djinni fetch devops --pages 5
```
- **Apply to all available jobs from djinni**
```bash
python octoffers djinni apply "Hello, I'm looking for job" # <-- This argument stands for cover letter
```

### `.env` sample
```env
DJINNI_SESSION_ID=".2193dhsa9h419d1"
MOCK_EMAILADDR="jhondoe@gmail.com"
INDEED_REGION="ca"
```

### Questions & Anwsers
- **Q:** Does Octoffers offer customization of applications or cover letters, or is it more of a basic submission tool?
    - **A:** Customization depends on the driver, if specific career platform is hard to automate, most likely that `apply()` submission method will be more basic.
- **Q:** What is the success rate of Octoffers applications compared to manual ones?
    - **A:** It depends on the role that you're applying for,

### Data Visualization

#### Star History

<a href="https://star-history.com/#init64/octoffers&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=init64/octoffers&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=init64/octoffers&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=init64/octoffers&type=Date" />
 </picture>
</a>
