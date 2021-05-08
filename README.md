# Cat Scraper

This scraper scrapes a website for cats, and stores them into a file.

When it finds *new* cats, it sends a notification to a Telegram chat/channel.
You must configure the Telegram API token, and the channel you want to send it to.
This is done in `.env`.

It is tailor-made for a specific website, but you still have to fill its URL into `.env`.
