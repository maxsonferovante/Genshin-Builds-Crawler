from GenshinBuildsCrawler.genshinBuildsCrawler import GenBuildsCrawler


def run():
    url = 'https://genshin-builds.com/pt'
    crawler = GenBuildsCrawler(url)
    crawler.download_url()
    crawler.get_information_response_html()
    print(crawler.dictWeapon.keys())


if __name__ == '__main__':
    run()
