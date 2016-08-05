import wikipedia


def get_overview(company_name="TIS株式会社", company_address=""):
    wikipedia.set_lang("ja")
    # query = wikipedia.search(company_name, company_address)
    try:
        return wikipedia.summary(company_name, company_address)
    except:
        raise


if __name__ == '__main__':
    print(get_overveiw("大阪駅"))
    print(get_overveiw(company_name="大阪駅", company_address="〒160-0023 東京都新宿区西新宿8丁目17番1号 住友不動産新宿グランドタワー"))
    print(get_overveiw(company_name="TIS株式会社", company_address="〒160-0023 東京都新宿区西新宿8丁目17番1号 住友不動産新宿グランドタワー"))
    print(get_overveiw(company_name="TIS", company_address="〒160-0023 東京都新宿区西新宿8丁目17番1号 住友不動産新宿グランドタワー"))
    print(get_overveiw(company_name="TIS株式会社"))
    print(get_overveiw(company_name="TIS株式会社", company_address="企業"))
