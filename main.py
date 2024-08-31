from GenshinBuildsCrawler.genshinBuildsCrawler import GenBuildsCrawler


def run():
    url = 'https://genshin-builds.com/pt'
    crawler = GenBuildsCrawler(url)
    crawler.download_url()
    crawler.get_information_response_html()
    crawler.dictCharacter
    print(crawler.dictCharacter.keys())


if __name__ == '__main__':
    run()
