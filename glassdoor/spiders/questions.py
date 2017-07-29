import re
import scrapy


GLASSDOOR_DOMAIN = 'https://www.glassdoor.com'


def clean(s):
    return re.sub(r'\xa0', ' ', s)


def has_no_answers(element):
    return element.css('a::text').extract_first().strip() == 'Answer Question'


def has_nda(element):
    return re.search(r'\bNDA\b', element) is not None


class QuestionSpider(scrapy.Spider):
    name = 'questions'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = (kwargs['url'],)

    def parse(self, response):
        for review in response.css('.empReview.cf'):
            role = review.css('h2.summary').xpath('string(.)').extract_first()

            for element in review.css('.interviewQuestion'):
                question = '\n'.join(
                    clean(x).strip()
                    for x in element.xpath('text()').extract()
                )

                answers_url = GLASSDOOR_DOMAIN + \
                    element.css('a').xpath('@href').extract_first()

                if has_nda(question):
                    continue

                obj = {
                    'role': role,
                    'question': question,
                    'answers': [],
                    'answers_url': answers_url,
                }

                if has_no_answers(element):
                    yield obj
                else:
                    request = scrapy.http.Request(
                        answers_url,
                        callback=self.parse_answers,
                        meta=obj,
                    )
                    request.meta['obj'] = obj
                    yield request

        next_page = response.css('li.next > a').xpath('@href').extract_first()
        if next_page:
            yield scrapy.http.Request(GLASSDOOR_DOMAIN + next_page)

    def parse_answers(self, response):
        obj = response.meta['obj']

        for comment in response.css('.commentText'):
            answer = '\n'.join(
                clean(line).rstrip()
                for line in comment.xpath('text()').extract()
            )
            if answer:
                obj['answers'].append(answer)

        yield obj
