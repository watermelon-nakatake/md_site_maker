import words_dict
import make_new_resource as mr
import make_new_article


def translate_single_sentence_to_source(md_str, keywords, ignore_words, replace_list):
    key_phrase_dict = make_new_article.make_keywords_sample_dict(keywords)
    mr.list_duplication_check(words_dict.noun_list)
    print(key_phrase_dict)
    conj_dict = mr.make_word_dict(words_dict.conj_list, ignore_words)
    conj_list = sorted(conj_dict.keys(), key=lambda x: len(x), reverse=True)
    # print(conj_dict)
    noun_dict = mr.make_word_dict(words_dict.noun_list, ignore_words)
    noun_list = sorted(noun_dict.keys(), key=lambda x: len(x), reverse=True)
    omit_list = mr.make_omit_list(words_dict.noun_list)
    # print(noun_list)
    result = mr.sentence_filter(md_str, conj_dict, conj_list, noun_dict, noun_list, key_phrase_dict, omit_list,
                                ignore_words, replace_list).replace('#', '')
    print('\n\n' + result)


if __name__ == '__main__':
    m_str = '当サイトでおすすめしている出会い系サイトを使えば、女性はメールを何通送っても完全に無料で広告代理店のセフレを探すことができます。'

    k_p = {
        's_adj': '普通の', 'sub': '女性',
        'o_adj': 'センスのいい', 'obj': '広告代理店社員', 'obj_key': '広告代理店', 'obj_p': 'の',
        'act_adj': '安全に', 'act': 'セフレを作る', 'act_noun': 'セフレ', 'act_noun_flag': True,
        'act_connection': ['セフレ関係'], 'a_adj': '確実に', '2act_w': 'セックスする', '2act_noun': 'セックス',
        'o_reason': '',
        'o_sex': 'm', '_age': 'n', 'o_cat': 'j', 'act_code': 'gf',
        'hot_month': '8月', 'hot_season': '8月', 'hot_month_next': '8月'}
    translate_single_sentence_to_source(m_str, k_p, [], [])
