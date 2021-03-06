key_dict = {
    0: {'all_key': '既婚者', 'sub_key': '既婚者', 'sub': '既婚者', 's_sex': 'm', 's_ms': 'm', 'eng': 'married_person',
        'type': 'only_sub', 'o_sex': 'w'},
    1: {'all_key': '既婚', 'sub_key': '既婚', 'sub': '既婚男性', 's_sex': 'm', 's_ms': 'm', 'eng': 'married_man',
        'type': 'only_sub', 'o_sex': 'w'},
    2: {'all_key': '新婚', 'sub_key': '新婚', 'sub': '新婚男性', 's_sex': 'm', 's_ms': 'm', 'eng': 'newly_married_man',
        'type': 'only_sub', 'o_sex': 'w'},
    3: {'all_key': '妻子持ち', 'sub_key': '妻子持ち', 'sub': '妻子持ち男性', 's_sex': 'm', 's_ms': 'm', 'eng': 'man_with_wife',
        'type': 'only_sub', 'o_sex': 'w'},
    4: {'all_key': '彼女持ち', 'sub_key': '彼女持ち', 'sub': '彼女持ち男性', 's_sex': 'm', 's_ms': 's', 'eng': 'man_with_gf',
        'type': 'only_sub', 'o_sex': 'w'},
    5: {'all_key': 'バツイチ', 'sub_key': 'バツイチ', 'sub': 'バツイチ男性', 's_sex': 'm', 's_ms': 's', 'eng': 'man_with_wife',
        'type': 'only_sub', 'o_sex': 'w'},
    6: {'all_key': '独身', 'sub_key': '独身', 'sub': '独身男性', 's_sex': 'm', 's_ms': 's', 'eng': 'single', 'type': 'only_sub',
        'o_sex': 'w'},
    7: {'all_key': 'セックスレス', 'sub_key': 'セックスレス', 'sub': 'セックスレス男性', 's_sex': 'm', 's_ms': 'm', 'eng': 'sexless',
        'type': 'only_sub', 'o_sex': 'w'},
    8: {'all_key': '社会人', 'sub_key': '社会人', 'sub': '社会人', 's_sex': 'm', 's_ms': 's', 'eng': 'society',
        'type': 'only_sub', 'o_sex': 'w'},
    9: {'all_key': '学生', 'sub_key': '学生', 'sub': '学生', 's_sex': 'm', 's_ms': 's', 'eng': 'student', 'type': 'only_sub',
        'o_sex': 'w'},
    10: {'all_key': '大学生', 'sub_key': '大学生', 'sub': '大学生', 's_sex': 'm', 's_ms': 's', 'eng': 'university_student',
         'type': 'only_sub', 'o_sex': 'w'},
    11: {'all_key': '医師', 'sub_key': '医師', 'sub': '医師', 's_sex': 'm', 's_ms': 's', 'eng': 'doctor', 'type': 'only_sub',
         'o_sex': 'w'},
    12: {'all_key': '医者', 'sub_key': '医者', 'sub': '医者', 's_sex': 'm', 's_ms': 's', 'eng': 'doctor2', 'type': 'only_sub',
         'o_sex': 'w'},
    13: {'all_key': 'バイト', 'sub_key': 'バイト', 'sub': 'バイトの男性', 's_sex': 'm', 's_ms': 's', 'eng': 'part‐time_job',
         'type': 'only_sub', 'o_sex': 'w'},
    14: {'all_key': '経営者', 'sub_key': '経営者', 'sub': '経営者', 's_sex': 'm', 's_ms': 's', 'eng': 'manager',
         'type': 'only_sub', 'o_sex': 'w'},
    15: {'all_key': '公務員', 'sub_key': '公務員', 'sub': '公務員', 's_sex': 'm', 's_ms': 's', 'eng': 'public_service_worker',
         'type': 'only_sub', 'o_sex': 'w'},
    16: {'all_key': '高学歴', 'sub_key': '高学歴', 'sub': '高学歴', 's_sex': 'm', 's_ms': 's', 'eng': 'higher_education',
         'type': 'only_sub', 'o_sex': 'w'},
    17: {'all_key': '未成年', 'sub_key': '未成年', 'sub': '未成年', 's_sex': 'm', 's_ms': 's', 'eng': 'under_age',
         'type': 'only_sub', 'o_sex': 'w'},
    18: {'all_key': '10代', 'sub_key': '10代', 'sub': '10代男性', 's_sex': 'm', 's_ms': 's', 'eng': '10s',
         'type': 'only_sub', 'o_sex': 'w'},
    19: {'all_key': '20代', 'sub_key': '20代', 'sub': '20代男性', 's_sex': 'm', 's_ms': 's', 'eng': '20s',
         'type': 'only_sub', 'o_sex': 'w'},
    20: {'all_key': '30代', 'sub_key': '30代', 'sub': '30代男性', 's_sex': 'm', 's_ms': 's', 'eng': '30s',
         'type': 'only_sub', 'o_sex': 'w'},
    21: {'all_key': '40代', 'sub_key': '40代', 'sub': '40代男性', 's_sex': 'm', 's_ms': 's', 'eng': '40s',
         'type': 'only_sub', 'o_sex': 'w'},
    22: {'all_key': '50代', 'sub_key': '50代', 'sub': '50代男性', 's_sex': 'm', 's_ms': 's', 'eng': '50s',
         'type': 'only_sub', 'o_sex': 'w'},
    23: {'all_key': '60代', 'sub_key': '60代', 'sub': '60代男性', 's_sex': 'm', 's_ms': 's', 'eng': '60s',
         'type': 'only_sub', 'o_sex': 'w'},
    24: {'all_key': '70代', 'sub_key': '70代', 'sub': '70代男性', 's_sex': 'm', 's_ms': 's', 'eng': '70s',
         'type': 'only_sub', 'o_sex': 'w'},
    25: {'all_key': '高齢者', 'sub_key': '高齢者', 'sub': '高齢男性', 's_sex': 'm', 's_ms': 's', 'eng': 'aged_man',
         'type': 'only_sub', 'o_sex': 'w'},
    26: {'all_key': '中年', 'sub_key': '中年', 'sub': '中年男性', 's_sex': 'm', 's_ms': 's', 'eng': 'middle_aged_man',
         'type': 'only_sub', 'o_sex': 'w'},
    27: {'all_key': 'おっさん', 'sub_key': 'おっさん', 'sub': 'おっさん', 's_sex': 'm', 's_ms': 's', 'eng': 'uncle',
         'type': 'only_sub', 'o_sex': 'w'},
    28: {'all_key': 'アラサー', 'sub_key': 'アラサー', 'sub': 'アラサー男性', 's_sex': 'm', 's_ms': 's', 'eng': '30_something',
         'type': 'only_sub', 'o_sex': 'w'},
    29: {'all_key': 'アラフォー', 'sub_key': 'アラフォー', 'sub': 'アラフォー男性', 's_sex': 'm', 's_ms': 's', 'eng': '40_something',
         'type': 'only_sub', 'o_sex': 'w'},
    30: {'all_key': 'アラフィフ', 'sub_key': 'アラフィフ', 'sub': 'アラフィフ男性', 's_sex': 'm', 's_ms': 's', 'eng': '50_something',
         'type': 'only_sub', 'o_sex': 'w'},
    31: {'all_key': '熟年', 'sub_key': '熟年', 'sub': '熟年男性', 's_sex': 'm', 's_ms': 's', 'eng': 'mature_age',
         'type': 'only_sub', 'o_sex': 'w'},
    32: {'all_key': 'シニア', 'sub_key': 'シニア', 'sub': 'シニア男性', 's_sex': 'm', 's_ms': 's', 'eng': 'senior',
         'type': 'only_sub', 'o_sex': 'w'},
    33: {'all_key': '留学生', 'sub_key': '留学生', 'sub': '留学生', 's_sex': 'm', 's_ms': 's', 'eng': 'student_studying_abroad',
         'type': 'only_sub', 'o_sex': 'w'},
    34: {'all_key': '中国人', 'sub_key': '中国人', 'sub': '中国人', 's_sex': 'm', 's_ms': 's', 'eng': 'chinese',
         'type': 'only_sub', 'o_sex': 'w'},
    35: {'all_key': '韓国人', 'sub_key': '韓国人', 'sub': '韓国人', 's_sex': 'm', 's_ms': 's', 'eng': 'korean',
         'type': 'only_sub', 'o_sex': 'w'},
    36: {'all_key': '外国人', 'sub_key': '外国人', 'sub': '外国人', 's_sex': 'm', 's_ms': 's', 'eng': 'alien',
         'type': 'only_sub', 'o_sex': 'w'},
    37: {'all_key': 'A型', 'sub_key': 'A型', 'sub': 'A型男性', 's_sex': 'm', 's_ms': 's', 'eng': 'type_A',
         'type': 'only_sub', 'o_sex': 'w'},
    38: {'all_key': 'O型', 'sub_key': 'O型', 'sub': 'O型男性', 's_sex': 'm', 's_ms': 's', 'eng': 'type_O',
         'type': 'only_sub', 'o_sex': 'w'},
    39: {'all_key': 'B型', 'sub_key': 'B型', 'sub': 'B型男性', 's_sex': 'm', 's_ms': 's', 'eng': 'type_B',
         'type': 'only_sub', 'o_sex': 'w'},
    40: {'all_key': 'AB型', 'sub_key': 'AB型', 'sub': 'AB型男性', 's_sex': 'm', 's_ms': 's', 'eng': 'type_AB',
         'type': 'only_sub', 'o_sex': 'w'},
    41: {'all_key': '初心者', 'sub_key': '初心者', 'sub': '初心者', 's_sex': 'm', 's_ms': 's', 'eng': 'beginner',
         'type': 'only_sub', 'o_sex': 'w'},
    42: {'all_key': 'ヤリチン', 'sub_key': 'ヤリチン', 'sub': 'ヤリチン男性', 's_sex': 'm', 's_ms': 's', 'eng': 'man_whore',
         'type': 'only_sub', 'o_sex': 'w'},
    43: {'all_key': 'デブ', 'sub_key': 'デブ', 'sub': 'デブ', 's_sex': 'm', 's_ms': 's', 'eng': 'fatty', 'type': 'only_sub',
         'o_sex': 'w'},
    44: {'all_key': 'オタク', 'sub_key': 'オタク', 'sub': 'オタク', 's_sex': 'm', 's_ms': 's', 'eng': 'otaku',
         'type': 'only_sub', 'o_sex': 'w'},
    45: {'all_key': '地方在住', 'sub_key': '地方在住', 'sub': '地方在住男性', 's_sex': 'm', 's_ms': 's', 'eng': 'country_folk',
         'type': 'only_sub', 'o_sex': 'w'},
    46: {'all_key': 'アラカン', 'sub_key': 'アラカン', 'sub': 'アラカン男性', 's_sex': 'm', 's_ms': 's', 'eng': 'arakan',
         'type': 'only_sub', 'o_sex': 'w'},
    47: {'all_key': '無職', 'sub_key': '無職', 'sub': '無職男性', 's_sex': 'm', 's_ms': 's', 'eng': 'unemployed',
         'type': 'only_sub', 'o_sex': 'w'},
    48: {'all_key': 'ニート', 'sub_key': 'ニート', 'sub': 'ニート男性', 's_sex': 'm', 's_ms': 's', 'eng': 'neat',
         'type': 'only_sub', 'o_sex': 'w'},
    49: {'all_key': 'おじいさん', 'sub_key': 'おじいさん', 'sub': 'おじいさん', 's_sex': 'm', 's_ms': 's', 'eng': 'old_man',
         'type': 'only_sub', 'o_sex': 'w'},
    50: {'all_key': 'ブサイク', 'sub_key': 'ブサイク', 'sub': '不細工男性', 's_sex': 'm', 's_ms': 's', 'eng': 'bacik',
         'type': 'only_sub', 'o_sex': 'w'},
    51: {'all_key': '単身赴任', 'sub_key': '単身赴任', 'sub': '単身赴任男性', 's_sex': 'm', 's_ms': 'm', 'eng': 'one_way',
         'type': 'only_sub', 'o_sex': 'w'},
    52: {'all_key': '人見知り', 'sub_key': '人見知り', 'sub': '人見知り男性', 's_sex': 'm', 's_ms': 's', 'eng': 'indiscriminate',
         'type': 'only_sub', 'o_sex': 'w'},
    53: {'all_key': '奥手', 'sub_key': '奥手', 'sub': '奥手男性', 's_sex': 'm', 's_ms': 's', 'eng': 'forth', 'type': 'only_sub',
         'o_sex': 'w'},
    54: {'all_key': 'コミュ障', 'sub_key': 'コミュ障', 'sub': 'コミュ障男性', 's_sex': 'm', 's_ms': 's', 'eng': 'communess',
         'type': 'only_sub', 'o_sex': 'w'},
    55: {'all_key': '肥満', 'sub_key': '肥満', 'sub': '肥満男性', 's_sex': 'm', 's_ms': 's', 'eng': 'obesity',
         'type': 'only_sub', 'o_sex': 'w'},
    56: {'all_key': '虚弱体質', 'sub_key': '虚弱体質', 'sub': '虚弱体質男性', 's_sex': 'm', 's_ms': 's', 'eng': 'frail_quality',
         'type': 'only_sub', 'o_sex': 'w'},
    57: {'all_key': '包茎', 'sub_key': '包茎', 'sub': '包茎男性', 's_sex': 'm', 's_ms': 's', 'eng': 'forgotism',
         'type': 'only_sub', 'o_sex': 'w'},
    58: {'all_key': '素人童貞', 'sub_key': '素人童貞', 'sub': '素人童貞', 's_sex': 'm', 's_ms': 's', 'eng': 'amateur_virgin',
         'type': 'only_sub', 'o_sex': 'w'},
    59: {'all_key': '引きこもり', 'sub_key': '引きこもり', 'sub': '引きこもり男性', 's_sex': 'm', 's_ms': 's',
         'eng': 'social_withdrawal', 'type': 'only_sub', 'o_sex': 'w'},
    60: {'all_key': '高卒', 'sub_key': '高卒', 'sub': '高卒男性', 's_sex': 'm', 's_ms': 's', 'eng': 'high_school_graduate',
         'type': 'only_sub', 'o_sex': 'w'},
    61: {'all_key': '中卒', 'sub_key': '中卒', 'sub': '中卒男性', 's_sex': 'm', 's_ms': 's', 'eng': 'middle_school',
         'type': 'only_sub', 'o_sex': 'w'},
    62: {'all_key': 'フリーター', 'sub_key': 'フリーター', 'sub': 'フリーター男性', 's_sex': 'm', 's_ms': 's', 'eng': 'freeter',
         'type': 'only_sub', 'o_sex': 'w'},
    63: {'all_key': 'アニオタ', 'sub_key': 'アニオタ', 'sub': 'アニオタ男子', 's_sex': 'm', 's_ms': 's', 'eng': 'aniota',
         'type': 'only_sub', 'o_sex': 'w'},
    64: {'all_key': 'ドルオタ', 'sub_key': 'ドルオタ', 'sub': 'ドルオタ男子', 's_sex': 'm', 's_ms': 's', 'eng': 'dolta',
         'type': 'only_sub', 'o_sex': 'w'},
    65: {'all_key': 'ストーカー', 'sub_key': 'ストーカー', 'sub': 'ストーカー男性', 's_sex': 'm', 's_ms': 's', 'eng': 'stalker',
         'type': 'only_sub', 'o_sex': 'w'},
    66: {'all_key': 'フェチ', 'sub_key': 'フェチ', 'sub': 'フェチ男性', 's_sex': 'm', 's_ms': 's', 'eng': 'fetish',
         'type': 'only_sub', 'o_sex': 'w'},
    67: {'all_key': 'おっぱい星人', 'sub_key': 'おっぱい星人', 'sub': 'おっぱい星人', 's_sex': 'm', 's_ms': 's', 'eng': 'tits_alien',
         'type': 'only_sub', 'o_sex': 'w'},
    68: {'all_key': '根暗', 'sub_key': '根暗', 'sub': 'ネクラ男性', 's_sex': 'm', 's_ms': 's', 'eng': 'dark', 'type': 'only_sub',
         'o_sex': 'w'},
    69: {'all_key': '障害者', 'sub_key': '障害者', 'sub': '障害者男性', 's_sex': 'm', 's_ms': 's', 'eng': 'handicapped',
         'type': 'only_sub', 'o_sex': 'w'},
    70: {'all_key': '認知症', 'sub_key': '認知症', 'sub': '認知症男性', 's_sex': 'm', 's_ms': 's', 'eng': 'dementia',
         'type': 'only_sub', 'o_sex': 'w'},
    71: {'all_key': '発達障害', 'sub_key': '発達障害', 'sub': '発達障害男性', 's_sex': 'm', 's_ms': 's',
         'eng': 'developmental_disorder', 'type': 'only_sub', 'o_sex': 'w'},
    72: {'all_key': 'メンタル', 'sub_key': 'メンタル', 'sub': 'メンヘラ男子', 's_sex': 'm', 's_ms': 's', 'eng': 'mental',
         'type': 'only_sub', 'o_sex': 'w'},
    73: {'all_key': 'うつ病', 'sub_key': 'うつ病', 'sub': 'うつ病男子', 's_sex': 'm', 's_ms': 's', 'eng': 'depression',
         'type': 'only_sub', 'o_sex': 'w'},
    74: {'all_key': '貧困', 'sub_key': '貧困', 'sub': '貧乏男性', 's_sex': 'm', 's_ms': 's', 'eng': 'poverty',
         'type': 'only_sub', 'o_sex': 'w'},
    75: {'all_key': 'ネカフェ難民', 'sub_key': 'ネカフェ難民', 'sub': 'ネカフェ難民', 's_sex': 'm', 's_ms': 's', 'eng': 'nekafe_refugee',
         'type': 'only_sub', 'o_sex': 'w'},
    76: {'all_key': '住所不定', 'sub_key': '住所不定', 'sub': '住所不定男性', 's_sex': 'm', 's_ms': 's', 'eng': 'addressless',
         'type': 'only_sub', 'o_sex': 'w'},
    77: {'all_key': '派遣社員', 'sub_key': '派遣社員', 'sub': '男性派遣社員', 's_sex': 'm', 's_ms': 's', 'eng': 'dispatched_employee',
         'type': 'only_sub', 'o_sex': 'w'},
    78: {'all_key': 'オヤジ', 'sub_key': 'オヤジ', 'sub': 'オヤジ', 's_sex': 'm', 's_ms': 's', 'eng': 'father',
         'type': 'only_sub', 'o_sex': 'w'},
    79: {'all_key': '非モテ', 'sub_key': '非モテ', 'sub': '非モテ男性', 's_sex': 'm', 's_ms': 's', 'eng': 'non_mote',
         'type': 'only_sub', 'o_sex': 'w'},
    80: {'all_key': '期間工', 'sub_key': '期間工', 'sub': '期間工男性', 's_sex': 'm', 's_ms': 's', 'eng': 'period_of_time',
         'type': 'only_sub', 'o_sex': 'w'},
    81: {'all_key': '低所得', 'sub_key': '低所得', 'sub': '低所得男性', 's_sex': 'm', 's_ms': 's', 'eng': 'low_income',
         'type': 'only_sub', 'o_sex': 'w'},
    82: {'all_key': '孤独', 'sub_key': '孤独', 'sub': '孤独男子', 's_sex': 'm', 's_ms': 's', 'eng': 'loneliness',
         'type': 'only_sub', 'o_sex': 'w'},
    83: {'all_key': '彼女いない歴=年齢', 'sub_key': '彼女いない歴=年齢', 'sub': '彼女いない歴=年齢の男性', 's_sex': 'm', 's_ms': 's',
         'eng': 'less_equal_age', 'type': 'only_sub', 'o_sex': 'w'},
    84: {'all_key': '陰キャラ', 'sub_key': '陰キャラ', 'sub': '陰キャ男子', 's_sex': 'm', 's_ms': 's', 'eng': 'dark_character',
         'type': 'only_sub', 'o_sex': 'w'},
    85: {'all_key': '職人', 'sub_key': '職人', 'sub': '職人男性', 's_sex': 'm', 's_ms': 's', 'eng': 'craftsman',
         'type': 'only_sub', 'o_sex': 'w'},
    86: {'all_key': '肉体労働', 'sub_key': '肉体労働', 'sub': '肉体労働男性', 's_sex': 'm', 's_ms': 's', 'eng': 'manual_labor',
         'type': 'only_sub', 'o_sex': 'w'},
    87: {'all_key': 'バツあり', 'sub_key': 'バツあり', 'sub': 'バツあり男子', 's_sex': 'm', 's_ms': 's', 'eng': 'there_is_a_plump',
         'type': 'only_sub', 'o_sex': 'w'}
}
