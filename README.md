# What does this thing do?

Given a Glassdoor url, this will extract interview questions (and answers).

# Requirements

- Python 3+
- Scrapy


# Usage

```shell
$ scrapy crawl -a url=<< glassdoor url >>
```

**Note:** The url should have this form: `https://www.glassdoor.com/Interview/*.html`.

Results will be stored in `/tmp/output.json'`.

Output example:

```json
{
  "questions": "...",
  "role": "...",
  "answers": [...],
  "answers_url": "..."
}
```
