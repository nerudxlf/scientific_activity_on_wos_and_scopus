import pandas as pd


def list_to_upper_case(data_list: list) -> list:
    """
    Функция для изменения регистра названий в списке
    :param data_list: список с данными
    :return: возвращает новый список с элементами в новом регистре
    """
    return_list = []
    for i in data_list:
        return_list.append(i.upper())
    return return_list


def main():
    df_wos_citation = pd.read_excel("WoS.xls")
    df_wos_data = pd.read_excel("wos5.xlsx")
    df_oecd = pd.read_excel("OECD Category Mapping.xlsx")

    df_wos_citation.filter(["Название", "Всего цитат"])
    df_wos_data.filter(["Article Title", "WoS Categories"])
    join_df_by_title = pd.merge(left=df_wos_data, right=df_wos_citation, left_on="Article Title", right_on="Название")

    list_citation = join_df_by_title["Всего цитат"].to_list()
    list_research_areas = join_df_by_title["WoS Categories"].to_list()
    oecd_category_df_list = df_oecd['WoS_Description'].tolist()  # перевожу данные к списку

    result_dict = {}

    for i in range(len(list_research_areas)):
        if result_dict.get(list_research_areas[i]):
            result_dict[list_research_areas[i]] += list_citation[i]
        else:
            result_dict |= {list_research_areas[i]: list_citation[i]}

    oecd_category_df_list = list_to_upper_case(oecd_category_df_list)
    oecd_category_df_dict = dict.fromkeys(oecd_category_df_list)
    result_dict_upper_key = {}
    for key, item in result_dict.items():
        result_dict_upper_key |= {key.upper(): item}

    for key, item in oecd_category_df_dict.items():
        oecd_category_df_dict[key] = 0

    for key, item in oecd_category_df_dict.items():
        for key_old, item_old in result_dict_upper_key.items():
            if key_old == key:
                oecd_category_df_dict[key] += item_old

    result_df_value = pd.DataFrame(oecd_category_df_dict, index=['Количество']).T
    result_df_value["WoS Categories"] = result_df_value.index
    result_all = pd.merge(left_on="WoS_Description", right_on="WoS Categories", left=df_oecd,
                          right=result_df_value)
    result_all.drop("WoS Categories", axis=1, inplace=True)
    result_all.to_excel("result.xlsx", index=False)
