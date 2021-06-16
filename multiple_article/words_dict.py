# -*- coding: utf-8 -*-

noun_list = [{'before': '<!--sefure-->',
              'after': ['セフレ', 'セックスフレンド'],
              'plist': [0.8, 0.2]},
             {'before': '<!--sex-->',
              'after': ['セックス', 'SEX', 'エッチ', 'H'],
              'plist': [0.4, 0.2, 0.3, 0.1]},
             {'before': '<!--man-->',
              'after': ['男性', '男'],
              'plist': [0.9, 0.1]},
             {'before': '<!--profile-->',
              'after': ['プロフィール', 'プロフ']},
             {'before': '<!--mail-->',
              'after': ['メール', 'メッセージ', 'DM']},
             {'before': '<!--send-mail-->',
              'after': ['メールする', 'メッセージを送る']},
             {'before': '<!--h-2-->',
              'after': ['エッチ', 'H', 'スケベ']},
             {'before': '<!--hな-->',
              'after': ['エッチな', 'Hな', 'スケべな', 'エロい'],
              'plist': [0.4, 0.1, 0.1, 0.4]},
             {'before': '<!--ero-n-->',
              'after': ['エロ', 'エッチ', 'スケベ']},
             {'before': '<!--post-->',
              'after': ['書き込み', '書込み', '投稿']},
             {'before': '<!--d-app-->',
              'after': ['出会いアプリ', '出会い系アプリ']},
             {'before': '<!--site-->',
              'after': ['サイト', '出会い系サイト'],
              'plist': [0.7, 0.3]},
             {'before': '<!--deaikei-->',
              'after': ['出会い系サイト', '出会い系']},
             {'before': '<!--way-->',
              'after': ['方法', 'やり方'],
              'plist': [0.6, 0.4]},
             {'before': '<!--wife-->',
              'after': ['人妻', '既婚女性'],
              'plist': [0.6, 0.4]},
             {'before': '<!--hotel-->',
              'after': ['ラブホテル', 'ホテル', 'ラブホ']},
             {'before': '<!--line-->',
              'after': ['ライン', 'LINE'],
              'plist': [0.4, 0.6]},
             {'before': '<!--furin-->',
              'after': ['不倫', '浮気', '婚外恋愛']},
             {'before': '<!--net-d-->',
              'after': ['ネットの出会い', 'ネトナン', 'ネットナンパ'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--date-->',
              'after': ['デート', '面接']},
             {'before': '<!--looks-->',
              'after': ['ルックス', '見た目', '外見', '見た目のスペック', 'イケメンかブサメンか']},
             {'before': '<!--s-can-->',
              'after': ['できます', '可能です']},
             {'before': '<!--episode-->',
              'after': ['体験談', '経験談', 'レビュー'],
              'plist': [0.6, 0.3, 0.1]},
             {'before': '<!--site-user-->',
              'after': ['会員', '利用者', 'サイト利用者']},
             {'before': '<!--user-->',
              'after': ['女性会員', '女性利用者', '女子会員']},
             {'before': '<!--beauty-->',
              'after': ['美人', '美女', '美形'],
              'plist': [0.5, 0.4, 0.1]},
             {'before': '<!--reader-->',
              'after': ['方', '男性', '人'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--there-is-->',
              'after': ['いる', 'いらっしゃる'],
              'plist': [0.4, 0.6]},
             {'before': '<!--serious-->',
              'after': ['真面目な出会い', '本命の出会い', '真剣交際', '本気の出会い', '本命の恋愛'],
              'plist': [0.4, 0.2, 0.1, 0.1, 0.2]},
             {'before': '<!--ero-->',
              'after': ['エロくて', 'エッチで', 'いやらしくて', 'スケベで'],
              'plist': [0.4, 0.3, 0.1, 0.2],
              'omit': ['エッチできる']},
             {'before': '<!--make-->',
              'after': ['の作り方', 'の探し方', 'を作る方法', 'を探す方法'],
              'plist': [0.5, 0.1, 0.3, 0.1]},
             {'before': '<!--technique-->',
              'after': ['テクニック', '技術', '技'],
              'plist': [0.6, 0.3, 0.1]},
             {'before': '<!--internet-->',
              'after': ['ネット', 'インターネット'],
              'plist': [0.7, 0.3]},
             {'before': '<!--husband2-->',
              'after': ['旦那', '旦那さん', '夫', '配偶者'],
              'plist': [0.3, 0.2, 0.3, 0.2]},
             {'before': '<!--no-good-->',
              'after': ['ブサイクな', 'ブサメンの', 'イケメンじゃない'],
              'plist': [0.5, 0.2, 0.3]},
             {'before': '<!--no-good-w-->',
              'after': ['ブサイク', 'ブス', 'デブス'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--girl-friend-->',
              'after': ['彼女', '恋人'],
              'plist': [0.7, 0.3]},
             {'before': '<!--boy-friend-->',
              'after': ['彼氏', '恋人'],
              'plist': [0.7, 0.3]},
             {'before': '<!--marriage-->',
              'after': ['婚活', '結婚相手探し', '結婚相手募集'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--condom-->',
              'after': ['コンドーム', 'ゴム'],
              'plist': [0.6, 0.4]},
             {'before': '<!--is-not-->',
              'after': ['ありません', 'ないです'],
              'plist': [0.8, 0.2]},
             {'before': '<!--absolutely-->',
              'after': ['絶対に', '本当に'],
              'plist': [0.6, 0.4]},
             {'before': '<!--very-->',
              'after': ['かなり', '本当に', 'とても', '相当', '結構'],
              'plist': [0.3, 0.1, 0.2, 0.2, 0.2]},
             {'before': '<!--well-->',
              'after': ['非常に', 'かなり', 'とても'],
              'plist': [0.3, 0.5, 0.2]},
             {'before': '<!--success-rate-->',
              'after': ['確率', '成功率']},
             {'before': '<!--rate-->',
              'after': ['確率', '可能性'],
              'plist': [0.6, 0.4]},
             {'before': '<!--cost-->',
              'after': ['お金', '費用', 'コスト']},
             {'before': '<!--low-cost-->',
              'after': ['安い費用', '低コスト', '安い金額']},
             {'before': '<!--money-->',
              'after': ['お金', '金', '金銭'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--chance-d-->',
              'after': ['出会いのチャンス', '出会えるチャンス', '出会いの機会', '出会える機会'],
              'plist': [0.4, 0.3, 0.2, 0.1]},
             {'before': '<!--chance-->',
              'after': ['チャンス', '機会', '好機'],
              'plist': [0.5, 0.4, 0.1]},
             {'before': '<!--point-->',
              'after': ['ポイント', 'サイト内ポイント'],
              'plist': [0.6, 0.4]},
             {'before': '<!--potency-->',
              'after': ['可能性が高', '可能性が大き', 'ことが多', '場合が多', '見込みが大き'],
              'plist': [0.3, 0.2, 0.2, 0.2, 0.1]},
             {'before': '<!--nicely-->',
              'after': ['うまく', '上手に'],
              'plist': [0.6, 0.4]},
             {'before': '<!--nicely2-->',
              'after': ['うまく', '思ったように', '思い通りに'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--certainly-->',
              'after': ['必ず', '絶対に', '確実に'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--surely-->',
              'after': ['確実に', '高確率で', '高い確率で', '間違いなく'],
              'plist': [0.4, 0.2, 0.2, 0.2]},
             {'before': '<!--surely-a-->',
              'after': ['確実な', '堅実な', '高確率な', '間違いのない']},
             {'before': '<!--partner-->',
              'after': ['相手', 'パートナー'],
              'plist': [0.6, 0.4]},
             {'before': '<!--think2-->',
              'after': ['だと思います', 'でしょう'],
              'plist': [0.7, 0.3]},
             {'before': '<!--think-->',
              'after': ['と思います', 'でしょう'],
              'plist': [0.6, 0.4]},
             {'before': '<!--may-be-->',
              'after': ['かも知れません', '可能性もあります', 'こともあります'],
              'plist': [0.5, 0.2, 0.3]},
             {'before': '<!--friend-->',
              'after': ['友達', '友人'],
              'plist': [0.7, 0.3]},
             {'before': '<!--real-->',
              'after': ['現実', 'リアル']},
             {'before': '<!--real2-->',
              'after': ['本物の', 'リアルな'],
              'plist': [0.6, 0.4]},
             {'before': '<!--various-->',
              'after': ['様々な', '多種多様な', 'いろいろな', 'いろんな'],
              'plist': [0.3, 0.2, 0.3, 0.2]},
             {'before': '<!--because-->',
              'after': ['ので', 'ですから', 'ため', 'から'],
              'plist': [0.3, 0.2, 0.3, 0.2]},
             {'before': '<!--lie-->',
              'after': ['嘘', 'ウソ', '偽り', 'ニセモノ']},
             {'before': '<!--experience-->',
              'after': ['体験談', '体験']},
             {'before': '<!--beginner-->',
              'after': ['初心者の方', '初心者', '初めての方', 'ビギナー']},
             {'before': '<!--suddenly-->',
              'after': ['いきなり', '急に', '突然', '前触れもなく']},
             {'before': '<!--dealer-->',
              'after': ['業者', '悪質業者', '悪質な業者'],
              'plist': [0.6, 0.2, 0.2]},
             {'before': '<!--bad-site-->',
              'after': ['悪質出会い系サイト', '悪質出会い系', '出会えない系', '出会えない系サイト', '詐欺サイト']},
             {'before': '<!--at-first-l-->',
              'after': ['最初に', '初めて']},
             {'before': '<!--at-first-->',
              'after': ['最初', '初め']},
             {'before': '<!--privacy-->',
              'after': ['個人情報', 'プライバシー', 'プライバシー情報'],
              'plist': [0.5, 0.2, 0.3]},
             {'before': '<!--at-all-->',
              'after': ['全く', '全然']},
             {'before': '<!--anonymous-->',
              'after': ['匿名で', '実名を出さず', '本名を出さずに'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--response-->',
              'after': ['レス', 'リプライ', '応答'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--comment-->',
              'after': ['コメント', '書き込み']},
             {'before': '<!--warn-->',
              'after': ['気をつけましょう', '気をつけてください', '注意してください', '注意が必要です', '注意しましょう'],
              'plist': [0.2, 0.3, 0.2, 0.1, 0.2]},
             {'before': '<!--on-earth-->',
              'after': ['そもそも', 'だいたい'],
              'plist': [0.6, 0.4]},
             {'before': '<!--best-->',
              'after': ['ベスト', '最適'],
              'plist': [0.6, 0.4]},
             {'before': '<!--love-->',
              'after': ['恋愛', '恋愛関係', '恋人関係'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--good-->',
              'after': ['良い', 'いい', '素敵な', '素晴らしい']},
             {'before': '<!--one-night-->',
              'after': ['行きずり', 'ワンナイトラブ', '一夜限り', '一回だけ']},
             {'before': '<!--little-->',
              'after': ['少しだけ', 'ちょっとだけ', 'ほんの少し']},
             {'before': '<!--you-->',
              'after': ['あなた', '自分']},
             {'before': '<!--me-->',
              'after': ['私', '自分']},
             {'before': '<!--own-->',
              'after': ['自ら', '自分', '自分自身']},
             {'before': '<!--very-good-->',
              'after': ['最高', '極上'],
              'plist': [0.6, 0.4]},
             {'before': '<!--so-far-->',
              'after': ['これまで', '今まで', '現在まで'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--many-->',
              'after': ['たくさん', '数多く'],
              'plist': [0.6, 0.4]},
             {'before': '<!--many2-->',
              'after': ['たくさんの', '数多くの', '多数の'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--everyday-life-->',
              'after': ['普段の生活', '日常生活', 'いつもの生活'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--easily-->',
              'after': ['容易に', '簡単に']},
             {'before': '<!--easy-->',
              'after': ['簡単', '易しい', '難しくない', '容易'],
              'plist': [0.5, 0.1, 0.2, 0.2]},
             {'before': '<!--relatively-->',
              'after': ['比較的', '割りと', '結構'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--in-detail-->',
              'after': ['詳しく', '詳細に', '事細かに'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--find-->',
              'after': ['求めて', '探して'],
              'plist': [0.3, 0.7]},
             {'before': '<!--can-find-->',
              'after': ['見つけられる', '探せる'],
              'plist': [0.4, 0.6]},
             {'before': '<!--find2-->',
              'after': ['見つけて', '探して'],
              'plist': [0.4, 0.6]},
             {'before': '<!--seriously-->',
              'after': ['本気で', '真剣に', '真面目に'],
              'plist': [0.5, 0.2, 0.3]},
             {'before': '<!--re-mail-->',
              'after': ['返信', '返事']},
             {'before': '<!--merit-->',
              'after': ['メリット', '利点', '良い点']},
             {'before': '<!--intimate-->',
              'after': ['親密に', '仲良く'],
              'plist': [0.3, 0.7]},
             {'before': '<!--acquaintance-->',
              'after': ['知人', '知り合い', '知ってる人'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--illegal-->',
              'after': ['違法', '法律違反', '犯罪']},
             {'before': '<!--making-love-->',
              'after': ['<!--sex-->', '出会って<!--sex-->'],
              'plist': [0.7, 0.3]},
             {'before': '<!--R18-->',
              'after': ['18歳未満の', '18歳に満たない', '18歳になっていない'],
              'plist': [0.6, 0.2, 0.2]},
             {'before': '<!--like-->',
              'after': ['みたいな', 'のような']},
             {'before': '<!--japan-->',
              'after': ['日本', '我が国', 'この国'],
              'plist': [0.6, 0.2, 0.2]},
             {'before': '<!--exist-->',
              'after': ['いる', 'いらっしゃる'],
              'plist': [0.4, 0.6]},
             {'before': '<!--address-->',
              'after': ['メアド', 'メールアドレス', 'アドレス', 'メルアド'],
              'plist': [0.3, 0.5, 0.1, 0.1]},
             {'before': '<!--smart-phone-->',
              'after': ['スマホ', 'スマートフォン', '携帯']},
             {'before': '<!--entry-->',
              'after': ['登録', '入会登録', '入会', 'エントリー'],
              'plist': [0.4, 0.3, 0.2, 0.1]},
             {'before': '<!--self-int-->',
              'after': ['自己紹介文', '自由コメント', '自己PR', '一口コメント'],
              'plist': [0.2, 0.3, 0.3, 0.2]},
             {'before': '<!--photo-->',
              'after': ['写真', '画像']},
             {'before': '<!--to-sex-->',
              'after': ['ヤリモク', 'セックス目的', 'エッチ目的', '身体目当て', 'カラダ目的'],
              'plist': [0.3, 0.3, 0.2, 0.1, 0.1]},
             {'before': '<!--rich-->',
              'after': ['お金持ち', '金持ち', 'セレブ'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--wife2-->',
              'after': ['奥さん', '妻', '配偶者', '夫人'],
              'plist': [0.4, 0.2, 0.2, 0.2]},
             {'before': '<!--husband-->',
              'after': ['既婚男性', '既婚者', '妻子持ち'],
              'plist': [0.5, 0.3, 0.2]},
             {'before': '<!--whore-->',
              'after': ['割り切り', 'ワリキリ', 'サポート', '援交'],
              'plist': [0.4, 0.3, 0.2, 0.1]},
             {'before': '<!--deaikei2-->',
              'after': ['出会い系サイト', '出会い系', '出会いアプリ', 'マッチングサイト', 'コミュニティサイト']},
             {'before': '<!--blog-->',
              'after': ['当サイト', '本サイト', '弊サイト']},
             {'before': '<!--communication-->',
              'after': ['やり取り', 'コミュニケーション', '連絡']},
             {'before': '<!--communicate-->',
              'after': ['やり取りする', '連絡を取る', 'メールで話す']},
             {'before': '<!--conversation-->',
              'after': ['会話', '話'],
              'plist': [0.6, 0.4]},
             {'before': '<!--look-->',
              'after': ['見た目', '外見', 'ルックス']},
             {'before': '<!--secret-->',
              'after': ['コツ', '秘訣', 'ポイント', '裏技', '裏ワザ'],
              'plist': [0.4, 0.1, 0.3, 0.1, 0.1]},
             {'before': '<!--important-->',
              'after': ['重要', '大事', '大切']},
             {'before': '<!--crucial-->',
              'after': ['大事', '大切']},
             {'before': '<!--woman-y-->',
              'after': ['女の子', '女子']},
             {'before': '<!--woman-o-->',
              'after': ['女性', '女の人']},
             {'before': '<!--woman-->',
              'after': ['女性', '女の子', '女子', '女の人'],
              'plist': [0.5, 0.3, 0.1, 0.1]},
             {'before': '<!--woman-n-->',
              'after': ['女子', '女性'],
              'plist': [0.7, 0.3]},
             {'before': '<!--description-->',
              'after': ['解説', '説明', '紹介'],
              'plist': [0.3, 0.4, 0.3]},
             {'before': '<!--there-->',
              'after': ['この記事', '当記事', '本稿'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--author-->',
              'after': ['私', '管理人', '筆者']},
             {'before': '<!--page-->',
              'after': ['記事', 'ページ'],
              'plist': [0.7, 0.3]},
             {'before': '<!--way-to-->',
              'after': ['出会い方', '出会いの方法', '出会いのやり方'],
              'plist': [0.4, 0.3, 0.3]},
             {'before': '<!--handsome-->',
              'after': ['イケメン', '男前', 'いい男'],
              'plist': [0.5, 0.4, 0.1]},
             {'before': '<!--search-->',
              'after': ['検索', 'サーチ'],
              'plist': [0.7, 0.3]},
             {'before': '<!--friend2-->',
              'after': ['友達', '仲間'],
              'plist': [0.6, 0.4]},
             {'before': '<!--adult-->',
              'after': ['エッチな出会い', '大人の出会い', 'アダルトな出会い', 'エッチな関係', '大人の関係', 'ヤリモクの出会い',
                        'エッチな大人の出会い', '大人の交際', '遊びの関係', 'エッチな交際']},
             {'before': '<!--free-point-->',
              'after': ['無料体験ポイント', '無料お試しポイント', '無料ポイント', 'お試し用無料ポイント']},
             {'before': '<!--b-bbs-->',
              'after': ['募集掲示板', '募集用掲示板', '掲示板']},
             {'before': '<!--s-bbs-->',
              'after': ['出会い掲示板', '出会い募集掲示板', 'ネット掲示板', '掲示板', '出会いBBS']},
             {'before': '<!--d-bbs-->',
              'after': ['出会い掲示板', '出会い系掲示板', '掲示板']},
             {'before': '<!--adult-bbs-->',
              'after': ['アダルト掲示板', 'アダルト系の掲示板', 'エッチ系の掲示板', '大人の出会い用掲示板']},
             {'before': '<!--pure-bbs-->',
              'after': ['ピュア掲示板', 'ピュア系掲示板', 'ピュア系の掲示板', '真面目な出会い系の掲示板']},
             {'before': '<!--site-blog-->',
              'after': ['サイト', 'ブログ']},
             {'before': '<!--google-->',
              'after': ['Google', 'グーグル']},
             {'before': '<!--sample-->',
              'after': ['例文', '文例', '文章例', 'メールサンプル', 'メールの例文', 'メッセージ例文', 'メッセージ例']},
             {'before': '<!--area-->',
              'after': ['地域', 'エリア'],
              'plist': [0.7, 0.3]},
             {'before': '<!--name-boobs-->',
              'after': ['おっぱい', '胸', 'バスト'],
              'plist': [0.4, 0.4, 0.2]},
             {'before': '<!--pop-and-famous-n-->',
              'after': ['人気のある', '人気の', '大手の', '有名な']},
             {'before': '<!--pop-and-famous-p-->',
              'after': ['人気', '大手', '有名']},
             {'before': '<!--pop-p-->',
              'after': ['人気', '大人気']},
             {'before': '<!--pop-n-->',
              'after': ['人気のある', '人気の', '大人気の']},
             {'before': '<!--famous-p-->',
              'after': ['大手', '有名']},
             {'before': '<!--famous-n-->',
              'after': ['大手の', '有名な']},
             {'before': '<!--question-->',
              'after': ['疑問', '質問']},
             {'before': '<!--men-and-women-->',
              'after': ['男女', '男性女性', '男性と女性']},
             {'before': '<!--men-or-women-->',
              'after': ['男でも女でも', '男性でも女性でも', '男性女性関係なく', '男女関係なく']},
             {'before': '<!--instinct-->',
              'after': ['本能', '欲望', '情欲']},
             {'before': '<!--size-of-bust-->',
              'after': ['B', 'C', 'D', 'E', 'F', 'G']},
             {'before': '<!--real-name-->',
              'after': ['本名', '実名', '本当の名前', 'リアルの名前']},
             {'before': '<!--kiss-or-sof-->',
              'after': ['キスフレ', 'ソフレ', 'キスフレやソフレ', 'ソフレやキスフレ']},
             {'before': '<!--job-->',
              'after': ['職業', '仕事']},
             {'before': '<!--eros-degree-->',
              'after': ['エロさ', 'エッチさ']},
             {'before': '<!--serious-per-->',
              'after': ['真面目', '純粋', '生真面目']},
             {'before': '<!--regardless-->',
              'after': ['関係なく', '無関係に']},
             {'before': '<!--relationship-->',
              'after': ['人間関係', '人との付き合い', '他人との関係']},
             {'before': '<!--relation-->',
              'after': ['関係', '付き合い', '交際']},
             {'before': '<!--not-communicate-->',
              'after': ['コミュ障害', '人が苦手', '人付き合いが苦手']},
             {'before': '<!--for-real-->',
              'after': ['実際に', 'リアルで']},
             {'before': '<!--in-real-->',
              'after': ['実際には', '現実では']},
             {'before': '<!--use-->',
              'after': ['使用して', '使って', '利用して']},
             {'before': '<!--use-a-->',
              'after': ['使用した', '使った', '利用した']},
             {'before': '<!--use-i-->',
              'after': ['使い', '利用し']},
             {'before': '<!--use-u-->',
              'after': ['使用する', '使う', '利用する']},
             {'before': '<!--can-use-->',
              'after': ['利用できる', '使える']},
             {'before': '<!--if-use-->',
              'after': ['利用すれば', '使えば']},
             {'before': '<!--reply-->',
              'after': ['リアクション', '返信', 'リプライ']},
             {'before': '<!--reply-m-->',
              'after': ['返事', '返信', 'リプライ']},
             {'before': '<!--divorce-->',
              'after': ['バツイチ', 'バツあり']},
             {'before': '<!--go-introduce-->',
              'after': ['ご紹介', 'ご案内']},
             {'before': '<!--way-to-encounter-->',
              'after': ['出会いの方法', '出会いのやり方', '出会い方', '出会う方法']},
             {'before': '<!--others-->',
              'after': ['他人', '他の人']},
             {'before': '<!--target-person-->',
              'after': ['人', '女性', '女の人']},
             {'before': '<!--case-->',
              'after': ['ケース', '場合']},
             {'before': '<!--occasion-->',
              'after': ['場合', '時', '際']},
             {'before': '<!--other-side-->',
              'after': ['相手', '向こう', 'あちら', '先方', '相手の<!--target-person-->']},
             {'before': '<!--companion-->',
              'after': ['結婚相手', '運命の相手', '人生のパートナー', '伴侶']},
             {'before': '<!--can-meet-with-->',
              'after': ['と出会える', 'との出会いが見つかる', 'と出会うことができる']},
             {'before': '<!--can-meet-->',
              'after': ['出会える', '出会うことができる']},
             {'before': '<!--can-meet-i-->',
              'after': ['出会っ', '出会うことができ']},
             {'before': '<!--can-meet-s-->',
              'after': ['出会えます', '出会うことができます']},
             {'before': '<!--from-me-->',
              'after': ['自分から', 'こちらから']},
             {'before': '<!--conservative-->',
              'after': ['ガードが固', '身持ちが堅']},
             {'before': '<!--not-conservative-->',
              'after': ['ガードが緩', '貞操観念が低']},
             {'before': '<!--liking-->',
              'after': ['好みのタイプ', '好み', 'ストライクゾーン']},
             {'before': '<!--not-liking-->',
              'after': ['好みじゃな', '好きじゃな', '好みのタイプじゃな']},
             {'before': '<!--spam-mail-->',
              'after': ['スパムメール', '迷惑メール']},
             {'before': '<!--mail-magazine-->',
              'after': ['メールマガジン', 'メルマガ']},
             {'before': '<!--style-->',
              'after': ['体型', 'スタイル']},
             {'before': '<!--cost-performance-->',
              'after': ['効率', 'コスパ', 'コストパフォーマンス']},
             {'before': '<!--spare-time-->',
              'after': ['空き時間', '空いた時間', '暇な時間', '自由時間']},
             {'before': '<!--time-zone-->',
              'after': ['時間帯', '時間']},
             {'before': '<!--time-->',
              'after': ['時間', '時']},
             {'before': '<!--purpose-->',
              'after': ['目的', '目当て', '狙い']},
             {'before': '<!--communication-skill-->',
              'after': ['コミュニケーション能力', 'コミュニケーション力', 'コミュ力', 'コミュニケーションスキル']},
             {'before': '<!--socialize-women-->',
              'after': ['女性慣れし', '女慣れし', '女性に慣れ']},
             {'before': '<!--some-->',
              'after': ['複数の', 'いくつかの']},
             {'before': '<!--leak-->',
              'after': ['バレ', '知られ']},
             {'before': '<!--result-->',
              'after': ['最終的に', '結果的に']},
             {'before': '<!--approach-->',
              'after': ['アプローチする', '誘う']},
             {'before': '<!--approach-e-->',
              'after': ['アプローチして', '誘って']},
             {'before': '<!--impression-->',
              'after': ['印象', 'イメージ']},
             {'before': '<!--everyone-->',
              'after': ['誰でも', 'どんな人でも', '誰だって', 'どなたでも']},
             {'before': '<!--process-->',
              'after': ['手順', 'ステップ', 'プロセス', '順番']},
             {'before': '<!--showman-->',
              'after': ['芸能人', '有名人', 'テレビに出る人']},
             {'before': '<!--site-tell-->',
              'after': ['サイト内電話', 'サイトの電話', 'サイトの電話機能']},
             {'before': '<!--appoint-->',
              'after': ['約束', 'アポ']},
             {'before': '<!--talk-->',
              'after': ['やりとり', 'やり取り', '会話', '話']},
             {'before': '<!--real-meet-->',
              'after': ['会う', '実際に会う', 'リアルで会う']},
             {'before': '<!--regular-->',
              'after': ['普通の', '一般的な']},
             {'before': '<!--mail-talk-->',
              'after': ['メール交換', 'メールのやりとり', 'メッセージ交換']},
             {'before': '<!--kind-->',
              'after': ['優しい', '思いやりがある']},
             {'before': '<!--charming-->',
              'after': ['魅力的', '素敵']},
             {'before': '<!--lately-->',
              'after': ['最近', '近年']},
             {'before': '<!--age-->',
              'after': ['年代', '年齢層']},
             {'before': '<!--free-->',
              'after': ['無料', 'タダ']},
             {'before': '<!--boldly-->',
              'after': ['思い切って', '大胆に']},
             {'before': '<!--usual-->',
              'after': ['普段', '日常で', '日常生活で']},
             {'before': '<!--contact-point-->',
              'after': ['連絡先', 'アドレス', 'ラインID']},
             {'before': '<!--familiarity-->',
              'after': ['親近感', '親しみ']},
             {'before': '<!--bad-request-->',
              'after': ['架空請求', '不当請求']},
             {'before': '<!--understand-->',
              'after': ['理解できる', 'わかる']},
             {'before': '<!--judge-->',
              'after': ['判断できる', '分かる']},
             {'before': '<!--find-d-i-->',
              'after': ['出会いを探し', '出会っ']},
             {'before': '<!--find-d-u-->',
              'after': ['出会いを探す', '出会う']},
             {'before': '<!--find-d-u-with-->',
              'after': ['との出会いを探す', 'と出会う']},
             {'before': '<!--can-find-d-e-->',
              'after': ['出会いを探せ', '出会え']},
             {'before': '<!--can-find-d-e-with-->',
              'after': ['との出会いを探せ', 'と出会え']},
             {'before': '<!--can-find-d-u-->',
              'after': ['出会いを探せる', '出会える', '出会うことができる', '出会いを探すことができる']},
             {'before': '<!--can-find-d-u-s-->',
              'after': ['出会いを探せます', '出会えます', '出会うことができます', '出会いを探すことができます', '出会うことが可能です']},
             {'before': '<!--can-find-d-u-with-->',
              'after': ['との出会いを探せる', 'と出会える', 'と出会うことができる', 'との出会いを探すことができる']},
             {'before': '<!--full-rate-->',
              'after': ['１００％', '100％', '１０割']},
             {'before': '<!--rumor-->',
              'after': ['都市伝説', '噂']},
             {'before': '<!--recommended-->',
              'after': ['おすすめ', '人気の', '定番']},
             {'before': '<!--title-can-meet-->',
              'after': ['会える', '出会える']},
             {'before': '<!--title-easy-->',
              'after': ['簡単な', '手軽な', '楽な', '誰でもできる', '初心者向け']},
             {'before': '<!--make-way-->',
              'after': ['の作り方', 'の探し方']},
             {'before': '<!--make-way-g-->',
              'after': ['を作る方法', 'を探す方法']},
             {'before': '<!--do-mail-->',
              'after': ['メールをする', 'メールする', 'メッセージのやりとりをする']},
             {'before': '<!--question-mail-->',
              'after': ['質問メール', '質問メッセージ', '質問のメール']},
             {'before': '<!--mail-continue-->',
              'after': ['長続きする', '長く続く', '質問のメール']},
             {'before': '<!--like-thing-->',
              'after': ['好きなこと', '興味あること']},
             {'before': '<!--like-a-->',
              'after': ['好きな', 'お気に入りの']},
             {'before': '<!--like-s-->',
              'after': ['好きです', 'お気に入りです']},
             {'before': '<!--sympathy-->',
              'after': ['共感', 'シンパシー']},
             {'before': '<!--do-sympathy-->',
              'after': ['共感する', '同調する']},
             {'before': '<!--topic-->',
              'after': ['話題', '話のネタ', '話のタネ']},
             {'before': '<!--to-be-popular-->',
              'after': ['モテる', '女性に好かれる']},
             {'before': '<!--to-be-popular-e-->',
              'after': ['モテて', '女性に好かれて']},
             {'before': '<!--talk-s-->',
              'after': ['トーク', '会話']},
             {'before': '<!--talk-tec-->',
              'after': ['トークテクニック', '話術', '会話の技術']},
             {'before': '<!--talk-way-->',
              'after': ['話し方', '話法']},
             {'before': '<!--agreement-->',
              'after': ['同意', '賛成']},
             {'before': '<!--like-this-->',
              'after': ['このような', 'こんな感じの']},
             {'before': '<!--at-online-->',
              'after': ['オンライン', 'ネット', 'インターネット']},
             {'before': '<!--positive-->',
              'after': ['ポジティブ', '前向き', '積極的']},
             {'before': '<!--negative-->',
              'after': ['ネガティブ', '後ろ向き', '否定的']},
             {'before': '<!--flow-to-->',
              'after': ['流れ', 'やり方']},
             {'before': '<!--words-->',
              'after': ['言葉', 'ワード']},
             {'before': '<!--approach-n-->',
              'after': ['アプローチ', '話しかけ方']},
             {'before': '<!--enough-->',
              'after': ['OKです', '十分です', '十分です', '良いです', 'いいです'],
              'omit': ['いいですね', '良いですね']},
             {'before': '<!--copy-and-paste-->',
              'after': ['コピペ', 'コピーアンドペースト', 'コピー＆ペースト']},
             {'before': '<!--many-sp-->',
              'after': ['多数', 'たくさん', '数多く']},
             {'before': '<!--bitch-->',
              'after': ['ヤリマン', 'ビッチ']},
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
             {'before': '<!--check-prf3-->',
              'after': ['プロフ閲覧', 'プロフチェック', 'プロフィール閲覧', 'プロフィール確認', 'プロフ確認', 'プロフィールチェック']},
             {'before': '<!--be-famous-with-->',
              'after': ['で有名です', 'で定評があります', 'で知られています']},
             {'before': '<!--make-this-->',
              'after': ['作った', '作成した']},
             {'before': '<!--is-writen-s-->',
              'after': ['書かれています', '記載されています']},
             {'before': '<!--be-early-->',
              'after': ['早く', '早急に', 'すぐに']},
             {'before': '<!--write-in-bbs-->',
              'after': ['掲示板に書き込み', '掲示板に投稿', '掲示板に募集の書き込み']},
             {'before': '<!--from-me-r-->',
              'after': ['こちらから', '自分から', '自分の方から']},
             {'before': '<!--you-must-do-->',
              'after': ['すべし', 'するのがベターです', 'した方が良いです', 'しましょう']},
             {'before': '<!--for-the-moment-->',
              'after': ['とりあえず', 'さしあたって', '一旦', 'ひとまず']},
             {'before': '<!--fight-for-->',
              'after': ['頑張って', 'がんばって', '気合を入れて'],
              'omit': ['がんばって下さい', '頑張って下さい']},
             {'before': '<!--can-sex-->',
              'after': ['セックスできる', 'エッチできる', 'やれる']},
             {'before': '<!--want-to-know-i-->',
              'after': ['を教えて欲しい！', 'が知りたい！']},
             {'before': '<!--i-dont-know-->',
              'after': ['がよく分からない', 'が分からない', 'を知らない', 'をよく知らない', 'が<!--at-all-->分からない']},
             {'before': '<!--but-and-c-->',
              'after': ['けど、', 'が、', 'けれど、'],
              'omit': ['ですが、']},
             {'before': '<!--mail-app-->',
              'after': ['メール自動作成アプリ', 'メール作成アプリ', 'メッセージ作成アプリ', 'メール例文アプリ']},
             {'before': '<!--app-to-write-->',
              'after': ['書けるアプリ', '作成できるアプリ', '送れるアプリ', 'できるアプリ']},
             {'before': '<!--not-good-at-adj-->',
              'after': ['苦手な', '得意じゃない', 'あまり上手じゃない']},
             {'before': '<!--90-percent-->',
              'after': ['90％', '９０％', '９割', '九割']},
             {'before': '<!--how-to-do-q-->',
              'after': ['ってどうやればいいの', 'はどのようにすればいい', 'どうすれば上手くできる', 'どの<!--way-->がベスト']},
             {'before': '<!--can-not-anyway-->',
              'after': ['いくらやっても', 'どんなにがんばっても', 'どれだけ努力しても']},
             {'before': '<!--look-difficult-->',
              'after': ['難しそう', '大変そう', '困難そう', 'できなさそう']},
             {'before': '<!--prepare-for-->',
              'after': ['用意してある', '準備している', '完備している']},
             {'before': '<!--fact-->',
              'after': ['真実', '事実']},
             {'before': '<!--surprising-->',
              'after': ['衝撃の', '驚愕の', '驚くべき', '驚きの']},
             {'before': '<!--tell-to-you-->',
              'after': ['お伝えします', 'お教えします']},
             {'before': '<!--have-made-->',
              'after': ['作りました', '作成しました', '完成させました']},
             {'before': '<!--not-good-at-writing-->',
              'after': ['文才がない', '作文が苦手', '国語が不得意', '上手く手紙が書けない', '文章が下手', '文章が書けない']},
             {'before': '<!--to-the-last-->',
              'after': ['最後まで', '終わりまで', 'ラストまで']},
             {'before': '<!--please-read-->',
              'after': ['読んでみて下さい', '読んでください', '読んでみてください', 'お読みください']},
             {'before': '<!--only-to-know-->',
              'after': ['知ってさえいれば', '理解してさえいれば', '理解できてさえいれば']},
             {'before': '<!--if-know-->',
              'after': ['知っていれば', '理解していれば', '理解できていれば']},
             {'before': '<!--important-point-->',
              'after': ['必要な部分', '大事なところ', '大事な部分', '必要なポイント', '必要な要素', '大事なポイント', '要点']},
             {'before': '<!--which-site-->',
              'after': ['どこの<!--site-->', 'どの<!--site-->', 'いずれの<!--site-->']},
             {'before': '<!--make-to-be-able-->',
              'after': ['できるようになっています', 'できるようにしてあります', 'できるようになります']},
             {'before': '<!--your-thinking-->',
              'after': ['そんな気持ちで', 'そのような思いで', 'そう考えて']},
             {'before': '<!--must-be-useful-->',
              'after': ['の役に立つはず', 'に有用なはず', 'に貢献するはず']},
             {'before': '<!--rather-->',
              'after': ['少し', '少々']},
             {'before': '<!--by-all-means-->',
              'after': ['是非とも', '是非', 'どうぞ']},
             {'before': '<!--right-way-->',
              'after': ['正しい', '適切な', '適正な', '妥当な']},
             {'before': '<!--be-right-way-->',
              'after': ['正しく', '適切に', '適正に']},
             {'before': '<!--no-digg-->',
              'after': ['間違いない', '疑いない', '明白な', '紛れもない']},
             {'before': '<!--do-real-->',
              'after': ['実践', '実行']},
             {'before': '<!--be-made-so-->',
              'after': ['なっていますから', 'なっているので']},
             {'before': '<!--be-useful-->',
              'after': ['役立つ', '役に立つ']},
             {'before': '<!--do-copy-->',
              'after': ['真似して', '真似をして', 'コピーして', '模倣して']},
             {'before': '<!--can-send-->',
              'after': ['送ることができる', '送れる', '送信できる', '出せる']},
             {'before': '<!--that-much-->',
              'after': ['そんなに', 'そこまで', 'それほど']},
             {'before': '<!--publish-e-->',
              'after': ['掲載して', '載せて', '紹介して']},
             {'before': '<!--at-a-glance-->',
              'after': ['一見', 'ぱっと見', '見た感じ', '一見すると', '表面的には']},
             {'before': '<!--can-u-->',
              'after': ['可能な', 'できる'],
              'omit': ['できるだけ']},
             {'before': '<!--arrive-at-p-->',
              'after': ['たどり着いた', '到った', 'やって来た']},
             {'before': '<!--is-not-good-->',
              'after': ['が悪い', 'が良くない']},
             ]

o_other = ['一方、', 'それに対して、', 'それとは異なり、']

conj_list = [{'before': '<!--c-逆接-->',
              'after': ["しかし", "しかしながら", "けれども", "でも", "ところが", "ですが"]},
             {'before': '<!--c-並列-->',
              'after': ["また", "同様に", "同じように", "同じく"]},
             {'before': '<!--c-逆接-前提-->',
              'after': ["ですが", "ものの", "とはいえ"]},
             {'before': '<!--c-順接-->',
              'after': ["そのため", "ですから", "だから", "このため", "それで", "その結果"]},
             {'before': '<!--c-添加-->',
              'after': ["そして", "それに", "それから"]},
             {'before': '<!--c-添加2-->',
              'after': ["さらに", "しかも", "おまけに", "そのうえ", "そして更に"]},
             {'before': '<!--c-言換-->',
              'after': ["つまり", "すなわち", "要するに"]},
             {'before': '<!--c-解説-->',
              'after': ["このように", "こんな感じで", "ということで"]},
             {'before': '<!--c-説明-->',
              'after': ["というのも", "なぜなら"]},
             {'before': '<!--c-補足-->',
              'after': ["なお", "もっとも", "ただ", "ただし"]},
             {'before': '<!--c-補足2-->',
              'after': ["ちなみに", "余談ですが"]},
             {'before': '<!--c-対比-->',
              'after': ["逆に", "反対に"]},
             {'before': '<!--c-総括-->',
              'after': ["以上", "ということで", "といった感じで", 'ここまで', 'という感じで']},
             {'before': '<!--c-当然-->',
              'after': ["もちろん", "当然", "当然のことですが"]},
             {'before': '<!--c-じっさい-->',
              'after': ["実際", "現実に", "実際のところ", "実のところ", "実際に"]}
             ]

ignore_words = ['から', 'ので', 'いい', '良い', 'ため', 'H']

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
    'ますですから': 'ますので',
    '話しかけ方できる': 'アプローチできる',
    'デ良い点': 'デメリット',
    '素敵なね': 'いいね',
    'より絶対に': '高確率で',
    '定番します': '推奨します',
    'するから': 'するため',
    '早く絶対に': '早くそしてより確実に',
    'ですけれど': 'ですが'
}
