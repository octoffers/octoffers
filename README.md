# Octoffers

Octoffers is a community-driven project that simplifies job searching.
We manually integrate top career platforms, making it easy to auto-apply to jobs
with just a few clicks. Our open-source tool is free, efficient, and designed to help job seekers like you.


<img src="./.assets/octoffers_mascot.png" align="right" width="50%">

## Supported Platforms
| Platform      | Type    | Status            |
|---------------|---------|-------------------|
| Djinni        | Public  | Complete          |
| Indeed        | Private | Beta              |
| ZipRecruiter  | Private | Complete          |
| WorkBC        | Public  | ToDo              |
| Monster       | Public  | ToDo              |

## Requirements
- **python 3.9+**
- **chrome webdriver**
- **sqlite3**

<br>
<hr>

## Quick start
1) **Install package with pip**
`pip install octoffers`
2) **Pull Private Drivers** (if you have access)
```bash
git clone $PRIVATE_DRIVER_ORIGIN
cd $PRIVATE_DRIVER_REPOSITORY
pip install .
```
3) **Use Octoffers**
`octoffers help`

## How to use this

### ZipRecruiter

- **Fetch 3 pages of job postings**
```bash
octoffers ziprecruiter fetch "Software Engineer" --pages 3
```

- **Apply to all available jobs from ZipRecruiter**
```bash
octoffers ziprecruiter apply
```

### Djinni

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
DJINNI_SESSION_ID=[djinni_session_id] # Cookies
MOCK_EMAILADDR="jhondoe@gmail.com"
INDEED_REGION="ca"
ZIPRECRUITER_SESSION=[ziprecruiter_session] # Cookies
PYTHONBREAKPOINT=ipdb.set_trace # Debugging with ipdb
```

### Questions & Anwsers
- **Q:** Does Octoffers offer customization of applications or cover letters, or is it more of a basic submission tool?
    - **A:** Customization depends on the driver, if specific career platform is hard to automate, most likely that `apply()` submission method will be more basic.
- **Q:** What is the success rate of Octoffers applications compared to manual ones?
    - **A:** It depends on the role that you're applying for,

### Data Visualization

#### Star History

<a href="https://star-history.com/#octoffers/octoffers&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=octoffers/octoffers&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=octoffers/octoffers&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=octoffers/octoffers&type=Date" />
 </picture>
</a>
