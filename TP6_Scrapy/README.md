## **Partie 5 : Sélecteurs CSS et XPath**
- Dans le shell

#### Voir l'URL actuelle
>>> response.url
'http://quotes.toscrape.com/'

#### Voir le code HTML
>>> print(response.text[:500])
<!DOCTYPE html>
<html lang="en">
<head>
        <meta charset="UTF-8">
        <title>Quotes to Scrape</title>
    <link rel="stylesheet" href="/static/bootstrap.min.css">
    <link rel="stylesheet" href="/static/main.css">


</head>
<body>
    <div class="container">
        <div class="row header-box">
            <div class="col-md-8">
                <h1>
                    <a href="/" style="text-decoration: none">Quotes to Scrape</a>
                </h1>
            </div>

#### Tester un nouveau sélecteur
>>> response.css('div.quote span.text::text').getall()
['“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”', '“It is our choices, Harry, that show what we truly are, far more than our abilities.”', '“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”', '“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”', "“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”", '“Try not to become a man of success. Rather become a man of value.”', '“It is better to be hated for what you are than to be loved for what you are not.”', "“I have not failed. I've just found 10,000 ways that won't work.”", "“A woman is like a tea bag; you never know how strong it is until it's in hot water.”", '“A day without sunshine is like, you know, night.”']

####Testez le sélecteur CSS
>>> response.css('h1::text').get()
'\n                    '

#### Testez le sélecteur XPath
>>> response.xpath('//h1/text()').get()
'\n                    '

#### Pour avoir un résultat plus propre (sans les espaces)
>>> response.css('h1::text').get().strip()
''

#### Ou avec XPath
>>> response.xpath('normalize-space(//h1)').get()
'Quotes to Scrape'

#### Testez d'autres sélecteurs
>>> response.css('title::text').get()
'Quotes to Scrape'
>>> response.xpath('//title/text()').get()
'Quotes to Scrape'

#### Pour voir tous les quotes
>>> quotes = response.css('div.quote')
>>> len(quotes)
10

#### Premier quote
>>> first_quote = quotes[0]
>>> first_quote.css('span.text::text').get()
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'
>>> first_quote.xpath('.//span[@class="text"]/text()').get()
'“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”'

#### L'auteur du premier quote
>>> first_quote.css('small.author::text').get()
'Albert Einstein'
>>> first_quote.xpath('.//small[@class="author"]/text()').get()
'Albert Einstein'

#### Les tags du premier quote
>>> first_quote.css('div.tags a.tag::text').getall()
['change', 'deep-thoughts', 'thinking', 'world']
>>> first_quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').getall()
['change', 'deep-thoughts', 'thinking', 'world']















