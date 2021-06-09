correct_dict = {
    'わけためね': 'ことになりますからね',
    '実際にの': '現実での',
    'なから': 'ですから',
    'わためない': '分からない',
    '付き合いない': '交流がない',
    'そのですから': 'そのため',
    'できるですから': 'できるため',
    '最初て': '最初に',
    '自己解説': '自己紹介',
    '自己説明': '自己紹介',
    '利用目当て': '利用目的',
    '利用狙い': '利用目的',
    'メールの話': 'メールでの会話',
    'ますですから': 'ますので'

}

word_dict = [
    {'before': '<!--bitch-->',
     'after': ['ヤリマン', 'ビッチ', 'アバズレ']},
    {'before': '<!--a-margin-->',
     'after': ['余力', '余裕']},
    {'before': '<!--clear-->',
     'after': ['クリア', '達成']},
    {'before': '<!--gentle-->',
     'after': ['丁寧', '紳士的']},
    {'before': '<!--no-plb-->',
     'after': ['安心して', '心配しないで']},
    {'before': '<!--unrelated-->',
     'after': ['関係ない', '無関係']},
    {'before': '<!--can-say-->',
     'after': ['と言えます', 'と考えられます', 'と判断してOKです']},
    {'before': '<!--tel-check-->',
     'after': ['電話番号確認', '電話番号認証', '番号確認', '電話認証']},
    {'before': '<!--in-this-time-->',
     'after': ['する際に', 'する時に', 'する時点で']},
    {'before': '<!--foully-use-->',
     'after': ['不正利用', '不正な利用', '不正な使用', '不正使用']},
    {'before': '<!--template-->',
     'after': ['テンプレート', 'テンプレ']},
    {'before': '<!--can-see-->',
     'after': ['閲覧できる', '見ることができる']},
    {'before': '<!--refer-to-->',
     'after': ['参考にして', '参照して', '見てみて']},
    {'before': '<!--is-many-way-->',
     'after': ['いろいろあります', 'たくさんあります', '複数あります']},
    {'before': '<!--in-general-->',
     'after': ['通常の', '普通の', '一般的な']},
    {'before': '<!--than-usual-->',
     'after': ['通常より', '普通より', '一般より']},
    {'before': '<!--be-start-->',
     'after': ['スタートしま', '始まりま']},
    {'before': '<!--check-->',
     'after': ['チェック', '確認']},
    {'before': '<!--pro-check-->',
     'after': ['プロフのチェック', 'プロフィール閲覧']},
    {'before': '<!--pro-check1-->',
     'after': ['プロフィールのチェック', 'プロフ覧']},
    {'before': '<!--pro-check2-->',
     'after': ['プロフチェック', 'プロフィールの閲覧']},
    {'before': '<!--pro-check3-->',
     'after': ['プロフィールチェック', 'プロフの閲覧']},
    {'before': '<!--search-sf-->',
     'after': ['セフレ探し', 'セックスフレンド作り']},
    {'before': '<!--easy-to-sf-->',
     'after': ['セフレにしやすい', '<!--easily-->セフレにできる']},
    {'before': '<!--easy-to-sf-s-->',
     'after': ['セフレにしやすいです', '<!--easily-->セフレにできます']},
    {'before': '<!--how-->',
     'after': ['どんな', 'どういう', 'どのような']},
    {'before': '<!--writing-text-->',
     'after': ['文章を書く', '作文する']},
    {'before': '<!--easy-writing-->',
     'after': ['メールが楽に作れる', '<!--easily-->メールが書ける']},
    {'before': '<!--caution-n-->',
     'after': ['警戒', '用心']},
    {'before': '<!--show-you-way-->',
     'after': ['お教えします', 'ご教授します', '伝授致します']},
    {'before': '<!--you-can-use-->',
     'after': ['ご用意しています', '用意しています', '準備しています', 'ご利用いただけます']},
    {'before': '<!--one-at-a-time-->',
     'after': ['一人一人', '一人ずつ', '一人ずつ順番に']},
    {'before': '<!--check-prf-->',
     'after': ['プロフを見て', 'プロフィールをチェックして']},
    {'before': '<!--check-prf2-->',
     'after': ['プロフィールを見て', 'プロフをチェックして']},

]

ignore_words = ['から', 'ので', 'いい', '良い', 'ため']
